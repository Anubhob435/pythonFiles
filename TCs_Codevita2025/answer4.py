from collections import deque

def solve_treasure_hunt():
    # Read input
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().strip()
        # Split by spaces and take only the first m elements to handle formatting
        if ' ' in row:
            grid.append(row.split()[:m])
        else:
            grid.append(list(row)[:m])
    
    start_x, start_y = map(int, input().split())
    values = list(map(int, input().split()))
    k = int(input())
    
    # Map treasure symbols to values
    treasure_values = {
        '$': values[0],  # Pearl
        '*': values[1],  # Platinum
        '%': values[2],  # Gold
        '+': values[3],  # Diamond
        '#': 0,          # Rock
        ' ': 0           # Empty space (handle spaces)
    }
    
    def is_valid(r, c):
        return 0 <= r < n and 0 <= c < m
    
    def is_stable(r, c):
        # Last row is always stable
        if r == n - 1:
            return True
        # Cell is stable if there's a rock directly below
        if is_valid(r + 1, c) and grid[r + 1][c] == '#':
            return True
        return False
    
    def slide_down(r, c):
        """Simulate sliding down from position (r, c) and return final position and collected treasures"""
        total_value = 0
        steps = 0
        current_r = r
        
        # If starting position is stable, no sliding occurs
        if is_stable(r, c):
            if grid[r][c] != '#':
                total_value = treasure_values[grid[r][c]]
            return current_r, c, total_value, steps
        
        # Slide down collecting treasures
        while current_r < n:
            if grid[current_r][c] != '#':
                total_value += treasure_values[grid[current_r][c]]
            
            # Check if we've reached a stable position
            if is_stable(current_r, c):
                break
            
            current_r += 1
            steps += 1
        
        return current_r, c, total_value, steps
    
    # BFS to explore all possible paths
    # State: (row, col, steps_used, total_value)
    queue = deque()
    
    # Start from the initial position
    initial_r, initial_c, initial_value, slide_steps = slide_down(start_x, start_y)
    if slide_steps <= k:
        queue.append((initial_r, initial_c, slide_steps, initial_value))
    
    # Track visited states to avoid revisiting same state with worse or equal conditions
    # Key: (row, col, steps), Value: max_value at that state
    visited = {}
    max_treasure = 0
    
    # Track stable positions we've already been to
    visited_stable_positions = set()
    
    # If we start on a stable cell that's not in the last row
    if initial_r != n - 1 and is_stable(initial_r, initial_c):
        max_treasure = initial_value
        visited_stable_positions.add((initial_r, initial_c))
    
    while queue:
        curr_r, curr_c, steps_used, curr_value = queue.popleft()
        
        # Skip if we've used too many steps
        if steps_used > k:
            continue
        
        # Check if this state was already visited with better or equal value
        state_key = (curr_r, curr_c, steps_used)
        if state_key in visited and visited[state_key] >= curr_value:
            continue
        visited[state_key] = curr_value
        
        # Update max treasure if we're on a stable cell not in the last row
        if is_stable(curr_r, curr_c) and curr_r != n - 1:
            # Only count if this is a new stable position or we got here with more value
            stable_pos = (curr_r, curr_c)
            if stable_pos not in visited_stable_positions or curr_value > max_treasure:
                max_treasure = max(max_treasure, curr_value)
                visited_stable_positions.add(stable_pos)
        
        # Try moving left
        if is_valid(curr_r, curr_c - 1) and grid[curr_r][curr_c - 1] != '#':
            new_r, new_c, slide_value, slide_steps_taken = slide_down(curr_r, curr_c - 1)
            total_steps = steps_used + 1 + slide_steps_taken
            # Only add to queue if we end up at a different position or it's worth exploring
            if total_steps <= k and (new_r != curr_r or new_c != curr_c):
                queue.append((new_r, new_c, total_steps, curr_value + slide_value))
        
        # Try moving right
        if is_valid(curr_r, curr_c + 1) and grid[curr_r][curr_c + 1] != '#':
            new_r, new_c, slide_value, slide_steps_taken = slide_down(curr_r, curr_c + 1)
            total_steps = steps_used + 1 + slide_steps_taken
            # Only add to queue if we end up at a different position or it's worth exploring
            if total_steps <= k and (new_r != curr_r or new_c != curr_c):
                queue.append((new_r, new_c, total_steps, curr_value + slide_value))
        
        # Try climbing up
        if is_valid(curr_r - 1, curr_c):
            # Can climb if there's a rock to use
            if grid[curr_r - 1][curr_c] == '#':
                # Check if there's a cell above the rock to land on
                if is_valid(curr_r - 2, curr_c) and grid[curr_r - 2][curr_c] != '#':
                    new_r, new_c, slide_value, slide_steps_taken = slide_down(curr_r - 2, curr_c)
                    total_steps = steps_used + 1 + slide_steps_taken
                    # Only add to queue if we end up at a different position or it's worth exploring
                    if total_steps <= k and (new_r != curr_r or new_c != curr_c):
                        queue.append((new_r, new_c, total_steps, curr_value + slide_value))
            elif grid[curr_r - 1][curr_c] != '#':
                # Can move to treasure cell above
                new_r, new_c, slide_value, slide_steps_taken = slide_down(curr_r - 1, curr_c)
                total_steps = steps_used + 1 + slide_steps_taken
                # Only add to queue if we end up at a different position or it's worth exploring
                if total_steps <= k and (new_r != curr_r or new_c != curr_c):
                    queue.append((new_r, new_c, total_steps, curr_value + slide_value))
    
    print(max_treasure)

solve_treasure_hunt()
