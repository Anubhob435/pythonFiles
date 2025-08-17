l = int(input())
r = int(input())

range_list = []
score = 0

points = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]

for i in range(l, r + 1):
    range_list.append(i)
    
    
for j in points:
    if j in range_list:
        score += 1

print(score)