def solve():
    # Read grid dimensions
    n, m = map(int, input().split())
    
    # Read the grid
    grid = []
    for i in range(n):
        row = input().split()
        grid.append(row)
    
    # Read T (length of secret key)
    t = int(input())
    
    # Read number of clues
    num_clues = int(input())
    
    # Initialize valid positions for each time step
    # valid[time] = set of (row, col) that are valid at that time
    valid = [set() for _ in range(t + 1)]
    
    # Initially, all positions are valid for all times
    for time in range(1, t + 1):
        for i in range(n):
            for j in range(m):
                valid[time].add((i, j))
    
    # Process clues
    for _ in range(num_clues):
        time = int(input())
        x1, y1, x2, y2 = map(int, input().split())
        
        # Convert to 0-based indexing
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        
        # Remove positions in the sub-grid from valid positions at this time
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                if 0 <= i < n and 0 <= j < m:
                    valid[time].discard((i, j))
    
    # Check if any time step has no valid positions
    for time in range(1, t + 1):
        if len(valid[time]) == 0:
            print("Not enough clues")
            return
    
    # Find all valid paths using DFS
    def dfs(pos, time, visited, path):
        if time == t:
            return [path]
        
        i, j = pos
        results = []
        
        # Try all 4 directions (up, down, left, right)
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            
            # Check if next position is valid
            if (0 <= ni < n and 0 <= nj < m and 
                (ni, nj) not in visited and 
                (ni, nj) in valid[time + 1]):
                
                visited.add((ni, nj))
                results.extend(dfs((ni, nj), time + 1, visited, path + grid[ni][nj]))
                visited.remove((ni, nj))
        
        return results
    
    # Try all possible starting positions
    all_keys = []
    for start_pos in valid[1]:
        visited = {start_pos}
        i, j = start_pos
        keys = dfs(start_pos, 1, visited, grid[i][j])
        all_keys.extend(keys)
    
    # Check if we have exactly one unique key
    unique_keys = list(set(all_keys))
    
    if len(unique_keys) == 1:
        print(unique_keys[0])
    else:
        print("Not enough clues")

solve()
