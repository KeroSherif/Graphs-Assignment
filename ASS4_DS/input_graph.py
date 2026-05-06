from graph import Graph
from topological_sort import topological_sort, count_topological_orderings
from prim import prim
from visualize import draw_directed_graph, draw_mst_comparison


def has_path(graph, src, dst):
    """Check if there is a directed path from src to dst using DFS."""
    if src == dst:
        return True
    visited = set()
    stack = [src]
    while stack:
        node = stack.pop()
        if node == dst:
            return True
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.adj[node]:
            # Handle both weighted (tuple) and unweighted edges
            n = neighbor[0] if isinstance(neighbor, tuple) else neighbor
            if n not in visited:
                stack.append(n)
    return False


def get_graph_from_user():
    # Choose node type
    print("Do you want to use numbers or letters for nodes? (n/l)")
    node_type = input(">>> ").strip().lower()
    while node_type not in ['n', 'l']:
        print("Invalid! Please enter 'n' for numbers or 'l' for letters.")
        node_type = input(">>> ").strip().lower()

    print("\nHow many nodes?")
    count = int(input(">>> "))

    if node_type == 'n':
        print("Enter your node numbers separated by spaces (example: 1 5 10 20)")
        while True:
            raw = input(">>> ").strip().split()
            if len(raw) != count:
                print(f"Error: you need exactly {count} numbers, try again.")
                continue
            try:
                nums = [int(x) for x in raw]
            except ValueError:
                print("Error: all values must be integers, try again.")
                continue
            if len(set(nums)) != len(nums):
                print("Error: numbers must be unique (no duplicates), try again.")
                continue
            nodes = nums
            break
        print(f"\nYour nodes are: {nodes}")
    else:
        print("Enter your node names separated by spaces (example: a b c d)")
        while True:
            raw = input(">>> ").strip().split()
            if len(raw) != count:
                print(f"Error: you need exactly {count} node names, try again.")
                continue
            if len(set(raw)) != len(raw):
                print("Error: names must be unique (no duplicates), try again.")
                continue
            nodes = raw
            break
        print(f"\nYour nodes are: {nodes}")

    print("\nDirected or Undirected graph? (d/u)")
    graph_type = input(">>> ").strip().lower()
    while graph_type not in ['d', 'u']:
        print("Invalid! Please enter 'd' or 'u' only.")
        graph_type = input(">>> ").strip().lower()

    if graph_type == 'd':
        print("\n-> Topological Sort will be used (Directed graph)")
        print("   Note: MST is not available for Directed graphs")
    else:
        print("\n-> Prim's MST will be used (Undirected graph)")
        print("   Note: Topological Sort is not available for Undirected graphs")

    g = Graph(nodes)

    print("\nEnter edges (type 'done' when finished)")

    if graph_type == 'd':
        print(f"Format: u v  (example: {nodes[0]} {nodes[1] if len(nodes) > 1 else nodes[0]})")
        while True:
            edge = input(">>> ").strip()
            if edge == 'done':
                break
            try:
                parts = edge.split()
                u, v = parts[0], parts[1]
                if node_type == 'n':
                    u, v = int(u), int(v)
                if u not in nodes or v not in nodes:
                    print(f"Error: nodes must be from {nodes}, try again.")
                    continue
                if u == v:
                    print(f"Error: a node cannot point to itself ({u} -> {v}), try again.")
                    continue
                # Check if this exact edge already exists
                if v in g.adj[u]:
                    print(f"Error: edge {u} -> {v} already exists, try again.")
                    continue
                # Check if reverse edge exists (would make it bidirectional)
                if u in g.adj[v]:
                    print(f"Error: edge {v} -> {u} already exists, adding {u} -> {v} would make it bidirectional, try again.")
                    continue
                # Check if adding this edge creates a cycle
                # (i.e. there is already a path from v back to u)
                if has_path(g, v, u):
                    print(f"Error: adding {u} -> {v} would create a cycle (path {v} -> ... -> {u} already exists), try again.")
                    continue
                g.add_edge_directed(u, v)
            except:
                print(f"Invalid format! Use: u v  (example: {nodes[0]} {nodes[1] if len(nodes) > 1 else nodes[0]})")

        print("\n=== Topological Sort Steps ===")
        result = topological_sort(g, verbose=True)
        print("\nFinal Topological Sort:", result)

        # Count the number of valid topological orderings
        total_orderings, _ = count_topological_orderings(g, verbose=True)

        sort_text = ' -> '.join(map(str, result))
        header = f"Topological Sort: {sort_text}\nValid Topological Orderings: {total_orderings}"
        draw_directed_graph(
            g.to_dict(),
            title="Topological Sort Result",
            header_text=header
        )

    else:
        print(f"Format: u v weight  (example: {nodes[0]} {nodes[1] if len(nodes) > 1 else nodes[0]} 4)")
        while True:
            edge = input(">>> ").strip()
            if edge == 'done':
                break
            try:
                parts = edge.split()
                u, v, w = parts[0], parts[1], int(parts[2])
                if node_type == 'n':
                    u, v = int(u), int(v)
                if u not in nodes or v not in nodes:
                    print(f"Error: nodes must be from {nodes}, try again.")
                    continue
                if u == v:
                    print(f"Error: a node cannot connect to itself ({u} -- {v}), try again.")
                    continue
                # Check if this edge already exists (in either direction)
                existing_neighbors = [n[0] for n in g.adj[u]]
                if v in existing_neighbors:
                    print(f"Error: edge {u} -- {v} already exists, try again.")
                    continue
                g.add_edge_undirected(u, v, w)
            except:
                print(f"Invalid format! Use: u v weight  (example: {nodes[0]} {nodes[1] if len(nodes) > 1 else nodes[0]} 4)")

        print("\nStart from which node?")
        start = input(">>> ").strip()
        if node_type == 'n':
            start = int(start)

        print("\n=== Prim's Algorithm Steps ===")
        edges, weight = prim(g, start, verbose=True)
        print("\nFinal MST Edges:")
        for u, v, w in edges:
            print(f"  {u} -- {v}  weight: {w}")
        print(f"Total Weight: {weight}")
        mst_text = "  |  ".join([f"{u}-{v}({w})" for u, v, w in edges])
        draw_mst_comparison(
            g.to_dict(),
            edges,
            title="Prim's MST Result",
            header_text=f"MST (Total Weight: {weight}):  {mst_text}"
        )


get_graph_from_user()
