"""Small dependency-free SVG plots for exp07 reports."""

from __future__ import annotations

from pathlib import Path
import html
import math


def write_bar_svg(path: Path, labels: list[str], values: list[float], title: str, ylabel: str) -> None:
    width, height = 980, 420
    margin_l, margin_r, margin_t, margin_b = 80, 30, 55, 105
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    vmax = max([v for v in values if math.isfinite(v)] + [1e-12])
    bar_w = plot_w / max(1, len(values)) * 0.72
    gap = plot_w / max(1, len(values))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="18">{html.escape(title)}</text>',
        f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t+plot_h}" stroke="black"/>',
        f'<line x1="{margin_l}" y1="{margin_t+plot_h}" x2="{margin_l+plot_w}" y2="{margin_t+plot_h}" stroke="black"/>',
        f'<text x="18" y="{margin_t+plot_h/2}" transform="rotate(-90 18,{margin_t+plot_h/2})" font-family="Arial" font-size="13">{html.escape(ylabel)}</text>',
    ]
    for i in range(6):
        y = margin_t + plot_h * (1 - i / 5)
        val = vmax * i / 5
        parts.append(f'<line x1="{margin_l-4}" y1="{y:.1f}" x2="{margin_l+plot_w}" y2="{y:.1f}" stroke="#ddd"/>')
        parts.append(f'<text x="{margin_l-8}" y="{y+4:.1f}" text-anchor="end" font-family="Arial" font-size="11">{val:.2g}</text>')
    for idx, (label, value) in enumerate(zip(labels, values)):
        x = margin_l + idx * gap + (gap - bar_w) / 2
        h = 0.0 if not math.isfinite(value) else plot_h * value / vmax
        y = margin_t + plot_h - h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="#6f89b9"/>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{y-5:.1f}" text-anchor="middle" font-family="Arial" font-size="10">{value:.2g}</text>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{margin_t+plot_h+16}" transform="rotate(45 {x+bar_w/2:.1f},{margin_t+plot_h+16})" font-family="Arial" font-size="11">{html.escape(label)}</text>')
    parts.append('</svg>')
    path.write_text('\n'.join(parts), encoding='utf-8')


def write_line_svg(path: Path, xs: list[float], ys: list[float], title: str, xlabel: str, ylabel: str) -> None:
    width, height = 780, 420
    ml, mr, mt, mb = 80, 35, 55, 70
    pw, ph = width - ml - mr, height - mt - mb
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    if abs(xmax - xmin) < 1e-30:
        xmax = xmin + 1.0
    if abs(ymax - ymin) < 1e-30:
        ymax = ymin + 1.0
    def sx(x): return ml + pw * (x - xmin) / (xmax - xmin)
    def sy(y): return mt + ph * (1 - (y - ymin) / (ymax - ymin))
    pts = ' '.join(f'{sx(x):.1f},{sy(y):.1f}' for x, y in zip(xs, ys))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="18">{html.escape(title)}</text>',
        f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="black"/>',
        f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="black"/>',
        f'<polyline points="{pts}" fill="none" stroke="#6f89b9" stroke-width="3"/>',
    ]
    for x, y in zip(xs, ys):
        parts.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4" fill="#334e7d"/>')
    parts += [
        f'<text x="{ml+pw/2}" y="{height-20}" text-anchor="middle" font-family="Arial" font-size="13">{html.escape(xlabel)}</text>',
        f'<text x="18" y="{mt+ph/2}" transform="rotate(-90 18,{mt+ph/2})" font-family="Arial" font-size="13">{html.escape(ylabel)}</text>',
        f'<text x="{ml}" y="{mt+ph+20}" text-anchor="middle" font-family="Arial" font-size="11">{xmin:.2g}</text>',
        f'<text x="{ml+pw}" y="{mt+ph+20}" text-anchor="middle" font-family="Arial" font-size="11">{xmax:.2g}</text>',
        f'<text x="{ml-8}" y="{sy(ymin)+4:.1f}" text-anchor="end" font-family="Arial" font-size="11">{ymin:.2g}</text>',
        f'<text x="{ml-8}" y="{sy(ymax)+4:.1f}" text-anchor="end" font-family="Arial" font-size="11">{ymax:.2g}</text>',
        '</svg>',
    ]
    path.write_text('\n'.join(parts), encoding='utf-8')
