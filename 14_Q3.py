from itertools import combinations

def neg(v):
    return v[1:] if v.startswith("~") else f"~{v}"

def clause_text(clause):
    return " v ".join(sorted(clause, key=lambda v: v.strip("~"))) if clause else "{}"

def has_opposite(clause):
    # any() short-circuits and returns True the moment it finds a match
    return any(neg(v) in clause for v in clause)

def resolve(c1, c2):
    answers = []
    for v in c1:
        if neg(v) in c2:
            # Union (|) combines the sets, Difference (-) removes the resolved literals
            new_clause = (c1 | c2) - {v, neg(v)}
            
            if not has_opposite(new_clause):
                answers.append(frozenset(new_clause))
    return answers

def resolution(name, clauses, goal):
    print(f"{name}\nClauses")
    
    # Initialize the Knowledge Base (kb) as a set of frozensets, adding the negated goal
    kb = {frozenset(c) for c in clauses} | {frozenset([neg(goal)])}
    
    for c in kb:
        print(clause_text(c))
        
    print("Resolving")

    while True:
        new_clauses = set()
        
        # combinations() safely grabs every unique pair of clauses without nested index loops
        for c1, c2 in combinations(kb, 2):
            for res in resolve(c1, c2):
                if not res:  # An empty frozenset means a contradiction was found
                    print(f"Empty clause\nConclusion: {goal} is proved\n")
                    return
                new_clauses.add(res)
        
        # Find strictly new clauses using set difference
        added = new_clauses - kb 
        
        if not added:
            print(f"No contradiction\nConclusion: {goal} is not proved\n")
            return
            
        for c in added:
            print(clause_text(c))
            
        kb |= added  # Update the knowledge base with the new clauses

clauses_a = [["P", "Q"], ["~P", "R"], ["~Q", "S"], ["~R", "S"]]
clauses_b = [["~P", "Q"], ["~Q", "R"], ["~S", "~R"], ["P"]]

resolution("a", clauses_a, "S")
resolution("b", clauses_b, "S")