from collections import defaultdict
from itertools import permutations

def solve_optimal_arrangement():
    n = int(input())
    ship_data = defaultdict(lambda: {'total_weight': 0, 'weighted_positions': 0})
    
    for i in range(n):
        line = input().split()
        label = line[0]
        weight = int(line[1])
        position = i + 1
        
        ship_data[label]['total_weight'] += weight
        ship_data[label]['weighted_positions'] += weight * position
    
    k = int(input())
    ships = list(ship_data.keys())
    m = len(ships)
    
    # Precompute ship costs (constant part independent of arrangement)
    ship_costs = {}
    for label in ships:
        ship_costs[label] = ship_data[label]['weighted_positions']
    
    # Calculate cost more efficiently
    def calculate_cost(arrangement):
        # Cost = sum of (weighted_positions[i] + position[i] * total_weight[i])
        # = sum of weighted_positions[i] + sum of (position[i] * total_weight[i])
        cost = sum(ship_costs[label] for label in arrangement)
        cost += sum((i + 1) * ship_data[arrangement[i]]['total_weight'] 
                   for i in range(m))
        return cost
    
    # Use greedy sorting to find optimal arrangement more efficiently
    # Sort by total_weight in ascending order for initial heuristic
    sorted_ships = sorted(ships, key=lambda x: ship_data[x]['total_weight'])
    
    min_cost = float('inf')
    optimal_arrangements = []
    
    # For small m, check all permutations
    # For larger m, use heuristic approach
    if m <= 8:
        for perm in permutations(ships):
            cost = calculate_cost(perm)
            if cost < min_cost:
                min_cost = cost
                optimal_arrangements = [perm]
            elif cost == min_cost:
                optimal_arrangements.append(perm)
    else:
        # Heuristic: ships with lower total weight should go first
        # This minimizes their positional multiplier impact
        min_cost = calculate_cost(tuple(sorted_ships))
        optimal_arrangements = [tuple(sorted_ships)]
    
    optimal_arrangements.sort()
    result_arrangement = optimal_arrangements[k - 1]
    
    print(min_cost)
    print(' '.join(result_arrangement))

solve_optimal_arrangement()