#!/usr/bin/env python3
from single_agent_planner import a_star, compute_heuristics
from cbs import CBSSolver, disjoint_splitting
from visualize import Animation
from independent import IndependentSolver

# Simple 2-agent test case
my_map = [
    [True, True, True, True, True, True, True],
    [True, False, False, False, False, False, True],
    [True, False, False, False, False, False, True],
    [True, False, False, False, False, False, True],
    [True, False, False, False, False, False, True],
    [True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True]
]

starts = [(2, 1), (1, 2)]
goals = [(3, 5), (4, 4)]

print("Testing CBS with disjoint splitting...")
print("Starts:", starts)
print("Goals:", goals)

cbs = CBSSolver(my_map, starts, goals)
print("\n=== Running with disjoint=True ===")
try:
    paths = cbs.find_solution(disjoint=True)
    print("Solution found!")
    print("Paths:", paths)
except Exception as e:
    print("Error:", e)
