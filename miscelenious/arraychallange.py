def ArrayChallenge(num):
    def get_digits(n):
        return [int(d) for d in str(n)]

    digits = get_digits(num)  # Extract initial digits
    multiplications = 0

    while True:
        # Check for adjacent duplicate numbers
        for i in range(len(digits) - 1):
            if digits[i] == digits[i + 1]:  # Found adjacent duplicates
                return multiplications

        # Pick the first digit as the multiplier
        multiplier = digits[0]
        num *= multiplier  # Multiply num
        multiplications += 1

        # Extract new digits and replace the existing list
        digits = get_digits(num)  # Replace digits with new digits

# Test case
num = 8
print(ArrayChallenge(num))  # Output should be 3