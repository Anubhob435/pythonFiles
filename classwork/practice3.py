def find_single_person(arr):

    result = 0
    for num in arr:
        result ^= num
    return result

# Test cases
if __name__ == "__main__":
    test_cases = [
        [1, 2, 3, 2, 1],    # should return 3
        [5, 5, 8, 8, 9],    # should return 9
        [1, 1, 2],          # should return 2
    ]
    
    for test in test_cases:
        print(f"Party: {test}")
        print(f"Single person: {find_single_person(test)}\n")