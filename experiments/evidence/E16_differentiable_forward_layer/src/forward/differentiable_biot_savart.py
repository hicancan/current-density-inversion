"""Differentiable Biot-Savart forward layer for 2D sheet and via currents.

FFT-domain differentiable Biot-Savart forward. Sheet Jx/Jy -> Bx/By/Bz, via
source/sink s_l -> Bx/By. CPU numpy reference + optional torch autograd.
No CUDA hard dependency. All SI units.
"""
from __future__ import annotations

import numpy as np
from typing import Optional, Tuple

MU0 = 4.0e-7 * np.pi
_FOUR_PI = 4.0 * np.pi
_min_k = np.float64(1e-100)


def _fftfreq_2d(nx, ny, dx, dy):
    kx_1d = 2.0 * np.pi * np.fft.fftfreq(nx, d=dx).astype(np.float64)
    ky_1d = 2.0 * np.pi * np.fft.fftfreq(ny, d=dy).astype(np.float64)
    return kx_1d[np.newaxis, :], ky_1d[:, np.newaxis], np.sqrt(kx_1d[np.newaxis, :]**2 + ky_1d[:, np.newaxis]**2)


def _check_torch_available():
    try:
        import torch
        try:
            return True, torch.cuda.is_available()
        except Exception:
            return True, False
    except ImportError:
        return False, False


