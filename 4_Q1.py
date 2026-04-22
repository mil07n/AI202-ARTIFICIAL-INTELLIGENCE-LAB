graph = [
    ("Chicago", "Detroit", 283),
    ("Chicago", "Cleveland", 345),
    ("Chicago", "Indianapolis", 182),
    ("Detroit", "Cleveland", 169),
    ("Detroit", "Buffalo", 256),
    ("Cleveland", "Pittsburgh", 134),
    ("Cleveland", "Columbus", 144),
    ("Cleveland", "Buffalo", 189),
    ("Indianapolis", "Columbus", 176),
    ("Pittsburgh", "Philadelphia", 305),
    ("Pittsburgh", "Baltimore", 247),
    ("Pittsburgh", "Buffalo", 215),
    ("Columbus", "Pittsburgh", 185),
    ("Buffalo", "Syracuse", 150),
    ("Syracuse", "New York", 254),
    ("Syracuse", "Boston", 312),
    ("Syracuse", "Philadelphia", 253),
    ("New York", "Philadelphia", 97),
    ("New York", "Boston", 215),
    ("New York", "Providence", 181),
    ("Philadelphia", "Baltimore", 101),
    ("Boston", "Providence", 50),
    ("Boston", "Portland", 107),
]

class PriorityQueue:
    def __init__(self):
        self.items = []
    def push(self, item, priority):
        self.items.append((priority, item))
    def pop(self):
        min_index = 0
        for i in range(1, len(self.items)):
            if self.items[i][0] < self.items[min_index][0]:
                min_index = i
        priority, item = self.items[min_index]
        self.items.pop(min_index)
        return item
    def is_empty(self):
        return len(self.items) == 0
    
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

def uniform_cost_search(start, goal, graph):
    node = Node(start)
    frontier = PriorityQueue()
    frontier.push(node, node.path_cost)
    explored = set()
    while not frontier.is_empty():
        node = frontier.pop()
        if node.state == goal:
            return solution(node)
        explored.add(node.state)
        for child in expand(node, graph):
            if child.state not in explored and not any(n.state == child.state for _, n in frontier.items):
                frontier.push(child, child.path_cost)
    return None,None

def expand(node, graph):
    children = []
    for (city1, city2, cost) in graph:
        if city1 == node.state:
            children.append(Node(city2, node, city2, node.path_cost + cost))
        elif city2 == node.state:
            children.append(Node(city1, node, city1, node.path_cost + cost))
    return children

def solution(node):
    path = []
    total_cost = node.path_cost
    while node.parent is not None:
        path.append(node.state)
        node = node.parent
    path.append(node.state)  # add start state
    path.reverse()
    return path, total_cost

start_city = "Syracuse"
goal_city = "Chicago"

path, cost = uniform_cost_search(start_city, goal_city, graph)
if path is None:
    print("No path found between", start_city, "and", goal_city)
else:
    print("Path from", start_city, "to", goal_city, ":", path)
    print("Total cost:", cost)