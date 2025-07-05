def maxSubSquare(M):
    R = len(M)
    C = len(M[0])
    S = [[0]*C for _ in range(R)]

    max_of_s = 0
    max_i = 0
    max_j = 0

    for i in range(R):
        for j in range(C):
            if i == 0 or j == 0:
                S[i][j] = M[i][j]
            elif M[i][j] == 1:
                S[i][j] = min(S[i][j-1], S[i-1][j], S[i-1][j-1]) + 1
            else:
                S[i][j] = 0

            if S[i][j] > max_of_s:
                max_of_s = S[i][j]
                max_i = i
                max_j = j

    # Extract the sub-matrix
    result = []
    for i in range(max_i - max_of_s + 1, max_i + 1):
        row = []
        for j in range(max_j - max_of_s + 1, max_j + 1):
            row.append(M[i][j])
        result.append(row)
    return result

# Example usage:
M = [
    [1,0,0,1,0],
    [1,1,1,1,1],
    [1,0,1,1,1],
    [0,0,1,1,0],
    [1,1,1,1,1]
]
print(maxSubSquare(M))