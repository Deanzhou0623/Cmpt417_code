#!/usr/bin/env python3
"""
Task 5: Comprehensive MAPF Solver Benchmarking Script

This script benchmarks three MAPF solvers (Independent, Prioritized, CBS)
on diverse benchmark instances and generates performance comparison graphs.
"""

import argparse
import glob
import time
import csv
import os
from pathlib import Path
from single_agent_planner import get_sum_of_cost
from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver

# Timeout in seconds for each solver run
TIMEOUT = 300  # 5 minutes


def import_mapf_instance(filename):
    """Import a MAPF instance from a file."""
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")

    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start/goal positions
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals


def run_solver_with_timeout(solver_class, my_map, starts, goals, timeout=TIMEOUT):
    """
    Run a solver with timeout and error handling.
    Returns (success, result, runtime, error_msg)
    """
    start_time = time.time()

    try:
        solver = solver_class(my_map, starts, goals)
        paths = solver.find_solution()
        runtime = time.time() - start_time

        if paths is None:
            return False, None, runtime, "No solution found"

        if runtime > timeout:
            return False, None, runtime, "Timeout"

        cost = get_sum_of_cost(paths)
        return True, {"paths": paths, "cost": cost}, runtime, None

    except Exception as e:
        runtime = time.time() - start_time
        return False, None, runtime, str(e)


def benchmark_instance(instance_file, solvers_config):
    """
    Benchmark all solvers on a single instance.
    Returns a dictionary with results for each solver.
    """
    print(f"\n{'='*80}")
    print(f"Benchmarking: {instance_file}")
    print(f"{'='*80}")

    # Load instance
    my_map, starts, goals = import_mapf_instance(instance_file)
    num_agents = len(starts)
    map_size = len(my_map) * len(my_map[0])

    print(f"Map size: {len(my_map)}x{len(my_map[0])}, Agents: {num_agents}")

    results = {
        "instance": os.path.basename(instance_file),
        "map_rows": len(my_map),
        "map_cols": len(my_map[0]),
        "map_size": map_size,
        "num_agents": num_agents,
    }

    # Run each solver
    for solver_name, solver_class in solvers_config.items():
        print(f"\nRunning {solver_name}...")
        success, result, runtime, error = run_solver_with_timeout(
            solver_class, my_map, starts, goals
        )

        if success:
            print(f"  ✓ Success! Cost: {result['cost']}, Time: {runtime:.3f}s")
            results[f"{solver_name}_success"] = True
            results[f"{solver_name}_cost"] = result['cost']
            results[f"{solver_name}_time"] = runtime
            results[f"{solver_name}_error"] = ""
        else:
            print(f"  ✗ Failed: {error}, Time: {runtime:.3f}s")
            results[f"{solver_name}_success"] = False
            results[f"{solver_name}_cost"] = None
            results[f"{solver_name}_time"] = runtime
            results[f"{solver_name}_error"] = error

    return results


def save_results_to_csv(results, output_file):
    """Save benchmark results to a CSV file."""
    if not results:
        print("No results to save.")
        return

    fieldnames = list(results[0].keys())

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"\n{'='*80}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}")


def generate_summary_report(results):
    """Generate a summary report of the benchmark results."""
    print(f"\n{'='*80}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*80}\n")

    solvers = ["Independent", "Prioritized", "CBS"]

    # Success rates
    print("Success Rates:")
    print("-" * 40)
    for solver in solvers:
        success_count = sum(1 for r in results if r.get(f"{solver}_success", False))
        total = len(results)
        rate = (success_count / total * 100) if total > 0 else 0
        print(f"  {solver:15s}: {success_count}/{total} ({rate:.1f}%)")

    # Average runtime (for successful runs)
    print("\nAverage Runtime (successful runs only):")
    print("-" * 40)
    for solver in solvers:
        times = [r[f"{solver}_time"] for r in results if r.get(f"{solver}_success", False)]
        avg_time = sum(times) / len(times) if times else 0
        print(f"  {solver:15s}: {avg_time:.3f}s ({len(times)} runs)")

    # Average cost (for successful runs)
    print("\nAverage Solution Cost (successful runs only):")
    print("-" * 40)
    for solver in solvers:
        costs = [r[f"{solver}_cost"] for r in results if r.get(f"{solver}_success", False) and r.get(f"{solver}_cost") is not None]
        avg_cost = sum(costs) / len(costs) if costs else 0
        print(f"  {solver:15s}: {avg_cost:.1f} ({len(costs)} runs)")

    print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(description='Benchmark MAPF solvers')
    parser.add_argument('--benchmark_dir', type=str, default='benchmarks',
                        help='Directory containing benchmark instances')
    parser.add_argument('--output', type=str, default='benchmark_results.csv',
                        help='Output CSV file for results')
    parser.add_argument('--pattern', type=str, default='*.txt',
                        help='File pattern to match benchmark instances')

    args = parser.parse_args()

    # Solver configuration
    solvers_config = {
        "Independent": IndependentSolver,
        "Prioritized": PrioritizedPlanningSolver,
        "CBS": CBSSolver,
    }

    # Find benchmark instances
    benchmark_pattern = os.path.join(args.benchmark_dir, args.pattern)
    instance_files = sorted(glob.glob(benchmark_pattern))

    if not instance_files:
        print(f"No benchmark instances found matching: {benchmark_pattern}")
        return

    print(f"\nFound {len(instance_files)} benchmark instances")
    print(f"Output will be saved to: {args.output}")

    # Run benchmarks
    all_results = []
    for instance_file in instance_files:
        result = benchmark_instance(instance_file, solvers_config)
        all_results.append(result)

    # Save results
    save_results_to_csv(all_results, args.output)

    # Generate summary
    generate_summary_report(all_results)


if __name__ == '__main__':
    main()
