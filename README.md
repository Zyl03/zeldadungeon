# zeldadungeon
Interactive BFS dungeon visualizer built with Python and Pygame.  Shows pathfinding, frontier expansion, and shortest path in a Zelda-style dungeon.
source venv/bin/activate
git add .
git commit -m "Update code"
git push

deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate

python3 -m pip install pygbag
python3 -m pygbag main.py