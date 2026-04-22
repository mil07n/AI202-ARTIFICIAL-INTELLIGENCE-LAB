from collections import deque

variables = ["P1", "P2", "P3", "P4", "P5", "P6"]

# Domains: P1 is fixed to R1, others can be any room.
domains = {
    "P1": {"R1"},
    "P2": {"R1", "R2", "R3"},
    "P3": {"R1", "R2", "R3"},
    "P4": {"R1", "R2", "R3"},
    "P5": {"R1", "R2", "R3"},
    "P6": {"R1", "R2", "R3"}
}

# Neighbors: Projects that cannot share the same room.
neighbors = {
    "P1": ["P2", "P3", "P6"],
    "P2": ["P1", "P3", "P4"],
    "P3": ["P1", "P2", "P5"],
    "P4": ["P2", "P6"],
    "P5": ["P3", "P6"],
    "P6": ["P1", "P4", "P5"]
}

# Reduces domain of xi based on constraint: Xi != Xj
def revise(domains, xi, xj):
    # Remove values from xi that lack a different valid value in xj
    to_remove = {x for x in domains[xi] if not any(x != y for y in domains[xj])}
    
    if to_remove:
        domains[xi] -= to_remove
        return True, to_remove
    return False, set()

# AC-3 algorithm ensures arc consistency across all nodes
def ac3(domains):
    queue = deque([(xi, xj) for xi in variables for xj in neighbors[xi]])
    trace = []

    while queue:
        xi, xj = queue.popleft()
        revised, removed = revise(domains, xi, xj)

        # Record only the first 5 steps to keep output concise
        if len(trace) < 5:
            if revised:
                trace.append(f"Arc ({xi},{xj}) checked -> removed {sorted(list(removed))} from {xi}, domain = {sorted(list(domains[xi]))}")
            else:
                trace.append(f"Arc ({xi},{xj}) checked -> no change")

        # If a domain empties, the problem has no solution
        if not domains[xi]:
            return False, trace, domains

        # Re-evaluate neighbors if xi's domain changed
        if revised:
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))

    return True, trace, domains

# Print initial state
print("Initial Domains:")
for var in variables:
    print(f"{var}: {sorted(list(domains[var]))}")

consistent, trace, final_domains = ac3