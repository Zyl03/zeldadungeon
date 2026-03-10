from collections import deque
import time
import json

# Reprsents walls ,S is Start, E is End and . is the road
# The index of 2D array starts from zero

grid = [
list("#########################"),
list("#S..#..F..#...#M....#...#"),
list("###.#.###.#.#.#.###.#.#.#"),
list("#...#...#...#...#...#.#.#"),
list("#.#####.#####.###.###.#.#"),
list("#..~..#.....#...#.....#.#"),
list("#.###.#####.###.#####.#.#"),
list("#.#...#..F#...M.....#...#"),
list("#.#.###.#.###.#.###.###.#"),
list("#.#.....#.....#.#.~.#...#"),
list("#.###########.#.#.###.#.#"),
list("#.....#.....#.#.#...#.#.#"),
list("###.#.#.###.#.#.###.#.#.#"),
list("#...#...#...#.#...#...#.#"),
list("#.#####.#.###.###.#####.#"),
list("#..M..#.#...#...#..F..#.#"),
list("#.###.#.###.###.#####.#.#"),
list("#.#...#...#.~...#...#...#"),
list("#.#.#####.#######.#.###.#"),
list("#.#..~..#.....#...#...#.#"),
list("#.#####.#####.#.#####.#M#"),
list("#..F..#.....#.#.....#.#.#"),
list("#.###.#####.#.###.#.#.#.#"),
list("#...#.....#.....#...#..E#"),
list("#########################"),
]

# Using dictionary/map and queue
visited= set()
parent = {}
queue = deque()
path = deque()
queue_snap = deque()

# The length of 2D array will tell us how many elements in the array
# 2D array's element can be list array, etc..
# print(len(grid))


# Define Function
def breadth_first_search(row, column, steps):
    snapshots = []

    visited.clear()
    parent.clear()
    queue.clear()

    queue.append((row, column, steps))
    visited.add((row, column))

    # Frame 0: just the start node
    snapshots.append({
        "current": (row, column),
        "visited": {(row, column)},
        "frontier": [(row, column)]
    })

    expanded = 0
    queue_max = len(queue)
    queue_snap = deque()
    directions = [(-1,0), (0,-1), (1,0), (0,1)]
    terrain = {'.', 'E', 'F', 'M', '~', 'S'}

    while len(queue) != 0:
        row, column, steps = queue.popleft()

        if grid[row][column] == 'E':
            return steps, queue_max, expanded, queue_snap, snapshots

        expanded += 1

        for (dy, dx) in directions:
            new_row, new_column = row + dy, column + dx

            if 0 <= new_row < len(grid) and 0 <= new_column < len(grid[0]) and \
               grid[new_row][new_column] in terrain and \
               (new_row, new_column) not in visited:

                visited.add((new_row, new_column))
                parent[(new_row, new_column)] = (row, column)
                queue.append((new_row, new_column, steps + 1))

                if len(queue) > queue_max:
                    queue_snap = queue.copy()
                    queue_max = len(queue)

        # Frame after expanding this node
        snapshots.append({
            "current": (row, column),
            "visited": set(visited),
            "frontier": [(r, c) for (r, c, _) in queue]
        })

    return -1, queue_max, expanded, queue_snap, snapshots
def path_finding(end):
    temp = end
    path.append(end)
    for keys,value in parent.items():
        if keys == temp:
            path_finding(value)
    return 0

# While not include the length, the for loop just loop through the element in 2D array
# For grid is just the list
# We need the range for number since number is not iterable.

def finding_start_end():  
    for row in range(len(grid)):
    # This mean that we are iterating through the rows of element
        for column in range(len(grid[row])):
        # Finding the starting point
            if grid[row][column] == "S":
                start = (row,column)
                queue.append((row,column,0))
                steps, queue_max, expanded_amount, frontier, snapshots = breadth_first_search(row,column,0)
                frontier = [node[:2] for node in frontier]
                frontier_file = open("frontier.json", "w")
                json.dump(list(frontier), frontier_file)
                frontier_file.close()
                print("Steps, Queue_max, Amount of Expanded Point, Frontier:",steps,queue_max,expanded_amount,frontier)
            elif grid[row][column] == "E":
                end = [(row,column)]
    print("Start at:",start)
    print("End at:",end)
    path_finding(end[0])

#Info
finding_start_end()


path.reverse()
print("The Shortest Path:", path)

file = open("path.json", "w")
expanded_file = open("expanded.json", "w")

json.dump(list(path), file)
json.dump(list(visited), expanded_file)

file.close()
print()



