def ArrayChallenge(num):
    def get_digits(n):
        return [int(d) for d in str(n)]
    
    digits = get_digits(num)
    multiplications = 0
    
    while True:
        # Check for adjacent duplicates
        for i in range(len(digits) - 1):
            if digits[i] == digits[i + 1]:
                return multiplications
        
        # If no duplicates, multiply by one of its digits
        # Choose the first digit for simplicity
        multiplier = digits[0]
        new_num = num * multiplier
        new_digits = get_digits(new_num)
        
        # Append new digits to the list
        digits.extend(new_digits)
        num = new_num
        multiplications += 1

# Test cases
#print(ArrayChallenge(8))    # Output: 3
print(ArrayChallenge(198))  # Output: 2
#print(ArrayChallenge(134))  # Output: 1
#print(ArrayChallenge(46))   # Output: 2