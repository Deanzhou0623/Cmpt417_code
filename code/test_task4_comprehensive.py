#!/usr/bin/env python3
"""Comprehensive tests for Task 4: CBS with Disjoint Splitting"""

from single_agent_planner import a_star, compute_heuristics, is_constrained, build_constraint_table
from cbs import CBSSolver, disjoint_splitting, paths_violate_constraint
from visualize import Animation
import random

def test_positive_vertex_constraint():
    """Test that positive vertex constraints work correctly"""
    print("\n=== Test 1: Positive Vertex Constraint ===")

    # Simple map
    my_map = [
        [True, True, True, True, True],
        [True, False, False, False, True],
        [True, False, False, False, True],
        [True, True, True, True, True]
    ]

    start = (1, 1)
    goal = (1, 3)
    h_values = compute_heuristics(my_map, goal)

    # Positive constraint: must be at (1, 2) at timestep 1
    constraints = [
        {'agent': 0, 'loc': [(1, 2)], 'timestep': 1, 'positive': True}
    ]

    path = a_star(my_map, start, goal, h_values, 0, constraints)
    print(f"Start: {start}, Goal: {goal}")
    print(f"Constraint: Must be at (1, 2) at t=1")
    print(f"Path found: {path}")

    if path:
        from single_agent_planner import get_location
        loc_at_t1 = get_location(path, 1)
        assert loc_at_t1 == (1, 2), f"Agent should be at (1, 2) at t=1, but was at {loc_at_t1}"
        print("✓ Agent correctly at (1, 2) at t=1")
    else:
        print("✗ No path found!")
        return False

    return True


def test_positive_edge_constraint():
    """Test that positive edge constraints work correctly"""
    print("\n=== Test 2: Positive Edge Constraint ===")

    my_map = [
        [True, True, True, True, True],
        [True, False, False, False, True],
        [True, False, False, False, True],
        [True, True, True, True, True]
    ]

    start = (1, 1)
    goal = (2, 3)
    h_values = compute_heuristics(my_map, goal)

    # Positive constraint: must traverse edge (1,2) -> (1,3) at timestep 2
    constraints = [
        {'agent': 0, 'loc': [(1, 2), (1, 3)], 'timestep': 2, 'positive': True}
    ]

    path = a_star(my_map, start, goal, h_values, 0, constraints)
    print(f"Start: {start}, Goal: {goal}")
    print(f"Constraint: Must traverse edge (1,2)->(1,3) at t=2")
    print(f"Path found: {path}")

    if path and len(path) > 2:
        from single_agent_planner import get_location
        loc_at_t1 = get_location(path, 1)
        loc_at_t2 = get_location(path, 2)
        assert loc_at_t1 == (1, 2) and loc_at_t2 == (1, 3), \
            f"Agent should traverse (1,2)->(1,3) at t=2, but went {loc_at_t1}->{loc_at_t2}"
        print(f"✓ Agent correctly traversed edge (1,2)->(1,3) at t=2")
    else:
        print("✗ No valid path found!")
        return False

    return True


def test_disjoint_splitting_vertex():
    """Test disjoint splitting for vertex collision"""
    print("\n=== Test 3: Disjoint Splitting - Vertex Collision ===")

    collision = {
        'a1': 0,
        'a2': 1,
        'loc': [(2, 3)],
        'timestep': 5
    }

    # Set seed for reproducibility
    random.seed(42)
    constraints = disjoint_splitting(collision)

    print(f"Collision: agents 0 and 1 at {collision['loc'][0]} at t=5")
    print(f"Generated {len(constraints)} constraints:")

    assert len(constraints) == 2, "Should generate exactly 2 constraints"

    positive_count = sum(1 for c in constraints if c.get('positive', False))
    negative_count = sum(1 for c in constraints if not c.get('positive', False))

    assert positive_count == 1, f"Should have 1 positive constraint, got {positive_count}"
    assert negative_count == 1, f"Should have 1 negative constraint, got {negative_count}"

    for c in constraints:
        print(f"  Agent {c['agent']}: {'MUST' if c.get('positive') else 'MUST NOT'} be at {c['loc']} at t={c['timestep']}")

    print("✓ Disjoint splitting correctly generated 1 positive + 1 negative constraint")
    return True


def test_disjoint_splitting_edge():
    """Test disjoint splitting for edge collision"""
    print("\n=== Test 4: Disjoint Splitting - Edge Collision ===")

    collision = {
        'a1': 0,
        'a2': 1,
        'loc': [(2, 2), (2, 3)],
        'timestep': 4
    }

    random.seed(123)
    constraints = disjoint_splitting(collision)

    print(f"Collision: agent 0 moves (2,2)->(2,3) and agent 1 moves (2,3)->(2,2) at t=4")
    print(f"Generated {len(constraints)} constraints:")

    assert len(constraints) == 2, "Should generate exactly 2 constraints"

    positive_count = sum(1 for c in constraints if c.get('positive', False))
    negative_count = sum(1 for c in constraints if not c.get('positive', False))

    assert positive_count == 1, f"Should have 1 positive constraint, got {positive_count}"
    assert negative_count == 1, f"Should have 1 negative constraint, got {negative_count}"

    for c in constraints:
        edge_str = f"{c['loc'][0]}->{c['loc'][1]}" if len(c['loc']) == 2 else str(c['loc'][0])
        print(f"  Agent {c['agent']}: {'MUST' if c.get('positive') else 'MUST NOT'} traverse {edge_str} at t={c['timestep']}")

    print("✓ Disjoint splitting correctly generated 1 positive + 1 negative constraint")
    return True


