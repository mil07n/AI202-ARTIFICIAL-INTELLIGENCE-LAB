# 0 = hallway, 1 = wall/room
grid = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1]]
START, GOAL = (4, 1), (1, 5)

def h(r, c): 
    return abs(r - GOAL[0]) + abs(c - GOAL[1])

frontier = [(START[0], START[1], 0, None)]
reached = {START: 0}
path_map = {}

while frontier:
    frontier.sort(key=lambda x: x[2] + h(x[0], x[1]))
    r, c, g, parent = frontier.pop(0)

    if (r, c) == GOAL:
        print(f"Evacuation complete! Total steps: {g}")
        break

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0:
            new_g = g + 1
            if (nr, nc) not in reached or new_g < reached[(nr, nc)]:
                reached[(nr, nc)] = new_g
                path_map[(nr, nc)] = (r, c)
                frontier.append((nr, nc, new_g, (r, c)))

curr = GOAL
full_path = []
while curr in path_map:
    full_path.append(curr)
    curr = path_map[curr]
full_path.append(START)
print("Path:", full_path[::-1])