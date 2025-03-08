def find_smallest_number(numbers):
    if not numbers:
        return None
    return min(numbers)

sample_list = [10, 2, 5, 1, -7, 13]
print(find_smallest_number(sample_list))  # Output: -7