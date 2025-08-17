def get_distance_from_target(number, target):
    return abs(number - target)

def find_k_closest(arr, t, k):
    # Create list of (number, distance) pairs
    distances = []
    for num in arr:
        distance = get_distance_from_target(num, t)
        distances.append((num, distance))
    
    # Sort by distance
    distances.sort(key=lambda pair: pair[1])
    
    # Take first k numbers
    result = []
    for i in range(k):
        result.append(distances[i][0])
    
    return result

def calculate_product(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def generate_fibonacci_up_to(n):
    if n <= 0:
        return []
    
    fib = [0, 1]
    while fib[-1] <= n:
        fib.append(fib[-1] + fib[-2])
    return fib[:-1]  # Remove last number that exceeded n

def solve_min_diff_fibonacci(arr, t, k):
    # Step 1: Find k closest elements
    closest_elements = find_k_closest(arr, t, k)
    
    # Step 2: Calculate their product
    product = calculate_product(closest_elements)
    
    # Step 3: Generate Fibonacci sequence up to product
    fib_sequence = generate_fibonacci_up_to(product)
    
    # Step 4: Calculate sum
    return sum(fib_sequence)

def test_cases():
    test_cases = [
        ([1, 2, 3, 4, 5], 3, 2),
        ([10, 20, 30, 40, 50], 25, 3),
        ([5, 10, 15, 20], 12, 2)
    ]
    
    for arr, t, k in test_cases:
        result = solve_min_diff_fibonacci(arr, t, k)
        closest = find_k_closest(arr, t, k)
        product = calculate_product(closest)
        print(f"Array: {arr}")
        print(f"Target: {t}")
        print(f"K: {k}")
        print(f"K closest elements: {closest}")
        print(f"Their product: {product}")
        print(f"Fibonacci sum: {result}")
        print()

if __name__ == "__main__":
    test_cases()