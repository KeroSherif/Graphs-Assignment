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

## Recommended imports

```python
from graph import Graph
```
