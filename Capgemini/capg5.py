def find_nearest_number(arr, target):
    """Find number in array closest to target"""
    if not arr:
        return None
    return min(arr, key=lambda x: abs(x - target))

def generate_fibonacci(n):
    """Generate Fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib

def solve_nearest_fibonacci(arr, target, key):
    # Input validation
    if not arr or key < 0:
        return 0
        
    # Find nearest number
    nearest = find_nearest_number(arr, target)
    
    # Generate Fibonacci sequence
    fib_sequence = generate_fibonacci(key)
    
    # Calculate sum
    return sum(fib_sequence)

def test_cases():
    tests = [
        ([1, 5, 10, 15], 12, 5),
        ([2, 4, 6, 8], 5, 3),
        ([20, 30, 40], 25, 4),
        ([], 5, 3),  # Edge case: empty array
        ([1], 1, 0)  # Edge case: single element, zero key
    ]
    
    for arr, target, key in tests:
        print(f"\nTest Case:")
        print(f"Array: {arr}")
        print(f"Target: {target}")
        print(f"Key: {key}")
        
        result = solve_nearest_fibonacci(arr, target, key)
        if arr:
            nearest = find_nearest_number(arr, target)
            print(f"Nearest number to {target}: {nearest}")
        print(f"Fibonacci sum: {result}")

if __name__ == "__main__":
    test_cases()