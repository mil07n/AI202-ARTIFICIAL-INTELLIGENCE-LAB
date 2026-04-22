def forward_chaining(facts, rules, goal):
    known = set(facts)
    
    while True:
        start_len = len(known)
        for conditions, result in rules:
            # Check if all conditions are in 'known' using set subset (<=)
            if set(conditions) <= known and result not in known:
                known.add(result)
                print(result)
                if result == goal: 
                    return True, known
                
        # If no new facts were added in this pass, exit the loop
        if len(known) == start_len: 
            break
            
    return goal in known, known

def solve(name, facts, rules, goal):
    print(f"{name}\nFacts: {', '.join(facts)}")
    
    found, known = forward_chaining(facts, rules, goal)
    
    status = "proved" if found else "not proved"
    print(f"{goal} is {status}")
    print(f"Final facts: {', '.join(sorted(known))}\n")


rules_a = [(["P"], "Q"), (["L", "M"], "P"), (["A", "B"], "L")]
facts_a = ["A", "B", "M"]

rules_b = [(["A"], "B"), (["B"], "C"), (["C"], "D"), (["D", "E"], "F")]
facts_b = ["A", "E"]

solve("a", facts_a, rules_a, "Q")
solve("b", facts_b, rules_b, "F")