from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Set, Tuple

from graph import Graph


def _escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def directed_to_dot(graph: Graph, *, title: Optional[str] = None) -> str:
    """Return a Graphviz DOT representation for a directed, unweighted graph."""
    lines: List[str] = ["digraph G {"]
    lines.append("  rankdir=LR;")
    if title:
        lines.append(f"  labelloc=\"t\";")
        lines.append(f"  label=\"{_escape(title)}\";")

    for v in range(graph.num_vertices):
        lines.append(f"  {v};")

    for u in range(graph.num_vertices):
        for v in graph.adj[u]:
            lines.append(f"  {u} -> {v};")

    lines.append("}")
    return "\n".join(lines) + "\n"


def undirected_weighted_to_dot(
    graph: Graph,
    *,
    title: Optional[str] = None,
    highlight_edges: Optional[Iterable[Tuple[int, int, int]]] = None,
) -> str:
    """Return a Graphviz DOT representation for an undirected weighted graph.

    `highlight_edges` is an iterable of (u, v, weight) edges to emphasize (e.g., MST edges).
    """

    highlight: Set[Tuple[int, int, int]] = set()
    if highlight_edges is not None:
        for u, v, w in highlight_edges:
            a, b = (u, v) if u <= v else (v, u)
            highlight.add((a, b, w))

    lines: List[str] = ["graph G {"]
    lines.append("  rankdir=LR;")
    if title:
        lines.append("  labelloc=\"t\";")
        lines.append(f"  label=\"{_escape(title)}\";")

    for v in range(graph.num_vertices):
        lines.append(f"  {v};")

    seen: Set[Tuple[int, int, int]] = set()
    for u in range(graph.num_vertices):
        for w, v in graph.adj[u]:
            a, b = (u, v) if u <= v else (v, u)
            key = (a, b, w)
            if key in seen:
                continue
            seen.add(key)

            attrs: List[str] = [f'label="{w}"']
            if key in highlight:
                attrs.append('color="red"')
                attrs.append("penwidth=3")

            lines.append(f"  {a} -- {b} [{', '.join(attrs)}];")

    lines.append("}")
    return "\n".join(lines) + "\n"


def render_directed_png(
    graph: Graph,
    *,
    out_path: str,
    title: Optional[str] = None,
    order: Optional[List[int]] = None,
) -> str:
    """Render a directed graph to a PNG image.

    If `order` is provided, nodes are laid out left-to-right in that order.
    """

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx

    g = nx.DiGraph()
    g.add_nodes_from(range(graph.num_vertices))
    for u in range(graph.num_vertices):
        for v in graph.adj[u]:
            g.add_edge(u, v)

    if order:
        pos = {node: (i, 0) for i, node in enumerate(order)}
        for node in range(graph.num_vertices):
            pos.setdefault(node, (node, 0))
    else:
        pos = nx.spring_layout(g, seed=7)

    fig = plt.figure(figsize=(10, 2.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.axis("off")
    if title:
        ax.set_title(title)

    nx.draw_networkx_nodes(g, pos, node_size=900, ax=ax)
    nx.draw_networkx_labels(g, pos, font_size=10, ax=ax)
    nx.draw_networkx_edges(g, pos, arrows=True, arrowstyle="-|>", arrowsize=18, ax=ax)

    out = Path(out_path)
    fig.tight_layout()
    fig.savefig(out, format="png", dpi=200)
    plt.close(fig)
    return str(out)


def render_undirected_weighted_png(
    graph: Graph,
    *,
    out_path: str,
    title: Optional[str] = None,
    highlight_edges: Optional[Iterable[Tuple[int, int, int]]] = None,
) -> str:
    """Render an undirected weighted graph to a PNG image.

    `highlight_edges` (u, v, w) are drawn in red (useful for MST).
    """

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx

    g = nx.Graph()
    g.add_nodes_from(range(graph.num_vertices))

    # Add each undirected edge once.
    seen: Set[Tuple[int, int, int]] = set()
    for u in range(graph.num_vertices):
        for w, v in graph.adj[u]:
            a, b = (u, v) if u <= v else (v, u)
            key = (a, b, w)
            if key in seen:
                continue
            seen.add(key)
            g.add_edge(a, b, weight=w)

    pos = nx.spring_layout(g, seed=7)

    highlight: Set[Tuple[int, int, int]] = set()
    if highlight_edges is not None:
        for u, v, w in highlight_edges:
            a, b = (u, v) if u <= v else (v, u)
            highlight.add((a, b, w))

    mst_edges = []
    normal_edges = []
    for (u, v, data) in g.edges(data=True):
        w = int(data.get("weight"))
        key = (u, v, w) if u <= v else (v, u, w)
        if key in highlight:
            mst_edges.append((u, v))
        else:
            normal_edges.append((u, v))

    edge_labels = {(u, v): str(data.get("weight")) for u, v, data in g.edges(data=True)}

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.axis("off")
    if title:
        ax.set_title(title)

    nx.draw_networkx_nodes(g, pos, node_size=900, ax=ax)
    nx.draw_networkx_labels(g, pos, font_size=10, ax=ax)

    nx.draw_networkx_edges(g, pos, edgelist=normal_edges, width=1.5, ax=ax)
    if mst_edges:
        nx.draw_networkx_edges(g, pos, edgelist=mst_edges, width=3.5, edge_color="red", ax=ax)

    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=9, ax=ax)

    out = Path(out_path)
    fig.tight_layout()
    fig.savefig(out, format="png", dpi=200)
    plt.close(fig)
    return str(out)


if __name__ == "__main__":
    print(
        "visualize.py is a helper module. To generate images, run:\n"
        "  python main.py --viz both\n"
        "This will write topo.png and prim.png."
    )
