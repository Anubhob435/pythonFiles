def find_nearest_digits(N):
    digits = list(range(1, 10))  # 1 to 9
    digit1 = min(digits, key=lambda x: abs(x - N))
    digits.remove(digit1)
    digit2 = min(digits, key=lambda x: abs(x - N))
    return digit1, digit2

def generate_fibonacci(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib

def solve_fibonacci_sum(N):
    # Step 1: Find nearest digits
    digit1, digit2 = find_nearest_digits(N)
    
    # Step 2: Calculate product
    product = digit1 * digit2
    
    # Step 3: Generate Fibonacci sequence
    fib_sequence = generate_fibonacci(product)
    
    # Step 4: Calculate sum
    return sum(fib_sequence)

def test_cases():
    test_inputs = [3, 5, 7]
    for N in test_inputs:
        result = solve_fibonacci_sum(N)
        print(f"Input N = {N}")
        digit1, digit2 = find_nearest_digits(N)
        print(f"Nearest digits: {digit1}, {digit2}")
        print(f"Product: {digit1 * digit2}")
        print(f"Fibonacci sum: {result}")
        print()

if __name__ == "__main__":
    test_cases()