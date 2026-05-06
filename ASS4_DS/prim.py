import heapq
from graph import Graph

def prim(graph, start, verbose=False):
    visited = set()
    min_heap = [(0, start, -1)]
    mst_edges = []
    total_weight = 0

    if verbose:
        print(f"\n  Start from node {start}")

    while min_heap:
        weight, u, parent = heapq.heappop(min_heap)

        if u in visited:
            continue

        visited.add(u)
        total_weight += weight

        if parent != -1:
            if verbose:
                print(f"\n  Step: Add edge {parent} -- {u}  (weight: {weight})")
                print(f"        Total weight so far: {total_weight}")
            mst_edges.append((parent, u, weight))

        for v, w in graph.adj[u]:
            if v not in visited:
                if verbose:
                    print(f"    -> Checking edge {u} -- {v}  (weight: {w})")
                heapq.heappush(min_heap, (w, v, u))

    return mst_edges, total_weight
