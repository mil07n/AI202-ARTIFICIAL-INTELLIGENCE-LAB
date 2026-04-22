import re
from itertools import product

# The logic rules and order of operations
OPS = {
    '~': lambda a, _: not a,          # NOT
    '^': lambda a, b: a and b,        # AND
    'v': lambda a, b: a or b,         # OR
    '->': lambda a, b: not a or b,    # IMPLIES
    '<->': lambda a, b: a == b        # IFF
}
PREC = {'~': 4, '^': 3, 'v': 2, '->': 1, '<->': 0}

def solve(expr, val_map):
    out, ops = [], []
    
    # 1. Translate equation and swap letters for True/False immediately
    for t in re.findall(r'<->|->|[PQR~^v()]', expr):
        if t in 'PQR': 
            out.append(val_map[t])  # Instantly inject True/False
        elif t == '(': 
            ops.append(t)
        elif t == ')':
            while ops[-1] != '(': out.append(ops.pop())
            ops.pop()
        else:
            # Handle order of operations
            while ops and ops[-1] != '(' and (PREC.get(ops[-1], -1) > PREC[t] or 
                 (PREC.get(ops[-1], -1) == PREC[t] and t not in {'~', '->', '<->'})):
                out.append(ops.pop())
            ops.append(t)
            
    postfix = out + ops

    # 2. Do the math
    stack = []
    for t in postfix:
        if isinstance(t, bool): stack.append(t)
        elif t == '~': stack.append(not stack.pop())
        else:
            b, a = stack.pop(), stack.pop()
            stack.append(OPS[t](a, b))
            
    return stack[0]

def print_truth_table(expr):
    # Find unique variables (P, Q, R)
    symbols = list(dict.fromkeys(re.findall(r'[PQR]', expr)))
    
    # Print the header
    print(f"\n{' | '.join(symbols)} | {expr}")
    print("-" * (len(symbols) * 4 + len(expr) + 3))

    # Generate every True/False combo and solve
    for vals in product([False, True], repeat=len(symbols)):
        val_map = dict(zip(symbols, vals))
        result = solve(expr, val_map)
        
        # Print the row cleanly
        row = ' | '.join('T' if val_map[s] else 'F' for s in symbols)
        print(f"{row} | {'T' if result else 'F'}")

# --- Main Execution ---
# Translated the mathematical ∧ to ^ and ∨ to v so the script can read them.
statements = [
    "~P->Q", 
    "~P^~Q", 
    "~Pv~Q", 
    "~P->~Q", 
    "~P<->~Q", 
    "(PvQ)^(~P->Q)", 
    "((PvQ)->~R)", 
    "(((PvQ)->~R)<->((~P^~Q)->~R))", 
    "(((P->Q)^(Q->R))->(Q->R))", 
    "(((P->(QvR))->(~P^~Q^~R)))"
]

for s in statements:
    print_truth_table(s)