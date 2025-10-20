from collections import deque

def solve_treasure_hunt():
    # Read input
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        grid.append(input().split())
    
    start_x, start_y = map(int, input().split())
    pearl_val, platinum_val, gold_val, diamond_val = map(int, input().split())
    k = int(input())
    
    # Map symbols to values
    treasure_values = {
        '$': pearl_val,
        '*': platinum_val,
        '%': gold_val,
        '+': diamond_val,
        '#': 0  # Rock has no value
    }
    
    # Check if a cell is stable (has rock below or is bottom row)
    def is_stable(r, c):
        if r == n - 1:  # Bottom row is always stable
            return True
        if r + 1 < n and grid[r + 1][c] == '#':
            return True
        return False
    
    # Simulate sliding down from position (r, c) and collect treasures
    def slide_down(r, c):
        total_value = 0
        steps = 0
        
        while r < n:
            if grid[r][c] != '#':  # Can stand here
                total_value += treasure_values[grid[r][c]]
                if is_stable(r, c):
                    return r, c, total_value, steps
                steps += 1
                r += 1
            else:
                # Hit a rock, stop at position above it
                if r > 0:
                    return r - 1, c, total_value, steps - 1
                break
        
        # Reached bottom or couldn't find valid position
        return -1, -1, 0, 0
    
    # BFS to find maximum treasure value
    # State: (row, col, steps_used, treasure_collected)
    queue = deque()
    
    # Start position
    start_value = treasure_values[grid[start_x][start_y]]
    queue.append((start_x, start_y, 0, start_value))
    
    # Track best value for each (row, col, steps) state
    visited = {}
    max_treasure = 0
    
    while queue:
        r, c, steps, treasure = queue.popleft()
        
        # Check if we can end here (not on last row)
        if r != n - 1 and is_stable(r, c):
            max_treasure = max(max_treasure, treasure)
        
        if steps >= k:
            continue
        
        # State key for memoization
        state_key = (r, c, steps)
        if state_key in visited and visited[state_key] >= treasure:
            continue
        visited[state_key] = treasure
        
        # Try moving left
        if c > 0 and grid[r][c - 1] != '#':
            if is_stable(r, c - 1):
                new_treasure = treasure + treasure_values[grid[r][c - 1]]
                queue.append((r, c - 1, steps + 1, new_treasure))
            else:
                # Slide down
                new_r, new_c, slide_value, slide_steps = slide_down(r, c - 1)
                if new_r != -1 and steps + slide_steps + 1 <= k:
                    new_treasure = treasure + slide_value
                    queue.append((new_r, new_c, steps + slide_steps + 1, new_treasure))
        
        # Try moving right
        if c < m - 1 and grid[r][c + 1] != '#':
            if is_stable(r, c + 1):
                new_treasure = treasure + treasure_values[grid[r][c + 1]]
                queue.append((r, c + 1, steps + 1, new_treasure))
            else:
                # Slide down
                new_r, new_c, slide_value, slide_steps = slide_down(r, c + 1)
                if new_r != -1 and steps + slide_steps + 1 <= k:
                    new_treasure = treasure + slide_value
                    queue.append((new_r, new_c, steps + slide_steps + 1, new_treasure))
        
        # Try climbing up (only if there's a rock above)
        if r > 0 and grid[r - 1][c] == '#':
            # Can climb on the rock, try to move to cells adjacent to rock
            # Move up-left
            if c > 0 and r > 0 and grid[r - 1][c - 1] != '#':
                if is_stable(r - 1, c - 1):
                    new_treasure = treasure + treasure_values[grid[r - 1][c - 1]]
                    queue.append((r - 1, c - 1, steps + 1, new_treasure))
                else:
                    new_r, new_c, slide_value, slide_steps = slide_down(r - 1, c - 1)
                    if new_r != -1 and steps + slide_steps + 1 <= k:
                        new_treasure = treasure + slide_value
                        queue.append((new_r, new_c, steps + slide_steps + 1, new_treasure))
            
            # Move up-right
            if c < m - 1 and r > 0 and grid[r - 1][c + 1] != '#':
                if is_stable(r - 1, c + 1):
                    new_treasure = treasure + treasure_values[grid[r - 1][c + 1]]
                    queue.append((r - 1, c + 1, steps + 1, new_treasure))
                else:
                    new_r, new_c, slide_value, slide_steps = slide_down(r - 1, c + 1)
                    if new_r != -1 and steps + slide_steps + 1 <= k:
                        new_treasure = treasure + slide_value
                        queue.append((new_r, new_c, steps + slide_steps + 1, new_treasure))
            
            # Move directly up (if there's a cell above the rock)
            if r >= 2 and grid[r - 2][c] != '#':
                if is_stable(r - 2, c):
                    new_treasure = treasure + treasure_values[grid[r - 2][c]]
                    queue.append((r - 2, c, steps + 1, new_treasure))
                else:
                    new_r, new_c, slide_value, slide_steps = slide_down(r - 2, c)
                    if new_r != -1 and steps + slide_steps + 1 <= k:
                        new_treasure = treasure + slide_value
                        queue.append((new_r, new_c, steps + slide_steps + 1, new_treasure))
    
    print(max_treasure)

solve_treasure_hunt()