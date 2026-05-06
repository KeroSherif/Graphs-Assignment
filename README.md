# Graphs Assignment

This repo is organized as a few top-level Python files so Member 2 (Topological Sort) and Member 3 (Prim's MST) can depend on the same `Graph` foundation.

## Layout

- `graph.py` — Member 1: graph data structure + parsing helpers
- `topological_sort.py` — Member 2: topological sort (Kahn's algorithm)
- `prim.py` — Member 3: Prim's MST
- `main.py` — runs the lab examples

## Run tests

```bash
python -m py_compile graph.py topological_sort.py prim.py
```

## Run

```bash
python main.py
```

## Visualization (PNG)

This project exports images (PNG) for the example graphs by default when you run `main.py`.

```bash
python main.py
```

This writes `topo.png` and `prim.png`.

To disable image generation:

```bash
python main.py --viz none
```

## Recommended imports

```python
from graph import Graph
```