def test_paths_violate_constraint_vertex():
    """Test paths_violate_constraint for vertex constraints"""
    print("\n=== Test 5: paths_violate_constraint - Vertex ===")

    # Three agents with simple paths
    paths = [
        [(1, 1), (1, 2), (1, 3), (1, 4)],  # Agent 0
        [(2, 1), (2, 2), (1, 3), (2, 4)],  # Agent 1 - will be at (1,3) at t=2
        [(3, 1), (3, 2), (3, 3), (3, 4)]   # Agent 2
    ]

    # Agent 0 must be at (1, 3) at timestep 2
    constraint = {
        'agent': 0,
        'loc': [(1, 3)],
        'timestep': 2,
        'positive': True
    }

    violating_agents = paths_violate_constraint(constraint, paths)
    print(f"Constraint: Agent 0 MUST be at (1,3) at t=2")
    print(f"Agent paths at t=2: Agent 0: {paths[0][2]}, Agent 1: {paths[1][2]}, Agent 2: {paths[2][2]}")
    print(f"Violating agents: {violating_agents}")

    assert 1 in violating_agents, "Agent 1 should violate (also at (1,3) at t=2)"
    assert 2 not in violating_agents, "Agent 2 should not violate"

    print("✓ Correctly identified violating agents")
    return True


def test_cbs_with_disjoint():
    """Test full CBS with disjoint splitting on a simple case"""
    print("\n=== Test 6: Full CBS with Disjoint Splitting ===")

    my_map = [
        [True, True, True, True, True, True],
        [True, False, False, False, False, True],
        [True, False, False, False, False, True],
        [True, False, False, False, False, True],
        [True, True, True, True, True, True]
    ]

    starts = [(1, 1), (1, 4)]
    goals = [(1, 4), (1, 1)]

    print(f"2 agents swapping positions")
    print(f"Starts: {starts}")
    print(f"Goals: {goals}")

    # Test with standard CBS
    print("\n--- Standard CBS ---")
    cbs_standard = CBSSolver(my_map, starts, goals)
    paths_standard = cbs_standard.find_solution(disjoint=False)
    expanded_standard = cbs_standard.num_of_expanded
    cost_standard = sum(len(p) - 1 for p in paths_standard)

    # Test with disjoint CBS
    print("\n--- CBS with Disjoint Splitting ---")
    cbs_disjoint = CBSSolver(my_map, starts, goals)
    paths_disjoint = cbs_disjoint.find_solution(disjoint=True)
    expanded_disjoint = cbs_disjoint.num_of_expanded
    cost_disjoint = sum(len(p) - 1 for p in paths_disjoint)

    print(f"\nResults:")
    print(f"  Standard CBS: {expanded_standard} nodes expanded, cost = {cost_standard}")
    print(f"  Disjoint CBS: {expanded_disjoint} nodes expanded, cost = {cost_disjoint}")

    assert cost_standard == cost_disjoint, "Both should find optimal solution with same cost"
    print(f"✓ Both algorithms found optimal solution (cost={cost_standard})")

    if expanded_disjoint <= expanded_standard:
        print(f"✓ Disjoint splitting improved or matched efficiency ({expanded_disjoint} vs {expanded_standard})")
    else:
        print(f"⚠ Disjoint expanded more nodes (randomness can cause this occasionally)")

    return True


def test_exp4_instance():
    """Test on exp4.txt as specified in the assignment"""
    print("\n=== Test 7: exp4.txt Instance ===")

    from run_experiments import import_mapf_instance

    my_map, starts, goals = import_mapf_instance('instances/exp4.txt')

    print("Testing exp4.txt instance")
    print(f"Agents: {len(starts)}")

    # Standard CBS
    print("\n--- Standard CBS ---")
    cbs_standard = CBSSolver(my_map, starts, goals)
    paths_standard = cbs_standard.find_solution(disjoint=False)
    expanded_standard = cbs_standard.num_of_expanded
    cost_standard = sum(len(p) - 1 for p in paths_standard)

    # Disjoint CBS
    print("\n--- CBS with Disjoint Splitting ---")
    cbs_disjoint = CBSSolver(my_map, starts, goals)
    paths_disjoint = cbs_disjoint.find_solution(disjoint=True)
    expanded_disjoint = cbs_disjoint.num_of_expanded
    cost_disjoint = sum(len(p) - 1 for p in paths_disjoint)

    print(f"\n{'='*60}")
    print(f"RESULTS FOR exp4.txt:")
    print(f"  Standard CBS: {expanded_standard} nodes expanded, cost = {cost_standard}")
    print(f"  Disjoint CBS: {expanded_disjoint} nodes expanded, cost = {cost_disjoint}")
    print(f"  Improvement: {expanded_standard - expanded_disjoint} fewer nodes")
    print(f"{'='*60}")

    assert cost_standard == cost_disjoint, "Both should find optimal solution"
    print("✓ Both algorithms found optimal solution with same cost")

    # Assignment says ~11 for standard, ~8 for disjoint
    if expanded_disjoint < expanded_standard:
        print(f"✓ Disjoint splitting reduced node expansions")

    return True


if __name__ == '__main__':
    print("="*60)
    print("COMPREHENSIVE TASK 4 TEST SUITE")
    print("="*60)

    tests = [
        ("Positive Vertex Constraint", test_positive_vertex_constraint),
        ("Positive Edge Constraint", test_positive_edge_constraint),
        ("Disjoint Splitting - Vertex", test_disjoint_splitting_vertex),
        ("Disjoint Splitting - Edge", test_disjoint_splitting_edge),
        ("paths_violate_constraint - Vertex", test_paths_violate_constraint_vertex),
        ("Full CBS with Disjoint", test_cbs_with_disjoint),
        ("exp4.txt Instance", test_exp4_instance),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"✗ {name} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60)
