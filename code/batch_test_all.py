#!/usr/bin/env python3
"""Batch test CBS with disjoint on all test instances and compare with min-sum-of-cost.csv"""

from cbs import CBSSolver
from run_experiments import import_mapf_instance
import signal
import sys

# Read expected costs
expected_costs = {}
with open('instances/min-sum-of-cost.csv', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            parts = line.split(',')
            if len(parts) == 2:
                expected_costs[parts[0]] = int(parts[1])

# Get all test instances
test_instances = sorted([k for k in expected_costs.keys() if 'test_' in k])

print("="*80)
print(f"TESTING CBS WITH DISJOINT SPLITTING ON {len(test_instances)} INSTANCES")
print("="*80)

passed = 0
failed = 0
timeout_count = 0

for i, instance in enumerate(test_instances, 1):
    instance_name = instance.split('/')[-1]
    expected = expected_costs[instance]

    print(f"\n[{i}/{len(test_instances)}] {instance_name}...", end=' ', flush=True)

    try:
        my_map, starts, goals = import_mapf_instance(instance)
        cbs = CBSSolver(my_map, starts, goals)

        # Run CBS with disjoint splitting
        paths = cbs.find_solution(disjoint=True)
        cost = sum(len(p) - 1 for p in paths)

        if cost == expected:
            print(f"✅ cost={cost}")
            passed += 1
        else:
            print(f"❌ cost={cost}, expected={expected}")
            failed += 1

    except KeyboardInterrupt:
        print(f"⏱️  TIMEOUT/INTERRUPTED")
        timeout_count += 1
        break
    except Exception as e:
        print(f"❌ ERROR: {e}")
        failed += 1

print("\n" + "="*80)
print(f"RESULTS: {passed} passed, {failed} failed, {timeout_count} timeout")
print(f"Success rate: {passed}/{len(test_instances)} ({100*passed/len(test_instances) if test_instances else 0:.1f}%)")
print("="*80)
