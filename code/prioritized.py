import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost


class PrioritizedPlanningSolver(object):
    """A planner that plans for each robot sequentially."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()
        result = []
        constraints = []

        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints)
            if path is None:
                raise BaseException('No solutions')
            result.append(path)

            ##############################
            # Task 2: Add constraints here
            #         Useful variables:
            #            * path contains the solution path of the current (i'th) agent, e.g., [(1,1),(1,2),(1,3)]
            #            * self.num_of_agents has the number of total agents
            #            * constraints: array of constraints to consider for future A* searches

            # Task 2.1: Add vertex constraints
            # For each timestep in the current agent's path, add a vertex constraint
            # for all future agents (agents with index > i)
            for timestep in range(len(path)):
                for future_agent in range(i + 1, self.num_of_agents):
                    constraints.append({
                        'agent': future_agent,
                        'loc': [path[timestep]],
                        'timestep': timestep
                    })

            # Task 2.2: Add edge constraints
            # For each edge (move from one cell to another), add an edge constraint
            # for all future agents to prevent them from taking the reverse edge
            for timestep in range(len(path) - 1):
                for future_agent in range(i + 1, self.num_of_agents):
                    # Edge from path[timestep] to path[timestep+1]
                    # Constrain reverse edge: path[timestep+1] to path[timestep] at timestep+1
                    constraints.append({
                        'agent': future_agent,
                        'loc': [path[timestep + 1], path[timestep]],
                        'timestep': timestep + 1
                    })

            # Task 2.3: Add goal constraints for all future timesteps
            # Agent stays at goal forever, so constrain the goal location for all future timesteps
            goal_loc = path[-1]
            max_timestep = len(path) - 1
            # Add constraints for a reasonable time horizon (e.g., sum of all path lengths)
            # For now, use a large enough number to cover typical scenarios
            for future_timestep in range(max_timestep, max_timestep + 100):
                for future_agent in range(i + 1, self.num_of_agents):
                    constraints.append({
                        'agent': future_agent,
                        'loc': [goal_loc],
                        'timestep': future_timestep
                    })

            ##############################

        self.CPU_time = timer.time() - start_time

        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))
        print(result)
        return result
