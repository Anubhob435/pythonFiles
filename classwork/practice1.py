def rotate_array(arr=None, d=1):
    if not arr:
        return []
    
    n = len(arr)
    if n == 0 or d == 0:
        return arr
        
    d = d % n
    
    return arr[-d:] + arr[:-d]

if __name__ == "__main__":
    # Test cases
    test_array = [1, 2, 3, 4, 5]
    print(f"Original array: {test_array}")
    print(f"Rotated by 2: {rotate_array(test_array, 2)}")  # Output: [4, 5, 1, 2, 3]