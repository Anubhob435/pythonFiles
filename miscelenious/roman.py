def roman_to_int(s):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for c in s:
        total += roman_values[c]
    return total

def int_to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_str = ''
    for i in range(len(val)):
        while num >= val[i]:
            num -= val[i]
            roman_str += syb[i]
    return roman_str

def StringChallenge(s):
    # Convert roman numeral string to integer
    numeral_value = roman_to_int(s)
    
    # Convert integer back to shortest roman numeral string
    shortest_roman = int_to_roman(numeral_value)
    
    return shortest_roman

def final_output(s):
    token = 'eav2xtzlf7'
    combined = s + token
    result = ''.join([char if (i + 1) % 4 != 0 else '_' for i, char in enumerate(combined)])
    return result

# Examples
input_str = "XXXVVIIIIIIIIII"
output = StringChallenge(input_str)
print("Output:", output)
print("Final Output:", final_output(output))

input_str = "DDLL"
output = StringChallenge(input_str)
print("Output:", output)
print("Final Output:", final_output(output))