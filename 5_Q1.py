TOTAL_G = 3
TOTAL_B = 3
MOVES = [(1,0),(2,0),(0,1),(0,2),(1,1)]

def valid_state(g_left, b_left):
    g_right = TOTAL_G - g_left
    b_right = TOTAL_B - b_left
    if g_left < 0 or b_left < 0 or g_left > TOTAL_G or b_left > TOTAL_B:
        return False
    if g_left > 0 and b_left > g_left:
        return False
    if g_right > 0 and b_right > g_right:
        return False
    return True

def successors(state):
    g_left, b_left, boat = state
    next_states = []
    for g, b in MOVES:
        if boat == 0:
            new_state = (g_left - g, b_left - b, 1)
        else:
            new_state = (g_left + g, b_left + b, 0)
        if valid_state(new_state[0], new_state[1]):
            next_states.append(new_state)
    return next_states

def dls(state, goal, depth, path, visited):
    if state == goal:
        return path
    if depth == 0:
        return None
    for next_state in successors(state):
        if next_state not in visited:
            visited.add(next_state)
            result = dls(next_state, goal, depth-1,
            path + [next_state], visited)
            if result:
                return result
            visited.remove(next_state)
    return None

def run_ids(start_limit):
    start = (3,3,0)
    goal = (0,0,1)
    depth = start_limit
    while True:
        result = dls(start, goal, depth, [start], {start})
        if result:
            return result, depth
        depth += 1   # increase depth automatically

result, depth = run_ids(3)

print("Solution Path:")
for step in result:
    print(step)
print("Solution Depth:", depth)