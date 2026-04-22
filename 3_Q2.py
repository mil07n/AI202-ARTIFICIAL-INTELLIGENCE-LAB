import random

perception = ["Train", "NoTrain"]
obstacles = ["None", "Stuck"]
manual = ["Neutral", "Active"]
rules = {
    ("Train", "None", "Neutral"): ("Lower", "On", "Green"),
    ("Train", "Stuck", "Neutral"): ("Lower", "On", "Red"),
    ("NoTrain", "None", "Neutral"): ("Raise", "Off", "Green"),
    ("NoTrain", "Stuck", "Neutral"): ("Raise", "On", "Red"),
    ("Train", "None", "Active"): ("Lower", "On", "Red"),
    ("Train", "Stuck", "Active"): ("Lower", "On", "Red"),
    ("NoTrain", "None", "Active"): ("Raise", "Off", "Red"),
    ("NoTrain", "Stuck", "Active"): ("Raise", "On", "Red")
}
for step in range(10):
    p = random.choice(perception)
    o = random.choice(obstacles)
    m = random.choice(manual)

    action = rules[(p, o, m)]
    print(step, p, o, m, action)