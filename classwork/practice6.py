def has_pair_with_sum(arr, target):
    seen = set()
    for num in arr:
        complement = target - num
        if complement in seen:
            return True, (complement, num)
        seen.add(num)
    return False, None

# Test case
arr = [0, -1, 2, -3, 1, -4]
target = -2
found, pair = has_pair_with_sum(arr, target)
print(f"Found pair: {found}")  # Expected output: True
print(f"Numbers: {pair}")      # Expected output: (-3, 1)