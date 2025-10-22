#!/usr/bin/env python3
"""Verify CBS with disjoint splitting produces optimal costs"""

from cbs import CBSSolver
from run_experiments import import_mapf_instance

# Test a subset of instances
test_instances = [
    'instances/test_2.txt',
    'instances/test_6.txt',
    'instances/test_9.txt',
    'instances/test_10.txt',
    'instances/test_12.txt',
]

# Expected costs from min-sum-of-cost.csv
expected_costs = {
    'instances/test_2.txt': 18,
    'instances/test_6.txt': 24,
    'instances/test_9.txt': 24,
    'instances/test_10.txt': 19,
    'instances/test_12.txt': 36,
}

print("="*70)
print("VERIFYING CBS WITH DISJOINT SPLITTING ON TEST INSTANCES")
print("="*70)

all_passed = True

for instance in test_instances:
    print(f"\n{instance}:")
    my_map, starts, goals = import_mapf_instance(instance)

    cbs = CBSSolver(my_map, starts, goals)
    paths = cbs.find_solution(disjoint=True)
    cost = sum(len(p) - 1 for p in paths)
    expected = expected_costs[instance]

    status = "✅" if cost == expected else "❌"
    print(f"  Cost: {cost}, Expected: {expected} {status}")

    if cost != expected:
        all_passed = False

print("\n" + "="*70)
if all_passed:
    print("✅ ALL TESTS PASSED - All costs match optimal values!")
else:
    print("❌ SOME TESTS FAILED - Costs do not match expected values")
print("="*70)
