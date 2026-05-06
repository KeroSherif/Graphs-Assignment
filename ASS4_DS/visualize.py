import tkinter as tk
import math
import random


def _build_node_list(graph_dict):
    """Collect all nodes (keys + neighbors)."""
    nodes = set(graph_dict.keys())
    for u in graph_dict:
        for edge in graph_dict[u]:
            v = edge[0] if isinstance(edge, tuple) else edge
            nodes.add(v)
    return list(nodes)


def _build_edge_list(graph_dict, directed):
    """Return a list of unique (u, v) edges (ignoring weights)."""
    edges = set()
    for u in graph_dict:
        for edge in graph_dict[u]:
            v = edge[0] if isinstance(edge, tuple) else edge
            if directed:
                edges.add((u, v))
            else:
                # canonical order so undirected edges aren't duplicated
                key = (u, v) if str(u) < str(v) else (v, u)
                edges.add(key)
    return list(edges)


def get_dynamic_layout(nodes, width, height, top_offset=60,
                      edges=None, iterations=400, seed=42):
    """
    Force-directed layout (Fruchterman-Reingold style).
    - Connected nodes attract each other.
    - All nodes repel each other.
    - After many iterations, nodes spread out nicely with minimal edge crossings.
    """
    nodes_list = list(nodes)
    n = len(nodes_list)
    if n == 0:
        return {}
    if n == 1:
        return {nodes_list[0]: (width / 2, top_offset + (height - top_offset) / 2)}

    # Margin so nodes don't touch the edge of the canvas
    margin = 80
    drawable_w = width - 2 * margin
    drawable_h = (height - top_offset) - 2 * margin
    area = drawable_w * drawable_h
    # Ideal edge length
    k = math.sqrt(area / n)

    # Initial positions: deterministic random spread
    rng = random.Random(seed)
    pos = {}
    for node in nodes_list:
        x = margin + rng.random() * drawable_w
        y = top_offset + margin + rng.random() * drawable_h
        pos[node] = [x, y]

    edges = edges or []
    # Initial "temperature" controls max movement per iteration
    t = drawable_w / 8.0
    cooling = t / iterations

    for _ in range(iterations):
        disp = {node: [0.0, 0.0] for node in nodes_list}

        # Repulsive forces between every pair
        for i in range(n):
            for j in range(i + 1, n):
                u, v = nodes_list[i], nodes_list[j]
                dx = pos[u][0] - pos[v][0]
                dy = pos[u][1] - pos[v][1]
                dist = math.sqrt(dx * dx + dy * dy) + 0.01
                force = (k * k) / dist
                fx = (dx / dist) * force
                fy = (dy / dist) * force
                disp[u][0] += fx
                disp[u][1] += fy
                disp[v][0] -= fx
                disp[v][1] -= fy

        # Attractive forces along edges
        for u, v in edges:
            if u not in pos or v not in pos:
                continue
            dx = pos[u][0] - pos[v][0]
            dy = pos[u][1] - pos[v][1]
            dist = math.sqrt(dx * dx + dy * dy) + 0.01
            force = (dist * dist) / k
            fx = (dx / dist) * force
            fy = (dy / dist) * force
            disp[u][0] -= fx
            disp[u][1] -= fy
            disp[v][0] += fx
            disp[v][1] += fy

        # Apply displacement, capped by current temperature
        for node in nodes_list:
            dx, dy = disp[node]
            d = math.sqrt(dx * dx + dy * dy) + 0.01
            move = min(d, t)
            pos[node][0] += (dx / d) * move
            pos[node][1] += (dy / d) * move

            # Keep inside the drawable box
            pos[node][0] = max(margin, min(width - margin, pos[node][0]))
            pos[node][1] = max(top_offset + margin,
                               min(height - margin, pos[node][1]))

        t = max(0.1, t - cooling)

    return {node: (pos[node][0], pos[node][1]) for node in nodes_list}


