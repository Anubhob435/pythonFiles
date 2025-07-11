def can_pick(sequence, gem_value):
    if len(sequence) == 0:
        return True
    return gem_value > sequence[-1]

def solve(gems, lila_sequence, theo_sequence, is_lila_turn):
    if len(gems) == 0:
        return not is_lila_turn
    
    left_gem = gems[0]
    right_gem = gems[-1]
    
    can_pick_left = False
    can_pick_right = False
    
    if is_lila_turn:
        can_pick_left = can_pick(lila_sequence, left_gem)
        can_pick_right = can_pick(lila_sequence, right_gem)
    else:
        can_pick_left = can_pick(theo_sequence, left_gem)
        can_pick_right = can_pick(theo_sequence, right_gem)
    
    if not can_pick_left and not can_pick_right:
        return not is_lila_turn
    
    results = []
    
    if can_pick_left:
        new_gems = gems[1:]
        if is_lila_turn:
            new_lila = lila_sequence + [left_gem]
            result = solve(new_gems, new_lila, theo_sequence, False)
        else:
            new_theo = theo_sequence + [left_gem]
            result = solve(new_gems, lila_sequence, new_theo, True)
        results.append(result)
    
    if can_pick_right:
        new_gems = gems[:-1]
        if is_lila_turn:
            new_lila = lila_sequence + [right_gem]
            result = solve(new_gems, new_lila, theo_sequence, False)
        else:
            new_theo = theo_sequence + [right_gem]
            result = solve(new_gems, lila_sequence, new_theo, True)
        results.append(result)
    
    if is_lila_turn:
        return any(results)
    else:
        return all(results)

n = int(input())
gems = list(map(int, input().split()))

lila_wins = solve(gems, [], [], True)

if lila_wins:
    print("Lila")
else:
    print("Theo")