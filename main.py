from __future__ import annotations

import argparse

from graph import Graph
from prim import prim
from topological_sort import topological_sort


def run_topo_example() -> None:
    g = Graph(8)
    edges = [
        (7, 6),
        (7, 5),
        (5, 2),
        (5, 4),
        (6, 4),
        (6, 3),
        (3, 2),
        (3, 1),
        (4, 0),
        (2, 0),
        (1, 0),
    ]
    for u, v in edges:
        g.add_directed_edge(u, v)

    order = topological_sort(g)
    if not order:
        print("Cycle detected — topological sort not possible")
    else:
        print("Topological Order:", order)


def run_prim_example() -> None:
    g = Graph(9)
    weighted_edges = [
        (0, 1, 4),
        (0, 7, 8),
        (1, 2, 8),
        (1, 7, 11),
        (2, 3, 7),
        (2, 5, 4),
        (2, 8, 2),
        (3, 4, 9),
        (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1),
        (6, 8, 6),
        (7, 8, 7),
    ]
    for u, v, w in weighted_edges:
        g.add_undirected_weighted_edge(u, v, w)

    edges, weight = prim(g, 0)
    print("MST Edges:", edges)
    print("Total Weight:", weight)


def main() -> None:
    parser = argparse.ArgumentParser(description="Graphs Assignment runner")
    parser.add_argument(
        "--algo",
        choices=["topo", "prim", "both"],
        default="both",
        help="Which lab example to run",
    )
    args = parser.parse_args()

    if args.algo in ("topo", "both"):
        run_topo_example()

    if args.algo == "both":
        print()

    if args.algo in ("prim", "both"):
        run_prim_example()


if __name__ == "__main__":
    main()
