from collections import defaultdict
from itertools import permutations

def solve_optimal_arrangement():
    # Read input
    n = int(input())
    goodies = []
    for i in range(n):
        line = input().split()
        label = line[0]
        weight = int(line[1])
        goodies.append((label, weight, i + 1))  # position is 1-indexed from shore
    
    k = int(input())
    
    # Group goodies by ship label
    ship_data = defaultdict(lambda: {'total_weight': 0, 'weighted_positions': 0})
    
    for label, weight, position in goodies:
        ship_data[label]['total_weight'] += weight
        ship_data[label]['weighted_positions'] += weight * position
    
    # Get unique ships
    ships = list(ship_data.keys())
    
    # Calculate the cost for a given arrangement
    def calculate_cost(arrangement):
        total_cost = 0
        for ship_position, ship_label in enumerate(arrangement, 1):
            data = ship_data[ship_label]
            # Cost = sum(weight * (goodie_pos + ship_pos)) for all goodies going to this ship
            # = sum(weight * goodie_pos) + ship_pos * sum(weight)
            total_cost += data['weighted_positions'] + ship_position * data['total_weight']
        return total_cost
    
    # Find minimum cost by trying all permutations
    min_cost = float('inf')
    all_arrangements = []
    
    for perm in permutations(ships):
        cost = calculate_cost(perm)
        if cost < min_cost:
            min_cost = cost
            all_arrangements = [perm]
        elif cost == min_cost:
            all_arrangements.append(perm)
    
    # Sort arrangements alphabetically
    all_arrangements.sort()
    
    # Get the Kth arrangement (1-indexed)
    result_arrangement = all_arrangements[k - 1]
    
    print(min_cost)
    print(' '.join(result_arrangement))

# Run the solution
solve_optimal_arrangement()
