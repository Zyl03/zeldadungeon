# Zelda Dungeon

An interactive Breadth-First Search (BFS) dungeon visualizer built with Python and Pygame.

The project demonstrates:

* BFS frontier expansion
* Visited node exploration
* Shortest path reconstruction
* Interactive player movement
* Zelda-inspired dungeon environment
* Visual overlays for frontier, visited cells, and final path

## Controls

| Key        | Action               |
| ---------- | -------------------- |
| Arrow Keys | Move player          |
| Space      | Run BFS animation    |
| P          | Toggle shortest path |
| R          | Reset dungeon        |

## Technologies

* Python
* Pygame
* BFS (Breadth-First Search)

## Project Structure

```text
zeldadungeon/
├── main.py
├── game/
│   ├── bfs.py
│   ├── render.py
│   ├── assets.py
├── image/
├── fonts/
└── README.md
```

## Setup

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install pygame pygbag
```

Run locally:

```bash
python main.py
```

Run with Pygbag:

```bash
python -m pygbag main.py
```

## Future Improvements

* A* pathfinding visualization
* Weighted terrain costs
* Multiple AI enemies
* Dynamic dungeon generation
* Pathfinding performance comparison
