#!/usr/bin/env python3
"""Test CBS with and without disjoint splitting on all instances"""

from cbs import CBSSolver
from run_experiments import import_mapf_instance
import glob

instances = [
    'instances/exp0.txt',
    'instances/exp1.txt',
    'instances/exp2_1.txt',
    'instances/exp2_2.txt',
    'instances/exp2_3.txt',
    'instances/exp4.txt',
]

print("="*80)
print("TESTING CBS VS CBS WITH DISJOINT SPLITTING ON ALL INSTANCES")
print("="*80)

results = []

for instance_file in instances:
    print(f"\n{'='*80}")
    print(f"Instance: {instance_file}")
    print(f"{'='*80}")

    try:
        my_map, starts, goals = import_mapf_instance(instance_file)
        print(f"Agents: {len(starts)}")

        # Standard CBS
        print("\n--- Standard CBS ---")
        cbs_standard = CBSSolver(my_map, starts, goals)
        paths_standard = cbs_standard.find_solution(disjoint=False)
        expanded_standard = cbs_standard.num_of_expanded
        generated_standard = cbs_standard.num_of_generated
        cost_standard = sum(len(p) - 1 for p in paths_standard)

        print(f"\n--- CBS with Disjoint Splitting ---")
        cbs_disjoint = CBSSolver(my_map, starts, goals)
        paths_disjoint = cbs_disjoint.find_solution(disjoint=True)
        expanded_disjoint = cbs_disjoint.num_of_expanded
        generated_disjoint = cbs_disjoint.num_of_generated
        cost_disjoint = sum(len(p) - 1 for p in paths_disjoint)

        # Verify optimality
        if cost_standard != cost_disjoint:
            status = "❌ COST MISMATCH"
        else:
            status = "✅ OPTIMAL"

        improvement = expanded_standard - expanded_disjoint
        improvement_pct = (improvement / expanded_standard * 100) if expanded_standard > 0 else 0

        result = {
            'instance': instance_file.split('/')[-1],
            'standard_expanded': expanded_standard,
            'disjoint_expanded': expanded_disjoint,
            'standard_generated': generated_standard,
            'disjoint_generated': generated_disjoint,
            'cost': cost_standard,
            'status': status,
            'improvement': improvement,
            'improvement_pct': improvement_pct
        }
        results.append(result)

        print(f"\n{'='*80}")
        print(f"RESULTS:")
        print(f"  Standard CBS:  {expanded_standard:3d} expanded, {generated_standard:3d} generated, cost={cost_standard}")
        print(f"  Disjoint CBS:  {expanded_disjoint:3d} expanded, {generated_disjoint:3d} generated, cost={cost_disjoint}")
        print(f"  Improvement:   {improvement:+3d} nodes ({improvement_pct:+.1f}%)")
        print(f"  Status:        {status}")
        print(f"{'='*80}")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        results.append({
            'instance': instance_file.split('/')[-1],
            'status': f"❌ ERROR: {e}"
        })

print("\n\n")
print("="*80)
print("SUMMARY TABLE")
print("="*80)
print(f"{'Instance':<15} {'Standard':<10} {'Disjoint':<10} {'Improvement':<12} {'Cost':<6} {'Status':<15}")
print("-"*80)

for r in results:
    if 'standard_expanded' in r:
        print(f"{r['instance']:<15} {r['standard_expanded']:>9d} {r['disjoint_expanded']:>9d} {r['improvement']:>+6d} ({r['improvement_pct']:>+5.1f}%) {r['cost']:>5d} {r['status']:<15}")
    else:
        print(f"{r['instance']:<15} {r['status']}")

print("="*80)

# Check for exp4.txt specifically
exp4_results = [r for r in results if 'exp4' in r['instance']]
if exp4_results:
    r = exp4_results[0]
    if 'standard_expanded' in r:
        print(f"\nexp4.txt VERIFICATION (as per assignment):")
        print(f"  Assignment expectation: ~11 nodes for standard, ~8 for disjoint")
        print(f"  Your implementation:    {r['standard_expanded']} nodes for standard, {r['disjoint_expanded']} for disjoint")
        if r['disjoint_expanded'] < r['standard_expanded']:
            print(f"  ✅ Disjoint splitting successfully reduced node expansions!")
        if '✅' in r['status']:
            print(f"  ✅ Both algorithms found optimal solution!")
