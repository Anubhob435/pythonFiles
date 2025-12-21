stack_a = []
stack_b = []

g = int(input())

def twoStacks(maxSum, a, b):
    sum_a = 0
    count_a = 0

    while count_a < len(a) and sum_a + a[count_a] <= maxSum:
        sum_a += a[count_a]
        count_a += 1

    max_count = count_a

    sum_b = 0
    count_b = 0

    while count_b < len(b):
        sum_b += b[count_b]
        count_b += 1

        if sum_b > maxSum:
            break

        while sum_a + sum_b > maxSum and count_a > 0:
            count_a -= 1
            sum_a -= a[count_a]

        max_count = max(max_count, count_a + count_b)

    return max_count
        