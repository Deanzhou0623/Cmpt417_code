#!/usr/bin/env python3
from cbs import CBSSolver
from run_experiments import import_mapf_instance

instances = ['instances/exp0.txt', 'instances/exp1.txt', 'instances/exp2_1.txt', 'instances/exp4.txt']

print("="*70)
print("QUICK TEST: CBS vs CBS with Disjoint Splitting")
print("="*70)

for inst in instances:
    print(f"\n{inst}:")
    print("-"*70)

    my_map, starts, goals = import_mapf_instance(inst)

    # Standard
    cbs1 = CBSSolver(my_map, starts, goals)
    paths1 = cbs1.find_solution(disjoint=False)
    cost1 = sum(len(p)-1 for p in paths1)

    # Disjoint
    cbs2 = CBSSolver(my_map, starts, goals)
    paths2 = cbs2.find_solution(disjoint=True)
    cost2 = sum(len(p)-1 for p in paths2)

    status = "✅" if cost1 == cost2 else "❌"
    improvement = cbs1.num_of_expanded - cbs2.num_of_expanded

    print(f"  Standard: {cbs1.num_of_expanded:3d} expanded | Disjoint: {cbs2.num_of_expanded:3d} expanded | Improvement: {improvement:+3d}")
    print(f"  Cost: {cost1} vs {cost2} {status}")

print("\n" + "="*70)
