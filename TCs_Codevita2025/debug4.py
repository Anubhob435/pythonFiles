def debug_test_case_2():
    grid = [
        ['*', '%', '*'],
        ['#', '+', '$'],
        ['$', '*', '+'],
        ['%', '#', '*'],
        ['+', '$', '#'],
        ['#', '*', '%']
    ]
    n, m = 6, 3
    start_r, start_c = 3, 2
    values = [5, 9, 4, 1]  # Pearl, Platinum, Gold, Diamond
    k = 5
    
    treasure_values = {
        '$': values[0],  # Pearl = 5
        '*': values[1],  # Platinum = 9  
        '%': values[2],  # Gold = 4
        '+': values[3],  # Diamond = 1
        '#': 0,          # Rock
        ' ': 0           # Empty space
    }
    
    def is_valid(r, c):
        return 0 <= r < n and 0 <= c < m
    
    def is_stable(r, c):
        if r == n - 1:  # Last row is always stable
            return True
        if is_valid(r + 1, c) and grid[r + 1][c] == '#':
            return True
        return False
    
    print("Starting position:", start_r, start_c)
    print("Starting cell value:", grid[start_r][start_c], "=", treasure_values[grid[start_r][start_c]])
    print("Is starting position stable?", is_stable(start_r, start_c))
    
    # Check possible moves
    print("\nChecking possible moves:")
    
    # Left move
    left_r, left_c = start_r, start_c - 1
    if is_valid(left_r, left_c):
        print(f"Left ({left_r},{left_c}): {grid[left_r][left_c]} - Valid: {grid[left_r][left_c] != '#'}")
        if grid[left_r][left_c] != '#':
            print(f"  Is stable: {is_stable(left_r, left_c)}")
    else:
        print("Left: Out of bounds")
    
    # Right move  
    right_r, right_c = start_r, start_c + 1
    if is_valid(right_r, right_c):
        print(f"Right ({right_r},{right_c}): {grid[right_r][right_c]} - Valid: {grid[right_r][right_c] != '#'}")
        if grid[right_r][right_c] != '#':
            print(f"  Is stable: {is_stable(right_r, right_c)}")
    else:
        print("Right: Out of bounds")
    
    # Up move
    up_r, up_c = start_r - 1, start_c
    if is_valid(up_r, up_c):
        print(f"Up ({up_r},{up_c}): {grid[up_r][up_c]} - Valid: {grid[up_r][up_c] != '#'}")
        if grid[up_r][up_c] != '#':
            print(f"  Is stable: {is_stable(up_r, up_c)}")
    else:
        print("Up: Out of bounds")

debug_test_case_2()