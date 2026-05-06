from collections import deque
from math import factorial
from graph import Graph


def count_topological_orderings(graph, verbose=False):
    """
    Count the number of valid topological orderings using the
    'simultaneously-free groups' method:
      - Whenever k nodes become free (indegree=0) at the same time,
        they can be arranged in k! ways.
      - Multiply k! across all groups.
    Returns a tuple: (total_count, groups) where groups is a list of dicts.
    """
    # Build a mutable copy of in-degrees
    in_degree = {node: graph.get_in_degree(node) for node in graph.nodes}

    groups = []
    group_num = 1

    # Group 1: all nodes that are free from the start
    current_free = [node for node in graph.nodes if in_degree[node] == 0]

    while current_free:
        groups.append({
            "group": group_num,
            "nodes": list(current_free),
            "count": factorial(len(current_free)),
            "reason": _describe_group(group_num, groups)
        })

        # Process all currently-free nodes "simultaneously" and find the next batch
        next_free = []
        for u in current_free:
            for neighbor in graph.adj[u]:
                v = neighbor[0] if isinstance(neighbor, tuple) else neighbor
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    next_free.append(v)

        current_free = next_free
        group_num += 1

    # Multiply factorials together
    total = 1
    for g in groups:
        total *= g["count"]

    if verbose:
        _print_groups_table(groups, total)

    return total, groups


def _describe_group(group_num, previous_groups):
    if group_num == 1:
        return "All sources from the start"
    elif group_num == 2:
        return "Both free after Group 1 finishes"
    else:
        return f"All free after Group {group_num - 1} finishes"


def _print_groups_table(groups, total):
    print("\n  " + "=" * 70)
    print("  Number of Valid Topological Orderings")
    print("  " + "=" * 70)
    print(f"  {'Group':<7}{'Nodes':<22}{'Why free together':<32}{'Count'}")
    print("  " + "-" * 70)
    for g in groups:
        nodes_str = "(" + ", ".join(map(str, g["nodes"])) + ")"
        count_str = f"{len(g['nodes'])}! = {g['count']}"
        print(f"  {g['group']:<7}{nodes_str:<22}{g['reason']:<32}{count_str}")
    print("  " + "-" * 70)

    # Build the multiplication string
    parts = [f"{len(g['nodes'])}!" for g in groups]
    values = [str(g['count']) for g in groups]
    print(f"  Calculation: {' x '.join(parts)} = {' x '.join(values)} = {total}")
    print(f"  => {total} valid topological orderings")
    print("  " + "=" * 70)


def topological_sort(graph, verbose=False):
    """
    Kahn's Algorithm for Topological Sort.
    Repeatedly picks nodes with in-degree 0 and removes them from the graph,
    updating the in-degrees of their neighbors.
    """
    # Step 1: Compute initial in-degree for every node
    in_degree = {node: graph.get_in_degree(node) for node in graph.nodes}

    if verbose:
        print("\n  Step 1: Initial in-degrees")
        print("  " + "-" * 35)
        for node, deg in in_degree.items():
            print(f"    in-degree({node}) = {deg}")

    # Step 2: Put all nodes with in-degree 0 into the queue
    queue = deque([node for node in graph.nodes if in_degree[node] == 0])
    result = []

    if verbose:
        print(f"\n  Step 2: Nodes with in-degree 0 -> Queue: {list(queue)}")
        print("  " + "=" * 35)

    step = 1
    # Step 3: Process the queue
    while queue:
        u = queue.popleft()
        result.append(u)

        if verbose:
            print(f"\n  Step {step}: Pick node '{u}' (in-degree = 0)")
            print(f"    Result so far: {result}")
            print(f"    Remove '{u}' and update in-degrees of its neighbors:")

        # Decrease in-degree for each neighbor of u
        neighbors = graph.adj[u]
        if not neighbors and verbose:
            print(f"      (no outgoing edges from {u})")

        for neighbor in neighbors:
            v = neighbor[0] if isinstance(neighbor, tuple) else neighbor
            old_deg = in_degree[v]
            in_degree[v] -= 1
            new_deg = in_degree[v]

            if verbose:
                print(f"      in-degree({v}): {old_deg} -> {new_deg}")

            if in_degree[v] == 0:
                queue.append(v)
                if verbose:
                    print(f"        '{v}' now has in-degree 0 -> add to Queue")

        if verbose:
            print(f"    Queue: {list(queue)}")

        step += 1

    # Step 4: Check if a valid topological ordering was produced
    if len(result) != len(graph.nodes):
        if verbose:
            print("\n  Warning: graph contains a cycle, topological sort not possible!")
        return result

    if verbose:
        print("\n  " + "=" * 35)
        print(f"  Final Order: {' -> '.join(map(str, result))}")

    return result
