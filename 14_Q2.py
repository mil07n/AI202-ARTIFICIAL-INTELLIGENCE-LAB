def backward_chaining(goal, facts, rules, checked=None):
    if checked is None:
        checked = set()

    if goal in facts:
        print(f"{goal} is a fact")
        return True

    if goal in checked:
        return False

    checked.add(goal)

    for conditions, result in rules:
        if result == goal:
            print(f"To prove {goal}")
            
            # all() evaluates the generator and stops early if any condition returns False
            if all(backward_chaining(cond, facts, rules, checked) for cond in conditions):
                print(f"{goal} is proved")
                return True

    return False

def solve(name, facts, rules, goal):
    print(name)
    # Convert facts to a set once for O(1) lookups during recursion
    status = "true" if backward_chaining(goal, set(facts), rules) else "false"
    print(f"Conclusion: {goal} is {status}\n")


rules_a = [(["P"], "Q"), (["R"], "Q"), (["A"], "P"), (["B"], "R")]
facts_a = ["A", "B"]

rules_b = [(["A"], "B"), (["B", "C"], "D"), (["E"], "C")]
facts_b = ["A", "E"]

solve("a", facts_a, rules_a, "Q")
solve("b", facts_b, rules_b, "D")