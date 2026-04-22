from collections import deque

graph = {
    "Syracuse": {"Buffalo": 150, "New York": 254, "Boston": 312},
    "Buffalo": {"Detroit": 256, "Cleveland": 189, "Pittsburgh": 215},
    "Detroit": {"Chicago": 283},
    "Cleveland": {"Chicago": 345, "Detroit": 169, "Columbus": 144},
    "Columbus": {"Indianapolis": 176, "Pittsburgh": 185},
    "Indianapolis": {"Chicago": 182},
    "Pittsburgh": {"Philadelphia": 305},
    "Philadelphia": {"New York": 97},
    "New York": {"Boston": 215},
    "Boston": {},
    "Chicago": {}
}

# BFS
def bfs_all_paths(start, goal, graph):
    queue = deque([(start, [start], 0)])
    all_paths = []
    while queue:
        node, path, cost = queue.popleft()
        if node == goal:
            all_paths.append((path, cost))
            continue
        for neighbor, edge_cost in graph[node].items():
            if neighbor not in path:
                new_cost = cost + edge_cost
                queue.append((neighbor, path + [neighbor], new_cost))
    return all_paths

# DFS  
def dfs_all_paths(start, goal, graph):
    all_paths = []
    def dfs(node, path, cost):
        if node == goal:
            all_paths.append((path, cost))
            return
        for neighbor, edge_cost in graph[node].items():
            if neighbor not in path:
                new_cost = cost + edge_cost
                dfs(neighbor, path + [neighbor], new_cost)
    dfs(start, [start], 0)
    return all_paths

# prints
print("BFS - All paths from Syracuse to Chicago:")
for path, cost in bfs_all_paths("Syracuse", "Chicago", graph):
    print(" -> ".join(path), "| Cost:", cost)

print("\nDFS - All paths from Syracuse to Chicago:") 
for path, cost in dfs_all_paths("Syracuse", "Chicago", graph):
    print(" -> ".join(path), "| Cost:", cost)