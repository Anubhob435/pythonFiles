def robin_karp(text: str, pattern: str):
    if not pattern:
        return [0] if text else []
    base = 256
    m = len(pattern)
    n = len(text)
    h = 1
    for _ in range(m - 1):
        h = (h * base)
    p_hash = 0
    t_hash = 0
    result = []
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i]))
        t_hash = (base * t_hash + ord(text[i]))
    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i+m] == pattern:
                result.append(i)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m]))
    return result

print(robin_karp("AABAACAADAABAABA", "AABA"))  # Expected output: [0, 9, 12]