from graph import Graph
from topological_sort import topological_sort
from prim import prim

print("=" * 40)
print("   1. Topological Sort")
print("=" * 40)

g1 = Graph(8)
g1.add_edge_directed(7, 6)
g1.add_edge_directed(7, 5)
g1.add_edge_directed(6, 4)
g1.add_edge_directed(6, 3)
g1.add_edge_directed(5, 4)
g1.add_edge_directed(5, 2)
g1.add_edge_directed(3, 2)
g1.add_edge_directed(4, 1)
g1.add_edge_directed(2, 1)
g1.add_edge_directed(1, 0)

result = topological_sort(g1)
print("Result:", result)

print()
print("=" * 40)
print("   2. Prim's Algorithm (MST)")
print("=" * 40)

g2 = Graph(9)
g2.add_edge_undirected(0, 1, 4)
g2.add_edge_undirected(0, 7, 8)
g2.add_edge_undirected(1, 2, 8)
g2.add_edge_undirected(1, 7, 11)
g2.add_edge_undirected(2, 3, 7)
g2.add_edge_undirected(2, 5, 4)
g2.add_edge_undirected(2, 8, 2)
g2.add_edge_undirected(3, 4, 9)
g2.add_edge_undirected(3, 5, 14)
g2.add_edge_undirected(4, 5, 10)
g2.add_edge_undirected(5, 6, 2)
g2.add_edge_undirected(6, 7, 1)
g2.add_edge_undirected(6, 8, 6)
g2.add_edge_undirected(7, 8, 7)

edges, weight = prim(g2, 0)
print("MST Edges:")
for u, v, w in edges:
    print(f"  {u} -- {v}  weight: {w}")
print(f"Total Weight: {weight}")
