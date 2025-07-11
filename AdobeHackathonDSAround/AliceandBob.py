def solve():
    n = int(input())
    alice = list(map(int, input().split()))
    bob = list(map(int, input().split()))
    
    if sorted(alice) != sorted(bob):
        print("NO")
        return
    
    if alice == bob:
        print("YES")
        return
    
    pos_alice = {}
    pos_bob = {}
    
    for i in range(n):
        pos_alice[alice[i]] = i
        pos_bob[bob[i]] = i
    
    perm = [0] * n
    for i in range(n):
        value = alice[i]
        target_pos = pos_bob[value]
        perm[i] = target_pos
    
    visited = [False] * n
    cycles = []
    
    for i in range(n):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = perm[j]
            if len(cycle) > 1:
                cycles.append(cycle)
    
    distances = set()
    for i in range(1, n):
        distances.add(i)
    
    def can_sort_cycle(cycle):
        if len(cycle) <= 2:
            return True
        
        for d in distances:
            positions = []
            for i in range(len(cycle)):
                for j in range(i + 1, len(cycle)):
                    if abs(cycle[i] - cycle[j]) == d:
                        positions.append((cycle[i], cycle[j]))
            if len(positions) >= len(cycle) // 2:
                return True
        
        return False
    
    for cycle in cycles:
        if not can_sort_cycle(cycle):
            print("NO");  
            return

    
    print("YES")

solve()