def max_subarray_sum(nums):
    max_ending = max_so_far = nums[0]
    for x in nums[1:]:
        max_ending = max(x, max_ending + x)
        max_so_far = max(max_so_far, max_ending)
    return max_so_far

if __name__ == "__main__":
    arr = [1, -3, 2, 1, -1, 3, -2]
    print(max_subarray_sum(arr))