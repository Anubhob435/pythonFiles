def SearchingChallenge(strArr):
    # Convert the input array into a matrix
    matrix = [list(map(int, row)) for row in strArr]
    
    # Get the dimensions of the matrix
    rows, cols = len(matrix), len(matrix[0])
    
    # Define the directions for DFS
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    # Initialize the memoization table
    memo = [[0] * cols for _ in range(rows)]
    
    def dfs(r, c):
        # If the result is already memoized, return it
        if memo[r][c] != 0:
            return memo[r][c]
        
        # Initialize the longest path length to 1
        longest_path = 1
        
        # Explore all possible directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check if the new position is within the matrix bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the new position has a larger value
                if matrix[nr][nc] > matrix[r][c]:
                    # Recursively explore the new position
                    longest_path = max(longest_path, dfs(nr, nc) + 1)
        
        # Memoize the result
        memo[r][c] = longest_path
        return longest_path
    
    # Initialize the longest path length to 0
    longest_path = 0
    
    # Explore all positions in the matrix
    for r in range(rows):
        for c in range(cols):
            longest_path = max(longest_path, dfs(r, c))
    
    return longest_path - 1

print(SearchingChallenge(["12256", "56219", "43215"]))  # Output: 5
print(SearchingChallenge(["67", "21", "45"]))  # Output: 3
