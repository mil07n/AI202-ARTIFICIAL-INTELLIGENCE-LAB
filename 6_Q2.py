import heapq
from collections import deque

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def mst_cost(points):
    if not points:
        return 0
    pts = list(points)
    visited = {0}
    n = len(pts)
    dist = [float('inf')] * n
    for i in range(1, n):
        dist[i] = manhattan(pts[0], pts[i])
    total = 0
    while len(visited) < n:
        best = None
        best_d = float('inf')
        for i in range(n):
            if i in visited:
                continue
            if dist[i] < best_d:
                best_d = dist[i]
                best = i
        visited.add(best)
        total += best_d
        for j in range(n):
            if j in visited:
                continue
            d = manhattan(pts[best], pts[j])
            if d < dist[j]:
                dist[j] = d
    return total

def heuristic(pos, remaining):
    rem = list(remaining)
    if not rem:
        return 0
    d0 = min(manhattan(pos, r) for r in rem)
    mst = mst_cost(rem)
    return d0 + mst

def a_star_multi_reward(grid):
    rows = len(grid)
    cols = len(grid[0])

    start = None
    rewards = set()
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 2:
                start = (i, j)
            elif grid[i][j] == 3:
                rewards.add((i, j))

    start_state = (start[0], start[1], frozenset(rewards))

    counter = 0
    g_scores = {start_state: 0}
    parent = {start_state: None}
    action_from = {start_state: None}

    f0 = heuristic(start, rewards)
    frontier = [(f0, 0, counter, start_state)]
    nodes_expanded = 0
    nodes_generated = 0

    while frontier:
        f, g, _, state = heapq.heappop(frontier)
        nodes_expanded += 1
        x, y, rem = state
        rem = set(rem)
        if not rem:
            path = []
            cur = state
            while cur:
                path.append((cur[0], cur[1]))
                cur = parent[cur]
            path.reverse()
            visited_tiles = set(path)
            return {
                'path': path,
                'cost': g_scores[state],
                'nodes_expanded': nodes_expanded,
                'nodes_generated': nodes_generated,
                'visited_tiles': visited_tiles,
            }

        for dx, dy, act in [(-1,0,'U'), (1,0,'D'), (0,-1,'L'), (0,1,'R')]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < rows and 0 <= ny < cols):
                continue
            if grid[nx][ny] == 1:
                continue
            new_rem = set(rem)
            if (nx, ny) in new_rem:
                new_rem.remove((nx, ny))
            new_state = (nx, ny, frozenset(new_rem))
            tentative_g = g_scores[state] + 1
            nodes_generated += 1
            if new_state not in g_scores or tentative_g < g_scores[new_state]:
                g_scores[new_state] = tentative_g
                parent[new_state] = state
                action_from[new_state] = act
                f_new = tentative_g + heuristic((nx, ny), new_rem)
                counter += 1
                heapq.heappush(frontier, (f_new, tentative_g, counter, new_state))

    return None

if __name__ == "__main__":
    maze = [
        [2,0,0,0,1],
        [0,1,0,0,3],
        [0,0,3,1,1],
        [0,1,0,0,1],
        [3,0,0,0,3],
    ]
    print("Running A* to collect all rewards on sample 5x5 maze...")
    res = a_star_multi_reward(maze)
    if res is None:
        print("No path found to collect all rewards")
    else:
        print("Path length (steps):", len(res['path'])-1)
        print("Total cost:", res['cost'])
        print("Nodes expanded:", res['nodes_expanded'])
        print("Nodes generated:", res['nodes_generated'])
        print("Visited tiles on the way:", sorted(list(res['visited_tiles'])))
        print("Path (positions):")
        print(res['path'])
