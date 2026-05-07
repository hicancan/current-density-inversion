"""Graph builder for E23 Graph-Hodge basis."""
from __future__ import annotations

import math
from typing import Any


def _resistance_proxy(
    width_um: float, length_mm: float,
    thickness_um: float = 2.0, conductivity_sm: float = 5.8e7
) -> float:
    """R = L / (sigma * A) where A = width * thickness."""
    width_m = width_um * 1e-6
    thickness_m = thickness_um * 1e-6
    length_m = length_mm * 1e-3
    area = width_m * thickness_m
    if area <= 0:
        return 1e12
    return length_m / (conductivity_sm * area)


def _edge_key(a: str, b: str) -> str:
    """Canonical edge key for undirected pairing."""
    return f"{a}__{b}" if a < b else f"{b}__{a}"


def _node_id(kind: str, name: str) -> str:
    """Standard node identifier."""
    return f"{kind}__{name}"


def _edge_id(kind: str, src: str, dst: str) -> str:
    """Standard edge identifier."""
    return f"{kind}__{src}__{dst}"


def _trace_junction_id(trace_name: str, idx: int) -> str:
    """Junction node id for a trace point."""
    return _node_id("junction", f"{trace_name}_p{idx}")


def _distance_mm(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def build_graph(parsed: dict[str, Any]) -> dict[str, Any]:
    """Build a graph dict with nodes and edges from parsed layout."""
    nodes: dict[str, dict] = {}
    edges: dict[str, dict] = {}

    stackup = parsed["stackup"]

    # Layer nodes
    for ly in parsed["layers"]:
        nid = _node_id("layer", ly["name"])
        nodes[nid] = {
            "id": nid, "kind": "layer", "layer": ly["name"],
            "thickness_um": ly["thickness_um"],
            "type": ly["type"],
        }

    # Port nodes
    for port in parsed["ports"]:
        nid = _node_id("port", port["name"])
        nodes[nid] = {
            "id": nid, "kind": "port", "layer": port["layer"],
            "position_mm": port["position_mm"], "net": port["net"],
            "role": port["role"],
        }

    # Trace edges and junction nodes
    for trace in parsed["traces"]:
        pts = trace["points_mm"]
        layer_info = stackup.get(trace["layer"], {})
        thickness = layer_info.get("thickness_um", 2.0)
        conductivity = layer_info.get("conductivity_sm", 5.8e7)

        for i in range(len(pts)):
            jid = _trace_junction_id(trace["name"], i)
            if jid not in nodes:
                nodes[jid] = {
                    "id": jid, "kind": "junction",
                    "layer": trace["layer"],
                    "position_mm": pts[i], "net": trace["net"],
                }

        for i in range(len(pts) - 1):
            src_jid = _trace_junction_id(trace["name"], i)
            dst_jid = _trace_junction_id(trace["name"], i + 1)
            length = _distance_mm(pts[i], pts[i + 1])
            r = _resistance_proxy(trace["width_um"], length, thickness, conductivity)
            eid = _edge_id("trace", src_jid, dst_jid)
            edges[eid] = {
                "id": eid, "kind": "trace", "src": src_jid, "dst": dst_jid,
                "layer": trace["layer"], "net": trace["net"],
                "width_um": trace["width_um"], "length_mm": length,
                "resistance_proxy": r,
                "src_pos": pts[i], "dst_pos": pts[i + 1],
                "src_z_um": layer_info.get("z_mid_um", 0.0),
                "dst_z_um": layer_info.get("z_mid_um", 0.0),
            }

    # Port-to-trace connections: connect port nodes to nearest trace junction
    for port in parsed["ports"]:
        port_nid = _node_id("port", port["name"])
        port_pos = port["position_mm"]
        best_jid = None
        best_dist = float("inf")
        for nid, nd in nodes.items():
            if nd.get("kind") == "junction" and nd.get("layer") == port["layer"] and nd.get("net") == port["net"]:
                d = _distance_mm(port_pos, nd["position_mm"])
                if d < best_dist:
                    best_dist = d
                    best_jid = nid
        if best_jid is not None:
            best_nd = nodes[best_jid]
            eid = _edge_id("port_link", port_nid, best_jid)
            z_val = stackup.get(port["layer"], {}).get("z_mid_um", 0.0)
            edges[eid] = {
                "id": eid, "kind": "port_link", "src": port_nid, "dst": best_jid,
                "layer": port["layer"], "net": port["net"],
                "width_um": 100.0, "length_mm": best_dist,
                "resistance_proxy": 0.001,
                "src_pos": port["position_mm"],
                "dst_pos": best_nd["position_mm"],
                "src_z_um": z_val, "dst_z_um": z_val,
            }

    # Via edges
    for via in parsed["vias"]:
        from_layer_info = stackup.get(via["from_layer"], {})
        to_layer_info = stackup.get(via["to_layer"], {})
        z_from = from_layer_info.get("z_mid_um", 0.0)
        z_to = to_layer_info.get("z_mid_um", 0.0)
        via_length_mm = abs(z_from - z_to) * 1e-3

        src_nid = _node_id("via_top", via["name"])
        dst_nid = _node_id("via_bot", via["name"])
        pos = via["position_mm"]

        nodes[src_nid] = {
            "id": src_nid, "kind": "via_endpoint",
            "layer": via["from_layer"], "position_mm": pos,
            "net": via.get("net", "VDD"), "z_um": z_from,
        }
        nodes[dst_nid] = {
            "id": dst_nid, "kind": "via_endpoint",
            "layer": via["to_layer"], "position_mm": pos,
            "net": via.get("net", "VDD"), "z_um": z_to,
        }
        eid = _edge_id("via", src_nid, dst_nid)
        edges[eid] = {
            "id": eid, "kind": "via_edge", "src": src_nid, "dst": dst_nid,
            "layer": via["from_layer"], "from_layer": via["from_layer"],
            "to_layer": via["to_layer"], "net": via.get("net", "VDD"),
            "width_um": 50.0, "length_mm": via_length_mm if via_length_mm > 0 else 0.01,
            "resistance_proxy": 0.001,
            "src_pos": pos, "dst_pos": pos,
            "src_z_um": z_from, "dst_z_um": z_to,
        }

        # Connect via endpoints to nearby trace junctions
        for vnid, layer, z_val in [(src_nid, via["from_layer"], z_from), (dst_nid, via["to_layer"], z_to)]:
            best_jid = None
            best_dist = float("inf")
            for nid, nd in nodes.items():
                if nd.get("kind") == "junction" and nd.get("layer") == layer:
                    d = _distance_mm(pos, nd["position_mm"])
                    if d < best_dist:
                        best_dist = d
                        best_jid = nid
            if best_jid is not None:
                layer_info = stackup.get(layer, {})
                thickness = layer_info.get("thickness_um", 2.0)
                conductivity = layer_info.get("conductivity_sm", 5.8e7)
                r = _resistance_proxy(50.0, best_dist, thickness, conductivity)
                leid = _edge_id("via_link", vnid, best_jid)
                edges[leid] = {
                    "id": leid, "kind": "via_link", "src": vnid, "dst": best_jid,
                    "layer": layer, "net": via.get("net", "VDD"),
                    "width_um": 50.0, "length_mm": best_dist,
                    "resistance_proxy": r,
                    "src_pos": pos, "dst_pos": nodes[best_jid]["position_mm"],
                    "src_z_um": z_val,
                    "dst_z_um": stackup.get(layer, {}).get("z_mid_um", 0.0),
                }

    # Return plane nodes and candidate edges
    for rp in parsed["return_planes"]:
        rp_nid = _node_id("return_plane", rp["name"])
        # Centroid of outline as position
        outline = rp.get("outline_mm", [])
        if outline:
            cx = sum(pt[0] for pt in outline) / len(outline)
            cy = sum(pt[1] for pt in outline) / len(outline)
            rp_pos = (cx, cy)
        else:
            rp_pos = (0.0, 0.0)
        nodes[rp_nid] = {
            "id": rp_nid, "kind": "return_plane",
            "layer": rp["layer"], "net": rp.get("net", "GND"),
            "position_mm": rp_pos,
        }

        # Connect return plane to all junction nodes on same layer
        for nid, nd in nodes.items():
            if nd.get("kind") == "junction" and nd.get("layer") == rp["layer"]:
                pos = nd["position_mm"]
                layer_info = stackup.get(rp["layer"], {})
                thickness = layer_info.get("thickness_um", 2.0)
                conductivity = layer_info.get("conductivity_sm", 5.8e7)
                length = 1.0  # nominal length for return candidate
                r = _resistance_proxy(200.0, length, thickness, conductivity)
                reid = _edge_id("return_candidate", rp_nid, nid)
                edges[reid] = {
                    "id": reid, "kind": "return_candidate",
                    "src": rp_nid, "dst": nid,
                    "layer": rp["layer"], "net": rp.get("net", "GND"),
                    "width_um": 200.0, "length_mm": length,
                    "resistance_proxy": r,
                }

        # Connect return plane to sink ports on same layer
        for port in parsed["ports"]:
            if port["layer"] == rp["layer"] and port["role"] == "sink":
                port_nid = _node_id("port", port["name"])
                reid = _edge_id("return_candidate", rp_nid, port_nid)
                edges[reid] = {
                    "id": reid, "kind": "return_candidate",
                    "src": rp_nid, "dst": port_nid,
                    "layer": rp["layer"], "net": rp.get("net", "GND"),
                    "width_um": 200.0, "length_mm": 0.5,
                    "resistance_proxy": 0.001,
                }

    # Post-process: fill in src_pos/dst_pos/src_z_um/dst_z_um for ALL edges
    for eid, ed in edges.items():
        if "src_pos" not in ed:
            src_nd = nodes.get(ed["src"], {})
            dst_nd = nodes.get(ed["dst"], {})
            ed["src_pos"] = src_nd.get("position_mm", (0.0, 0.0))
            ed["dst_pos"] = dst_nd.get("position_mm", (0.0, 0.0))
            layer = ed.get("layer", "")
            z_val = stackup.get(layer, {}).get("z_mid_um", 0.0)
            ed["src_z_um"] = src_nd.get("z_um", z_val)
            ed["dst_z_um"] = dst_nd.get("z_um", z_val)

    return {"nodes": nodes, "edges": edges}


def _adjacency(graph: dict[str, Any]) -> dict[str, set[str]]:
    """Build adjacency set from graph."""
    adj: dict[str, set[str]] = {nid: set() for nid in graph["nodes"]}
    for ed in graph["edges"].values():
        s, d = ed["src"], ed["dst"]
        if s in adj:
            adj[s].add(d)
        if d in adj:
            adj[d].add(s)
    return adj


def connected_components(graph: dict[str, Any]) -> list[set[str]]:
    """Find connected components via DFS."""
    adj = _adjacency(graph)
    visited: set[str] = set()
    components: list[set[str]] = []

    for nid in graph["nodes"]:
        if nid in visited:
            continue
        comp: set[str] = set()
        stack = [nid]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            comp.add(v)
            stack.extend(adj.get(v, set()) - visited)
        components.append(comp)

    return components


def graph_is_connected(graph: dict[str, Any]) -> bool:
    """Check if the graph has a single connected component."""
    return len(connected_components(graph)) == 1


def count_via_candidates(graph: dict[str, Any]) -> int:
    """Count via edges and via endpoint nodes."""
    via_nodes = sum(1 for nd in graph["nodes"].values() if nd["kind"] == "via_endpoint")
    via_edges = sum(1 for ed in graph["edges"].values() if ed["kind"] == "via_edge")
    return via_edges


def count_return_candidates(graph: dict[str, Any]) -> int:
    """Count return candidate edges."""
    return sum(1 for ed in graph["edges"].values() if ed["kind"] == "return_candidate")


def layer_preserved(graph: dict[str, Any]) -> set[str]:
    """Set of layer names found in the graph."""
    return {nd.get("layer", "") for nd in graph["nodes"].values() if nd.get("layer")}


def graph_summary(graph: dict[str, Any]) -> dict[str, Any]:
    """Compute summary statistics for a graph."""
    node_kinds: dict[str, int] = {}
    for nd in graph["nodes"].values():
        k = nd["kind"]
        node_kinds[k] = node_kinds.get(k, 0) + 1

    edge_kinds: dict[str, int] = {}
    for ed in graph["edges"].values():
        k = ed["kind"]
        edge_kinds[k] = edge_kinds.get(k, 0) + 1

    return {
        "node_count": len(graph["nodes"]),
        "edge_count": len(graph["edges"]),
        "node_kinds": node_kinds,
        "edge_kinds": edge_kinds,
        "layer_count": len(layer_preserved(graph)),
        "layers": sorted(layer_preserved(graph)),
        "via_candidate_count": count_via_candidates(graph),
        "return_candidate_count": count_return_candidates(graph),
        "is_connected": graph_is_connected(graph),
        "components": len(connected_components(graph)),
    }