class BiotSavartForwardLayer:
    """Differentiable Biot-Savart forward operator.

    Parameters: nx, ny (int), dx, dy (float) [m].
    """

    def __init__(self, nx, ny, dx, dy):
        if nx < 2 or ny < 2:
            raise ValueError("grid dims >= 2 required")
        self.nx, self.ny, self.dx, self.dy = nx, ny, dx, dy
        kx, ky, k = _fftfreq_2d(nx, ny, dx, dy)
        self.kx, self.ky, self.k = kx, ky, k
        self._k_safe = np.maximum(k, _min_k)
        self._k0_mask = k < _min_k
        self.torch_available, self.cuda_available = _check_torch_available()

    @property
    def shape(self):
        return (self.ny, self.nx)

    def sheet_transfer_functions(self, dz):
        abs_dz = abs(dz)
        sign_dz = 1.0 if dz >= 0 else -1.0
        exp_factor = np.exp(-self._k_safe * abs_dz)
        k_s, k0 = self._k_safe, self._k0_mask
        mh = 0.5 * MU0
        T_bx_jy = np.where(k0, mh * sign_dz, mh * sign_dz * exp_factor)
        T_by_jx = np.where(k0, -mh * sign_dz, -mh * sign_dz * exp_factor)
        T_bz_jx = np.where(k0, 0.0, (1j * mh) * exp_factor * (-self.ky) / k_s)
        T_bz_jy = np.where(k0, 0.0, (1j * mh) * exp_factor * self.kx / k_s)
        return T_bx_jy, T_by_jx, T_bz_jx, T_bz_jy, k_s

    def sheet_to_B(self, Jx, Jy, source_z, obs_z, *, padding_factor=1, return_padded=False):
        Jx_a = np.asarray(Jx, dtype=np.float64)
        Jy_a = np.asarray(Jy, dtype=np.float64)
        if Jx_a.shape != self.shape or Jy_a.shape != self.shape:
            raise ValueError(f"expected shape {self.shape}")
        dz = obs_z - source_z
        T_bx_jy, T_by_jx, T_bz_jx, T_bz_jy, _ = self.sheet_transfer_functions(dz)

        if padding_factor > 1:
            ny_p, nx_p = self.ny * padding_factor, self.nx * padding_factor
            ny0, nx0 = (ny_p - self.ny) // 2, (nx_p - self.nx) // 2
            Jx_p = np.zeros((ny_p, nx_p), dtype=np.float64)
            Jy_p = np.zeros((ny_p, nx_p), dtype=np.float64)
            Jx_p[ny0:ny0+self.ny, nx0:nx0+self.nx] = Jx_a
            Jy_p[ny0:ny0+self.ny, nx0:nx0+self.nx] = Jy_a
            kx_p, ky_p, k_p = _fftfreq_2d(nx_p, ny_p, self.dx, self.dy)
            k_s_p = np.maximum(k_p, _min_k)
            k0_p = k_p < _min_k
            abs_dz = abs(dz)
            sign_dz = 1.0 if dz >= 0 else -1.0
            ef = np.exp(-k_s_p * abs_dz)
            mh = 0.5 * MU0
            Tbx = np.where(k0_p, mh*sign_dz, mh*sign_dz*ef)
            Tby = np.where(k0_p, -mh*sign_dz, -mh*sign_dz*ef)
            Tbz_x = np.where(k0_p, 0.0, (1j*mh)*ef*(-ky_p)/k_s_p)
            Tbz_y = np.where(k0_p, 0.0, (1j*mh)*ef*kx_p/k_s_p)
            Bx_p = np.fft.ifft2(Tbx * np.fft.fft2(Jy_p)).real
            By_p = np.fft.ifft2(Tby * np.fft.fft2(Jx_p)).real
            Bz_p = np.fft.ifft2(Tbz_x * np.fft.fft2(Jx_p) + Tbz_y * np.fft.fft2(Jy_p)).real
            if return_padded:
                return Bx_p, By_p, Bz_p
            return (Bx_p[ny0:ny0+self.ny, nx0:nx0+self.nx],
                    By_p[ny0:ny0+self.ny, nx0:nx0+self.nx],
                    Bz_p[ny0:ny0+self.ny, nx0:nx0+self.nx])

        Jx_f = np.fft.fft2(Jx_a)
        Jy_f = np.fft.fft2(Jy_a)
        return (np.fft.ifft2(T_bx_jy * Jy_f).real,
                np.fft.ifft2(T_by_jx * Jx_f).real,
                np.fft.ifft2(T_bz_jx * Jx_f + T_bz_jy * Jy_f).real)

    def via_kernel(self, z_bottom, z_top, obs_z, *, eps=1e-20):
        ny, nx = self.shape
        xs = (np.arange(nx) - nx//2) * self.dx
        ys = (np.arange(ny) - ny//2) * self.dy
        xx, yy = np.meshgrid(xs, ys)
        r2 = np.maximum(xx**2 + yy**2, eps)
        dzb, dzt = obs_z - z_bottom, obs_z - z_top
        Rb = np.sqrt(r2 + dzb**2)
        Rt = np.sqrt(r2 + dzt**2)
        integral = dzt / (r2 * Rt) - dzb / (r2 * Rb)
        pref = MU0 / _FOUR_PI
        return -pref * yy * integral, pref * xx * integral

    def via_to_Bxy(self, s_l, z_bottom, z_top, obs_z, *, padding_factor=1, return_padded=False):
        s_l_a = np.asarray(s_l, dtype=np.float64)
        if s_l_a.shape != self.shape:
            raise ValueError(f"expected shape {self.shape}")
        kx, ky = self.via_kernel(z_bottom, z_top, obs_z)
        kxs = np.fft.ifftshift(kx)
        kys = np.fft.ifftshift(ky)

        if padding_factor > 1:
            ny_p, nx_p = self.ny * padding_factor, self.nx * padding_factor
            ny0, nx0 = (ny_p - self.ny)//2, (nx_p - self.nx)//2
            s_p = np.zeros((ny_p, nx_p), dtype=np.float64)
            s_p[ny0:ny0+self.ny, nx0:nx0+self.nx] = s_l_a
            kx_p = np.zeros((ny_p, nx_p), dtype=np.float64)
            ky_p = np.zeros((ny_p, nx_p), dtype=np.float64)
            kx_p[ny0:ny0+self.ny, nx0:nx0+self.nx] = kx
            ky_p[ny0:ny0+self.ny, nx0:nx0+self.nx] = ky
            kxps = np.fft.ifftshift(kx_p)
            kyps = np.fft.ifftshift(ky_p)
            Bx_p = np.fft.ifft2(np.fft.fft2(kxps) * np.fft.fft2(s_p)).real
            By_p = np.fft.ifft2(np.fft.fft2(kyps) * np.fft.fft2(s_p)).real
            if return_padded:
                return Bx_p, By_p
            return (Bx_p[ny0:ny0+self.ny, nx0:nx0+self.nx],
                    By_p[ny0:ny0+self.ny, nx0:nx0+self.nx])

        return (np.fft.ifft2(np.fft.fft2(kxs) * np.fft.fft2(s_l_a)).real,
                np.fft.ifft2(np.fft.fft2(kys) * np.fft.fft2(s_l_a)).real)

    def multilayer_sum_B(self, B_list):
        if not B_list:
            raise ValueError("empty")
        f = B_list[0]
        if len(f) == 3:
            bx, by, bz = f[0].copy(), f[1].copy(), f[2].copy()
            for bi in B_list[1:]:
                bx += bi[0]; by += bi[1]; bz += bi[2]
            return bx, by, bz
        bx, by = f[0].copy(), f[1].copy()
        for bi in B_list[1:]:
            bx += bi[0]; by += bi[1]
        return bx, by

    def sheet_to_B_torch(self, Jx_t, Jy_t, source_z, obs_z, *, padding_factor=1):
        if not self.torch_available:
            raise RuntimeError("torch not available")
        import torch
        Jx_t = torch.as_tensor(Jx_t, dtype=torch.float64)
        Jy_t = torch.as_tensor(Jy_t, dtype=torch.float64)
        dev = Jx_t.device
        dx_t = torch.tensor(self.dx, device=dev, dtype=torch.float64)
        dy_t = torch.tensor(self.dy, device=dev, dtype=torch.float64)

        if padding_factor > 1:
            ny_p, nx_p = self.ny * padding_factor, self.nx * padding_factor
            ny0, nx0 = (ny_p-self.ny)//2, (nx_p-self.nx)//2
            Jx_p = torch.zeros(ny_p, nx_p, device=dev, dtype=torch.float64)
            Jy_p = torch.zeros(ny_p, nx_p, device=dev, dtype=torch.float64)
            Jx_p[ny0:ny0+self.ny, nx0:nx0+self.nx] = Jx_t
            Jy_p[ny0:ny0+self.ny, nx0:nx0+self.nx] = Jy_t
            Jx_f = torch.fft.fft2(Jx_p)
            Jy_f = torch.fft.fft2(Jy_p)
            kx1 = 2*np.pi*torch.fft.fftfreq(nx_p, d=dx_t, device=dev, dtype=torch.float64)
            ky1 = 2*np.pi*torch.fft.fftfreq(ny_p, d=dy_t, device=dev, dtype=torch.float64)
            kx_p, ky_p = kx1.unsqueeze(0), ky1.unsqueeze(1)
            k_p = torch.sqrt(kx_p**2+ky_p**2)
            ks_p = torch.clamp(k_p, min=_min_k)
            k0_p = k_p < _min_k
            abs_dz = abs(obs_z-source_z)
            sd = 1.0 if (obs_z-source_z) >= 0 else -1.0
            ef = torch.exp(-ks_p*abs_dz)
            mh = 0.5*MU0
            Tbx = torch.where(k0_p, torch.full_like(k_p, mh*sd), mh*sd*ef)
            Tby = torch.where(k0_p, torch.full_like(k_p, -mh*sd), -mh*sd*ef)
            kxo = torch.where(k0_p, torch.zeros_like(k_p), kx_p/ks_p)
            kyo = torch.where(k0_p, torch.zeros_like(k_p), ky_p/ks_p)
            Tbz_x = 1j*mh*ef*(-kyo)
            Tbz_y = 1j*mh*ef*kxo
            Bx_p = torch.fft.ifft2(Tbx*Jy_f).real
            By_p = torch.fft.ifft2(Tby*Jx_f).real
            Bz_p = torch.fft.ifft2(Tbz_x*Jx_f+Tbz_y*Jy_f).real
            return (Bx_p[ny0:ny0+self.ny, nx0:nx0+self.nx],
                    By_p[ny0:ny0+self.ny, nx0:nx0+self.nx],
                    Bz_p[ny0:ny0+self.ny, nx0:nx0+self.nx])

        Jx_f = torch.fft.fft2(Jx_t)
        Jy_f = torch.fft.fft2(Jy_t)
        kx1 = 2*np.pi*torch.fft.fftfreq(self.nx, d=dx_t, device=dev, dtype=torch.float64)
        ky1 = 2*np.pi*torch.fft.fftfreq(self.ny, d=dy_t, device=dev, dtype=torch.float64)
        kx_t, ky_t = kx1.unsqueeze(0), ky1.unsqueeze(1)
        k_t = torch.sqrt(kx_t**2+ky_t**2)
        ks_t = torch.clamp(k_t, min=_min_k)
        k0_t = k_t < _min_k
        abs_dz = abs(obs_z-source_z)
        sd = 1.0 if (obs_z-source_z) >= 0 else -1.0
        ef = torch.exp(-ks_t*abs_dz)
        mh = 0.5*MU0
        Tbx = torch.where(k0_t, torch.full_like(k_t, mh*sd), mh*sd*ef)
        Tby = torch.where(k0_t, torch.full_like(k_t, -mh*sd), -mh*sd*ef)
        kxo = torch.where(k0_t, torch.zeros_like(k_t), kx_t/ks_t)
        kyo = torch.where(k0_t, torch.zeros_like(k_t), ky_t/ks_t)
        Tbz_x = 1j*mh*ef*(-kyo)
        Tbz_y = 1j*mh*ef*kxo
        return (torch.fft.ifft2(Tbx*Jy_f).real,
                torch.fft.ifft2(Tby*Jx_f).real,
                torch.fft.ifft2(Tbz_x*Jx_f+Tbz_y*Jy_f).real)
