def rotate_from_index(arr, d):

    # Handle edge cases
    if not arr or d >= len(arr) or d < 0:
        return arr
        
    # Store value at d
    temp = arr[d]
    
    # Shift elements left
    for i in range(d, len(arr)-1):
        arr[i] = arr[i+1]
    
    # Place temp at end
    arr[-1] = temp
    
    return arr

# Test cases
if __name__ == "__main__":
    test_array = [1, 2, 3, 4, 5]
    print(f"Original array: {test_array}")
    print(f"After rotation from index 2: {rotate_from_index(test_array.copy(), 2)}")  # [1, 2, 4, 5, 3]
    
    # Edge cases
    print(f"Empty array: {rotate_from_index([], 1)}")  # []
    print(f"Invalid index: {rotate_from_index([1, 2, 3], 5)}")  # [1, 2, 3]