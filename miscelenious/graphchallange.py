from collections import defaultdict, deque

def GraphChallenge(strarr):
    # Create an adjacency list representation of the graph
    graph = defaultdict(list)
    for path in strarr:
        node1, node2 = path.split('-')
        graph[node1].append(node2)
        graph[node2].append(node1)

    # Perform BFS to find the longest path
    max_path_length = 0
    for node in graph:
        queue = deque([(node, 0)])  # (node, path_length)
        visited = set()
        while queue:
            current_node, path_length = queue.popleft()
            if current_node not in visited:
                visited.add(current_node)
                max_path_length = max(max_path_length, path_length)
                for neighbor in graph[current_node]:
                    queue.append((neighbor, path_length + 1))

    return max_path_length

print(GraphChallenge(["b-e", "b-c","c-d", "a-b", "e-f"]))  # Output: 4
print(GraphChallenge(["b-a", "c-e", "b-c", "d-c"]))  # Output: 3
