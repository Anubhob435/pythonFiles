def is_palindrome(s):
    return s == s[::-1]

def StringChallenge(strParam):
    if is_palindrome(strParam):
        return strParam

    n = len(strParam)

    # Try removing one character at a time
    for i in range(n):
        temp = strParam[:i] + strParam[i+1:]
        if is_palindrome(temp) and len(temp) >= 3:
            return strParam[i]

    # Try removing two characters
    for i in range(n):
        for j in range(i+1, n):
            temp = strParam[:i] + strParam[i+1:j] + strParam[j+1:]
            if is_palindrome(temp) and len(temp) >= 3:
                return strParam[i] + strParam[j]

    return "not possible"

# Keep this function call here 
print(StringChallenge(input()))