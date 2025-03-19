def max_steal(houses):
    if not houses:
        return 0
    if len(houses) == 1:
        return houses[0]
    
    prev1 = 0
    prev2 = 0
    
    for money in houses:
        current = max(prev1, prev2 + money)
        prev2 = prev1
        prev1 = current
    
    return prev1

# Test case
houses = [100, 4000, 300, 4000, 9000, 600]
print(max_steal(houses))  # Output: 13000