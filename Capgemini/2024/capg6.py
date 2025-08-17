def solve(N, heights):
    count = 1  # First building can always watch sunset
    max_height = heights[0]
    
    for i in range(1, N):
        if heights[i] > max_height:
            count += 1
            max_height = heights[i]
    
    print(count)
    
N = 5
Heights = [9, 11, 10, 8, 13]

solve(N, Heights)