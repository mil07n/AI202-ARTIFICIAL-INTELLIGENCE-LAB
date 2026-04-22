from collections import deque

grid = [
    [0, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 5, 9, 0, 0, 0, 0, 0, 8],
    [2, 0, 0, 0, 0, 8, 0, 0, 0],
    [0, 4, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 3, 0, 5, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 2]
]

TOTAL = 81

def idx(r, c):
    return r * 9 + c

# Build neighbors: cells sharing row, col, or 3x3 box
neighbors = [set() for _ in range(TOTAL)]
for r in range(9):
    for c in range(9):
        i = idx(r, c)
        for r2 in range(9):
            for c2 in range(9):
                j = idx(r2, c2)
                if i != j and (r == r2 or c == c2 or (r//3 == r2//3 and c//3 == c2//3)):
                    neighbors[i].add(j)

def make_domains():
    return [{grid[r][c]} if grid[r][c] != 0 else set(range(1, 10))
            for r in range(9) for c in range(9)]

# AC-3: prune domains using arc consistency
def ac3(domains):
    queue = deque((i, j) for i in range(TOTAL) for j in neighbors[i])
    while queue:
        xi, xj = queue.popleft()
        # Only prune if xj is a singleton
        if len(domains[xj]) == 1:
            val = next(iter(domains[xj]))
            if val in domains[xi]:
                domains[xi].discard(val)
                # If a domain becomes empty, it's an impossible puzzle
                if not domains[xi]:
                    return False   
                for xk in neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
    return True

# --- Main Execution ---
domains = make_domains()
consistent = ac3(domains)

print("Sudoku Solver — AC-3 Only")
print("-" * 40)

# Check the state of the domains after AC-3 finishes
if not consistent:
    print("Result: No solution found (Contradiction detected by AC-3).")
else:
    # Check if every square has exactly 1 pencil mark left
    is_solved = all(len(d) == 1 for d in domains)
    
    if is_solved:
        print("Result: Solved completely using only AC-3!\n")
    else:
        print("Result: AC-3 pruned the space, but Backtracking IS REQUIRED to fully solve.\n")
    
    # Print the resulting grid
    print("Remaining Domain Size Grid (or solved value if singleton):")
    for r in range(9):
        row_out = []
        for c in range(9):
            i = idx(r, c)
            if len(domains[i]) == 1:
                row_out.append(f" {next(iter(domains[i]))} ")
            else:
                row_out.append(f"({len(domains[i])})")
        print(" ".join(row_out))