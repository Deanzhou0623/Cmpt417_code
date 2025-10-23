#!/usr/bin/env python3
"""
Generate graphs from benchmark results for Task 5 report.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def load_results(csv_file):
    """Load benchmark results from CSV file."""
    return pd.read_csv(csv_file)


def plot_success_rates(df, output_dir):
    """Plot success rates for each solver."""
    solvers = ["Independent", "Prioritized", "CBS"]
    success_counts = []
    failure_counts = []

    for solver in solvers:
        success = df[f"{solver}_success"].sum()
        failure = (~df[f"{solver}_success"]).sum()
        success_counts.append(success)
        failure_counts.append(failure)

    fig, ax = plt.subplots()
    x = range(len(solvers))
    width = 0.35

    bars1 = ax.bar([i - width/2 for i in x], success_counts, width,
                    label='Success', color='#2ecc71')
    bars2 = ax.bar([i + width/2 for i in x], failure_counts, width,
                    label='Failure', color='#e74c3c')

    ax.set_xlabel('Solver', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Instances', fontsize=12, fontweight='bold')
    ax.set_title('Solver Success vs Failure Rates', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(solvers)
    ax.legend()

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'success_rates.png'), dpi=300)
    print(f"Saved: {os.path.join(output_dir, 'success_rates.png')}")
    plt.close()


def plot_runtime_comparison(df, output_dir):
    """Plot runtime comparison for successful runs."""
    solvers = ["Independent", "Prioritized", "CBS"]

    # Prepare data for successful runs only
    runtime_data = []
    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True]
        for _, row in successful.iterrows():
            runtime_data.append({
                'Solver': solver,
                'Runtime (s)': row[f"{solver}_time"],
                'Num Agents': row['num_agents']
            })

    runtime_df = pd.DataFrame(runtime_data)

    if runtime_df.empty:
        print("No successful runs to plot runtime comparison.")
        return

    # Box plot
    fig, ax = plt.subplots()
    sns.boxplot(data=runtime_df, x='Solver', y='Runtime (s)', ax=ax)
    ax.set_title('Runtime Distribution by Solver (Successful Runs)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Solver', fontsize=12, fontweight='bold')
    ax.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'runtime_boxplot.png'), dpi=300)
    print(f"Saved: {os.path.join(output_dir, 'runtime_boxplot.png')}")
    plt.close()


def plot_runtime_vs_agents(df, output_dir):
    """Plot runtime vs number of agents with line chart."""
    solvers = ["Independent", "Prioritized", "CBS"]
    colors = {'Independent': '#3498db', 'Prioritized': '#e67e22', 'CBS': '#9b59b6'}
    markers = {'Independent': 'o', 'Prioritized': 's', 'CBS': '^'}

    fig, ax = plt.subplots(figsize=(12, 8))

    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True].copy()
        if not successful.empty:
            # Sort by number of agents for proper line plotting
            successful = successful.sort_values('num_agents')
            ax.plot(successful['num_agents'], successful[f"{solver}_time"],
                   label=solver, linewidth=2.5, marker=markers[solver],
                   markersize=10, color=colors[solver], alpha=0.8)

    ax.set_xlabel('Number of Agents', fontsize=14, fontweight='bold')
    ax.set_ylabel('Runtime (seconds)', fontsize=14, fontweight='bold')
    ax.set_title('Algorithm Comparison: Runtime vs Number of Agents',
                 fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'runtime_vs_agents.png'), dpi=300)
    print(f"Saved: {os.path.join(output_dir, 'runtime_vs_agents.png')}")
    plt.close()


def plot_cost_comparison(df, output_dir):
    """Plot solution cost comparison."""
    solvers = ["Independent", "Prioritized", "CBS"]

    # Prepare data for successful runs only
    cost_data = []
    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True]
        for _, row in successful.iterrows():
            if pd.notna(row[f"{solver}_cost"]):
                cost_data.append({
                    'Solver': solver,
                    'Cost': row[f"{solver}_cost"],
                    'Instance': row['instance']
                })

    cost_df = pd.DataFrame(cost_data)

    if cost_df.empty:
        print("No successful runs to plot cost comparison.")
        return

    # Box plot
    fig, ax = plt.subplots()
    sns.boxplot(data=cost_df, x='Solver', y='Cost', ax=ax)
    ax.set_title('Solution Cost Distribution by Solver',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Solver', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sum of Costs', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cost_boxplot.png'), dpi=300)
    print(f"Saved: {os.path.join(output_dir, 'cost_boxplot.png')}")
    plt.close()


def plot_cost_vs_agents(df, output_dir):
    """Plot solution cost vs number of agents with line chart."""
    solvers = ["Independent", "Prioritized", "CBS"]
    colors = {'Independent': '#3498db', 'Prioritized': '#e67e22', 'CBS': '#9b59b6'}
    markers = {'Independent': 'o', 'Prioritized': 's', 'CBS': '^'}

    fig, ax = plt.subplots(figsize=(12, 8))

    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True].copy()
        successful = successful[successful[f"{solver}_cost"].notna()]
        if not successful.empty:
            # Sort by number of agents for proper line plotting
            successful = successful.sort_values('num_agents')
            ax.plot(successful['num_agents'], successful[f"{solver}_cost"],
                   label=solver, linewidth=2.5, marker=markers[solver],
                   markersize=10, color=colors[solver], alpha=0.8)

    ax.set_xlabel('Number of Agents', fontsize=14, fontweight='bold')
    ax.set_ylabel('Sum of Costs', fontsize=14, fontweight='bold')
    ax.set_title('Algorithm Comparison: Solution Cost vs Number of Agents',
                 fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cost_vs_agents.png'), dpi=300)
    print(f"Saved: {os.path.join(output_dir, 'cost_vs_agents.png')}")
    plt.close()


def plot_runtime_vs_map_size(df, output_dir):
    """Plot runtime vs map size."""
    solvers = ["Independent", "Prioritized", "CBS"]
    colors = {'Independent': '#3498db', 'Prioritized': '#e67e22', 'CBS': '#9b59b6'}

    fig, ax = plt.subplots()

    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True]
        if not successful.empty:
            ax.scatter(successful['map_size'], successful[f"{solver}_time"],
                      label=solver, alpha=0.7, s=100, color=colors[solver])

    ax.set_xlabel('Map Size (cells)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Runtime vs Map Size', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'runtime_vs_mapsize.png'), dpi=300)
    print(f"Saved: {os.path.join(output_dir, 'runtime_vs_mapsize.png')}")
    plt.close()


def plot_performance_heatmap(df, output_dir):
    """Create a heatmap showing solver performance across instances."""
    solvers = ["Independent", "Prioritized", "CBS"]

    # Create a matrix where rows are instances and columns are solvers
    # Values are runtime (or inf for failures)
    instances = df['instance'].tolist()
    data = []

    for _, row in df.iterrows():
        row_data = []
        for solver in solvers:
            if row[f"{solver}_success"]:
                row_data.append(row[f"{solver}_time"])
            else:
                row_data.append(float('inf'))
        data.append(row_data)

    # Replace inf with a large value for visualization
    max_time = max([v for row in data for v in row if v != float('inf')], default=1)
    data = [[v if v != float('inf') else max_time * 2 for v in row] for row in data]

    fig, ax = plt.subplots(figsize=(8, max(6, len(instances) * 0.4)))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto')

    # Set ticks
    ax.set_xticks(range(len(solvers)))
    ax.set_yticks(range(len(instances)))
    ax.set_xticklabels(solvers)
    ax.set_yticklabels(instances, fontsize=8)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Runtime (s)', fontsize=10, fontweight='bold')

    ax.set_title('Solver Performance Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'performance_heatmap.png'), dpi=300)
    print(f"Saved: {os.path.join(output_dir, 'performance_heatmap.png')}")
    plt.close()


def plot_combined_comparison(df, output_dir):
    """Create a comprehensive side-by-side comparison of all three algorithms."""
    solvers = ["Independent", "Prioritized", "CBS"]
    colors = {'Independent': '#3498db', 'Prioritized': '#e67e22', 'CBS': '#9b59b6'}
    markers = {'Independent': 'o', 'Prioritized': 's', 'CBS': '^'}

    # Create a 2x2 subplot layout
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    # Plot 1: Runtime vs Agents (line chart)
    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True].copy()
        if not successful.empty:
            successful = successful.sort_values('num_agents')
            ax1.plot(successful['num_agents'], successful[f"{solver}_time"],
                    label=solver, linewidth=2.5, marker=markers[solver],
                    markersize=8, color=colors[solver], alpha=0.8)
    ax1.set_xlabel('Number of Agents', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Runtime vs Number of Agents', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Plot 2: Cost vs Agents (line chart)
    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True].copy()
        successful = successful[successful[f"{solver}_cost"].notna()]
        if not successful.empty:
            successful = successful.sort_values('num_agents')
            ax2.plot(successful['num_agents'], successful[f"{solver}_cost"],
                    label=solver, linewidth=2.5, marker=markers[solver],
                    markersize=8, color=colors[solver], alpha=0.8)
    ax2.set_xlabel('Number of Agents', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Sum of Costs', fontsize=12, fontweight='bold')
    ax2.set_title('Solution Cost vs Number of Agents', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')

    # Plot 3: Runtime vs Map Size (line chart)
    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True].copy()
        if not successful.empty:
            successful = successful.sort_values('map_size')
            ax3.plot(successful['map_size'], successful[f"{solver}_time"],
                    label=solver, linewidth=2.5, marker=markers[solver],
                    markersize=8, color=colors[solver], alpha=0.8)
    ax3.set_xlabel('Map Size (cells)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
    ax3.set_title('Runtime vs Map Size', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, linestyle='--')

    # Plot 4: Average metrics bar chart
    avg_data = {'Runtime (ms)': [], 'Cost': []}
    for solver in solvers:
        successful = df[df[f"{solver}_success"] == True]
        avg_runtime = successful[f"{solver}_time"].mean() * 1000  # Convert to ms
        avg_cost = successful[successful[f"{solver}_cost"].notna()][f"{solver}_cost"].mean()
        avg_data['Runtime (ms)'].append(avg_runtime)
        avg_data['Cost'].append(avg_cost)

    x = range(len(solvers))
    width = 0.35
    ax4_twin = ax4.twinx()

    bars1 = ax4.bar([i - width/2 for i in x], avg_data['Runtime (ms)'], width,
                    label='Avg Runtime (ms)', color='#3498db', alpha=0.7)
    bars2 = ax4_twin.bar([i + width/2 for i in x], avg_data['Cost'], width,
                         label='Avg Cost', color='#e74c3c', alpha=0.7)

    ax4.set_xlabel('Solver', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Average Runtime (ms)', fontsize=12, fontweight='bold', color='#3498db')
    ax4_twin.set_ylabel('Average Cost', fontsize=12, fontweight='bold', color='#e74c3c')
    ax4.set_title('Average Performance Metrics', fontsize=13, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(solvers)
    ax4.tick_params(axis='y', labelcolor='#3498db')
    ax4_twin.tick_params(axis='y', labelcolor='#e74c3c')
    ax4.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Add value labels on bars
    for bar, val in zip(bars1, avg_data['Runtime (ms)']):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom', fontsize=9)
    for bar, val in zip(bars2, avg_data['Cost']):
        height = bar.get_height()
        ax4_twin.text(bar.get_x() + bar.get_width()/2., height,
                     f'{val:.1f}', ha='center', va='bottom', fontsize=9)

    # Add combined legend
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, fontsize=10, loc='upper left')

    plt.suptitle('MAPF Algorithms: Comprehensive Performance Comparison',
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'combined_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: {os.path.join(output_dir, 'combined_comparison.png')}")
    plt.close()


def generate_all_graphs(csv_file, output_dir):
    """Generate all benchmark graphs."""
    print(f"\nGenerating graphs from {csv_file}...")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    df = load_results(csv_file)
    print(f"Loaded {len(df)} benchmark results")

    # Generate graphs
    plot_success_rates(df, output_dir)
    plot_runtime_comparison(df, output_dir)
    plot_runtime_vs_agents(df, output_dir)
    plot_cost_comparison(df, output_dir)
    plot_cost_vs_agents(df, output_dir)
    plot_runtime_vs_map_size(df, output_dir)
    plot_performance_heatmap(df, output_dir)
    plot_combined_comparison(df, output_dir)

    print(f"\nAll graphs generated successfully in {output_dir}/")


def main():
    parser = argparse.ArgumentParser(description='Generate benchmark graphs')
    parser.add_argument('--input', type=str, default='benchmark_results.csv',
                        help='Input CSV file with benchmark results')
    parser.add_argument('--output_dir', type=str, default='benchmark_graphs',
                        help='Output directory for generated graphs')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        return

    generate_all_graphs(args.input, args.output_dir)


if __name__ == '__main__':
    main()
