n = int(input())
second_input = list(map(int, input().split()))

overlap = []
range_x_y = []

for i in range(second_input[0], second_input[1] + 1):
    range_x_y.append(i)
    overlap.append(0)
     
print(range_x_y)

ranges = []

for i in range(n):
    ranges.append(list(map(int, input().split())))

for u in range_x_y:
    for v in ranges:
        for j in range(v[0], v[1] + 1):
            if u == j:
                overlap[range_x_y.index(u)] += 1

print(overlap)
print(sum(overlap))