import math

distance = [
[0, 283, 345, 0, 182, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[283, 0, 0, 0, 0, 256, 0, 0, 0, 0, 0, 0, 0, 0],
[345, 0, 0, 144, 0, 189, 133, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 144, 0, 176, 0, 185, 0, 0, 0, 0, 0, 0, 0],
[182, 0, 0, 176, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 256, 189, 0, 0, 0, 0, 150, 0, 0, 0, 0, 0, 0],
[0, 0, 133, 185, 0, 0, 0, 0, 0, 305, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 150, 0, 0, 248, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 248, 0, 101, 0, 215, 181, 0],
[0, 0, 0, 0, 0, 0, 305, 0, 101, 0, 101, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 101, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 215, 0, 0, 0, 50, 107],
[0, 0, 0, 0, 0, 0, 0, 0, 181, 0, 0, 50, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 107, 0, 0]
]

States = {
    0: "Chicago", 1: "Detroit", 2: "Cleveland", 3: "Columbus", 4: "Indianapolis",
    5: "Buffalo", 6: "Pittsburgh", 7: "Syracuse", 8: "New York", 9: "Philadelphia",
    10: "Baltimore", 11: "Boston", 12: "Providence", 13: "Portland"
}

START = 0
GOAL = 11

minimax_nodes = 0
alphabeta_nodes = 0

def neighbors(city):
    return [(i, distance[city][i]) for i in range(len(distance)) if distance[city][i] > 0]

# MINIMAX — explores every possible path, no pruning
def minimax(city, visited, depth=0):
    global minimax_nodes
    minimax_nodes += 1

    if city == GOAL:
        return 0, [city]

    visited.add(city)
    best_cost = float('inf')
    best_path = []

    for nxt, cost in neighbors(city):
        if nxt not in visited:
            val, path = minimax(nxt, visited.copy(), depth + 1)
            if val != float('inf') and cost + val < best_cost:
                best_cost = cost + val
                best_path = [city] + path

    return best_cost, best_path


# ALPHA-BETA — same as minimax but prunes paths that can't beat current best
def alphabeta(city, visited, bound, depth=0):
    global alphabeta_nodes
    alphabeta_nodes += 1

    if city == GOAL:
        return 0, [city]

    visited.add(city)
    best_cost = float('inf')
    best_path = []

    for nxt, cost in neighbors(city):
        if nxt not in visited:
            val, path = alphabeta(nxt, visited.copy(), best_cost, depth + 1)

            if val != float('inf') and cost + val < best_cost:
                best_cost = cost + val
                best_path = [city] + path

            # PRUNE: if this path already costs more than the bound, stop exploring
            if best_cost >= bound:
                break

    return best_cost, best_path

# Run both from START
print("Finding path from", States[START], "to", States[GOAL])
print("=" * 50)

mm_cost, mm_path = minimax(START, set())
ab_cost, ab_path = alphabeta(START, set(), float('inf'))

print("\nMinimax Path:")
print(" -> ".join(States[i] for i in mm_path))
print("Cost:", mm_cost)
print("Nodes Explored:", minimax_nodes)

print("\nAlpha-Beta Path:")
print(" -> ".join(States[i] for i in ab_path))
print("Cost:", ab_cost)
print("Nodes Explored:", alphabeta_nodes)

print("\nEfficiency Gain:")
saved = minimax_nodes - alphabeta_nodes
reduction = (saved / minimax_nodes) * 100
print(f"Nodes Saved: {saved}")
print(f"Reduction: {reduction:.2f}%")