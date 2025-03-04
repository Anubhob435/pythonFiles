def product_smallestpair(target_sum, arr):
    if not arr:
        return -1
    if len(arr) < 2:
        return 0

    arr.sort()
    if arr[0] + arr[1] <= target_sum:
        return arr[0] * arr[1]
    return 0

# Test case
if __name__ == "__main__":
    print(product_smallestpair(5, [1, 2, 3, 4]))  # Expected output: 2 (1*2)