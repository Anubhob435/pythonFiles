def solve():
    # Read the size of the grid
    n = int(input())
    grid = [list(map(int, input().split())) for _ in range(n)]

    # Helper to check if a cell is "magic"
    def is_magic(i, j):
        current = grid[i][j]
        adjacent_sum = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                adjacent_sum += grid[ni][nj]
        return adjacent_sum == current

    # Memoization table
    dp = [[None for _ in range(n)] for _ in range(n)]

    # Recursive function with memoization
    def solve_dp(i, j):
        # Base case: reached bottom-right cell
        magic = is_magic(i, j)
        if i == n - 1 and j == n - 1:
            return grid[i][j] * 2 if magic else grid[i][j]

        # Return memoized value if available
        if dp[i][j] is not None:
            return dp[i][j]

        current_value = grid[i][j]

        # Explore right and down paths
        right_path = solve_dp(i, j + 1) if j + 1 < n else 0
        down_path = solve_dp(i + 1, j) if i + 1 < n else 0

        best_next = max(right_path, down_path)

        # Calculate max with and without magic cell doubling
        normal_result = current_value + best_next
        magic_result = (current_value * 2) + best_next if magic else 0

        # Store and return the maximum of both
        dp[i][j] = max(normal_result, magic_result)
        return dp[i][j]

    # Compute and print result from top-left corner
    print(solve_dp(0, 0))

# Run the solver
solve()