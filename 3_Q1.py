import random

rooms = ["A", "B", "C"]
state = {r: random.choice(["Dirty", "Clean"]) for r in rooms}
location = random.choice(rooms)
rules = {
    ("Dirty", "A"): "Clean",
    ("Dirty", "B"): "Clean",
    ("Dirty", "C"): "Clean",
    ("Clean", "A"): "Right",
    ("Clean", "B"): "Right",
    ("Clean", "C"): "Left"
}
for step in range(10):
    percept = state[location]
    action = rules[(percept, location)]
    print(step, location, percept, action)

    if action == "Clean":
        state[location] = "Clean"
    elif action == "Right":
        location = rooms[(rooms.index(location)+1) % 3]
    elif action == "Left":
        location = rooms[(rooms.index(location)-1) % 3]