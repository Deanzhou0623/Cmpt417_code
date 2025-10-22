# Task 4: CBS with Disjoint Splitting

## Overview
We extended the CBS solver to support disjoint splitting by introducing positive constraints and the required low‑level replanning logic. The main goals were to (1) handle positive vertex and edge constraints in the single-agent planner, (2) convert collisions into disjoint constraints where one branch enforces the colliding action, and (3) ensure the high-level search correctly propagates the stronger implications of positive constraints.

## Implementation Highlights
- Added the `positive` flag to every generated constraint (both standard and disjoint) and updated the low-level A* (`single_agent_planner.is_constrained`) to interpret positive vertex/edge constraints as required actions.
- Replaced the previous disjoint splitting helper with a version that generates exactly two constraints for a randomly selected colliding agent: one positive constraint that enforces the colliding action and one negative constraint that forbids it, creating the two disjoint branches.
- Augmented the high-level CBS loop so that whenever a positive constraint is added, we immediately derive the implied negative constraints for all other agents and replan any agent that violates them. Child nodes are discarded if any required replanning fails, keeping the search tree consistent with the stronger constraints.
- Relaxed `run_experiments.py`’s dependency on `matplotlib` by deferring the import of `Animation` until visualisation is requested, enabling batch runs in environments without GUI support.

## Experiments
1. **exp4 Benchmark**  
   ```bash
   python3 run_experiments.py --instance instances/exp4.txt --solver CBS --disjoint --batch
   ```  
   Observed: expanded 9 nodes, generated 13 nodes, sum of costs 11. (Runs vary slightly because the disjoint branch selection is random; the expanded-node count is within the expected range of ~8–11.)

2. **Regression Suite for `test_*` Instances**  
   ```bash
   python3 run_experiments.py --instance "instances/test_*" --solver CBS --batch --disjoint
   ```  
   The resulting `results.csv` matches the ground-truth values in `instances/min-sum-of-cost.csv` exactly (0 mismatches, 0 missing entries).

### Cost Comparison against `min-sum-of-cost.csv`

| Instance | Expected | Observed | Status |
|---|---:|---:|---|
| instances/test_1.txt | 41 | 41 | OK |
| instances/test_2.txt | 18 | 18 | OK |
| instances/test_3.txt | 28 | 28 | OK |
| instances/test_4.txt | 32 | 32 | OK |
| instances/test_5.txt | 26 | 26 | OK |
| instances/test_6.txt | 24 | 24 | OK |
| instances/test_7.txt | 34 | 34 | OK |
| instances/test_8.txt | 38 | 38 | OK |
| instances/test_9.txt | 24 | 24 | OK |
| instances/test_10.txt | 19 | 19 | OK |
| instances/test_11.txt | 35 | 35 | OK |
| instances/test_12.txt | 36 | 36 | OK |
| instances/test_13.txt | 36 | 36 | OK |
| instances/test_14.txt | 24 | 24 | OK |
| instances/test_15.txt | 50 | 50 | OK |
| instances/test_16.txt | 51 | 51 | OK |
| instances/test_17.txt | 39 | 39 | OK |
| instances/test_18.txt | 32 | 32 | OK |
| instances/test_19.txt | 47 | 47 | OK |
| instances/test_20.txt | 28 | 28 | OK |
| instances/test_21.txt | 46 | 46 | OK |
| instances/test_22.txt | 51 | 51 | OK |
| instances/test_23.txt | 32 | 32 | OK |
| instances/test_24.txt | 47 | 47 | OK |
| instances/test_25.txt | 40 | 40 | OK |
| instances/test_26.txt | 42 | 42 | OK |
| instances/test_27.txt | 40 | 40 | OK |
| instances/test_28.txt | 41 | 41 | OK |
| instances/test_29.txt | 48 | 48 | OK |
| instances/test_30.txt | 43 | 43 | OK |
| instances/test_31.txt | 39 | 39 | OK |
| instances/test_32.txt | 30 | 30 | OK |
| instances/test_33.txt | 28 | 28 | OK |
| instances/test_34.txt | 33 | 33 | OK |
| instances/test_35.txt | 30 | 30 | OK |
| instances/test_36.txt | 23 | 23 | OK |
| instances/test_37.txt | 38 | 38 | OK |
| instances/test_38.txt | 28 | 28 | OK |
| instances/test_39.txt | 35 | 35 | OK |
| instances/test_40.txt | 24 | 24 | OK |
| instances/test_41.txt | 45 | 45 | OK |
| instances/test_42.txt | 57 | 57 | OK |
| instances/test_43.txt | 43 | 43 | OK |
| instances/test_44.txt | 33 | 33 | OK |
| instances/test_45.txt | 24 | 24 | OK |
| instances/test_46.txt | 57 | 57 | OK |
| instances/test_47.txt | 65 | 65 | OK |
| instances/test_48.txt | 36 | 36 | OK |
| instances/test_49.txt | 42 | 42 | OK |
| instances/test_50.txt | 48 | 48 | OK |

## Results & Discussion
- Disjoint splitting reduced the number of expanded nodes on `exp4.txt` from the baseline CBS result (≈11 nodes) to 9 nodes in our run, reflecting the expected efficiency gain.
- Positive constraints are now fully supported in the single-agent planner, enabling consistent handling of the stronger disjoint constraints without violating completeness or optimality.
- The verification sweep confirmed that optimal costs remain unchanged across the full test battery, indicating the modifications preserved solution quality.

## Next Steps
- Consider seeding `random` for reproducible benchmarking across runs.
- Profile larger instances to quantify average node reductions due to disjoint splitting and explore heuristics for selecting the positive-constraint agent deterministically.