def render_window(graph_dict, graph_type='directed', mst_edges=None,
                  title="Graph Visualization", header_text=None):
    root = tk.Tk()
    root.title(title)

    canvas_width = 900
    canvas_height = 650
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Draw the header above the graph
    header_height = 0
    if header_text:
        line_count = header_text.count("\n") + 1
        header_height = max(60, 30 + line_count * 22)
        canvas.create_rectangle(0, 0, canvas_width, header_height,
                                fill="#f0f4ff", outline="")
        canvas.create_text(canvas_width / 2, header_height / 2, text=header_text,
                           font=("Arial", 13, "bold"), fill="#1a3a8a",
                           justify="center")

    nodes = _build_node_list(graph_dict)
    directed = (graph_type == 'directed')
    edges_for_layout = _build_edge_list(graph_dict, directed)

    pos = get_dynamic_layout(nodes, canvas_width, canvas_height,
                             top_offset=header_height,
                             edges=edges_for_layout)
    r = 25

    mst_set = set()
    if mst_edges:
        for u, v, w in mst_edges:
            key = (u, v) if str(u) < str(v) else (v, u)
            mst_set.add(key)

    # Track label positions to avoid overlap
    placed_labels = []

    # Draw edges
    drawn_undirected = set()
    for u in graph_dict:
        for edge in graph_dict[u]:
            v = edge[0] if isinstance(edge, tuple) else edge
            w = edge[1] if isinstance(edge, tuple) else ""

            # For undirected, only draw each edge once
            if not directed:
                key = (u, v) if str(u) < str(v) else (v, u)
                if key in drawn_undirected:
                    continue
                drawn_undirected.add(key)

            x1, y1 = pos[u]
            x2, y2 = pos[v]

            angle = math.atan2(y2 - y1, x2 - x1)
            start_x = x1 + r * math.cos(angle)
            start_y = y1 + r * math.sin(angle)
            end_x = x2 - r * math.cos(angle)
            end_y = y2 - r * math.sin(angle)

            color = "black"
            width = 2

            if not directed:
                key = (u, v) if str(u) < str(v) else (v, u)
                if mst_edges and key in mst_set:
                    color = "red"
                    width = 4
                elif mst_edges:
                    color = "#cccccc"
                canvas.create_line(start_x, start_y, end_x, end_y,
                                   fill=color, width=width)
            else:
                canvas.create_line(start_x, start_y, end_x, end_y,
                                   arrow=tk.LAST, arrowshape=(15, 20, 8),
                                   fill=color, width=width)

            # Place weight label perpendicular to the edge so it doesn't sit on the line
            if w != "":
                mx = (start_x + end_x) / 2
                my = (start_y + end_y) / 2
                # Perpendicular offset (15 pixels off the line)
                offset = 15
                perp_x = -math.sin(angle) * offset
                perp_y = math.cos(angle) * offset
                lx, ly = mx + perp_x, my + perp_y

                # Try to nudge if it overlaps an existing label
                for px, py in placed_labels:
                    if abs(lx - px) < 25 and abs(ly - py) < 18:
                        lx += offset
                        ly -= offset
                        break
                placed_labels.append((lx, ly))

                # White background behind label so it's readable over edges
                canvas.create_rectangle(lx - 12, ly - 9, lx + 12, ly + 9,
                                        fill="white", outline="")
                canvas.create_text(lx, ly, text=str(w), fill="blue",
                                   font=("Arial", 11, "bold"))

    # Draw nodes on top so edges go behind them
    for node, (x, y) in pos.items():
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           fill="lightblue", outline="darkblue", width=2)
        canvas.create_text(x, y, text=str(node), font=("Arial", 12, "bold"))

    root.mainloop()


def draw_directed_graph(graph_dict, title="Directed Graph",
                        in_degrees=None, header_text=None):
    render_window(graph_dict, 'directed', title=title, header_text=header_text)


def draw_undirected_weighted_graph(graph_dict, title="Undirected Weighted Graph",
                                   header_text=None):
    render_window(graph_dict, 'undirected', title=title, header_text=header_text)


def draw_mst_comparison(graph_dict, mst_edges, title="Minimum Spanning Tree",
                        header_text=None):
    render_window(graph_dict, 'undirected', mst_edges,
                  title=title, header_text=header_text)
