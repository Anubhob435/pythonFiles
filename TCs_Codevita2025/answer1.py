from collections import defaultdict
from itertools import permutations, product

def solve_optimal_arrangement():
    # Read input
    n = int(input())
    ship_data = {}
    
    for i in range(n):
        line = input().split()
        label = line[0]
        weight = int(line[1])
        position = i + 1  # position is 1-indexed from shore
        
        if label not in ship_data:
            ship_data[label] = {'total_weight': 0, 'weighted_positions': 0}
        ship_data[label]['total_weight'] += weight
        ship_data[label]['weighted_positions'] += weight * position
    
    k = int(input())
    
    # Get unique ships
    ships = list(ship_data.keys())
    
    # Calculate the cost for a given arrangement (optimized)
    def calculate_cost(arrangement):
        total_cost = 0
        for ship_position, ship_label in enumerate(arrangement, 1):
            data = ship_data[ship_label]
            # Cost = weighted_positions + ship_position * total_weight
            total_cost += data['weighted_positions'] + ship_position * data['total_weight']
        return total_cost
    
    # Optimized approach: First find the minimum cost using greedy algorithm
    # Then find all arrangements that achieve this minimum cost
    
    # Greedy approach: Sort ships by total weight (descending) for initial estimate
    ships_by_weight = sorted(ships, key=lambda s: (-ship_data[s]['total_weight'], s))
    min_cost = calculate_cost(ships_by_weight)
    
    # Now find all arrangements with this minimum cost
    optimal_arrangements = []
    
    # Only check all permutations if number of ships is reasonable
    if len(ships) <= 10:
        for perm in permutations(ships):
            cost = calculate_cost(perm)
            if cost < min_cost:
                min_cost = cost
                optimal_arrangements = [perm]
            elif cost == min_cost:
                optimal_arrangements.append(perm)
    else:
        # For larger cases, use the greedy solution
        # Group ships by weight and generate permutations within groups
        weight_to_ships = defaultdict(list)
        for ship in ships:
            weight_to_ships[ship_data[ship]['total_weight']].append(ship)
        
        # Sort groups by weight (descending)
        sorted_weights = sorted(weight_to_ships.keys(), reverse=True)
        
        # Generate all arrangements by permuting within each weight group
        group_arrangements = []
        for weight in sorted_weights:
            group_ships = sorted(weight_to_ships[weight])  # Sort alphabetically
            group_arrangements.append(list(permutations(group_ships)))
        
        # Generate all combinations
        for combo in product(*group_arrangements):
            arrangement = []
            for group in combo:
                arrangement.extend(group)
            cost = calculate_cost(arrangement)
            if cost == min_cost:
                optimal_arrangements.append(tuple(arrangement))
    
    # Sort arrangements alphabetically
    optimal_arrangements.sort()
    
    # Get the Kth arrangement (1-indexed)
    result_arrangement = optimal_arrangements[k - 1]
    
    print(min_cost)
    print(' '.join(result_arrangement))

# Run the solution
solve_optimal_arrangement()
