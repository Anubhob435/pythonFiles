def max_people(N):
    # Initialize k to 1
    k = 1
    
    # Keep increasing k until sum exceeds N
    while (k * (k + 1)) // 2 <= N:
        k += 1
    
    # Since we went one step too far, return k-1
    return k - 1

# Test cases
def test_cases():
    test_inputs = [10, 5, 3, 15]
    for N in test_inputs:
        result = max_people(N)
        print(f"Input N = {N}")
        print(f"Output: {result}")
        print()

# Run test cases
if __name__ == "__main__":
    test_cases()