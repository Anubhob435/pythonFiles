n, m = map(int, input("Enter the size of the grid (N M): ").split())

grid = []
for _ in range(n):
    grid.append(list(map(int, input().split())))

    # Change all values in the last row to 1
grid[n - 1] = [1] * m

print(grid)

a, b = map(int, input("Starting coordinates: ").split())
c, d = map(int, input("Enter destination: ").split())

count = 0

while True:
    if grid[a+1][b] != 1:
        if a != n:   
            count += 1
            a+=1
    
print(count)
print(a, b)
