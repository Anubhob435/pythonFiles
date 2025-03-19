def compress_string(s):
    # Dictionary to store character frequencies
    char_freq = {}
    
    # Parse the input string
    i = 0
    while i < len(s):
        # Get the character
        char = s[i]
        
        # Find the number that follows
        i += 1
        num = ""
        while i < len(s) and s[i].isdigit():
            num += s[i]
            i += 1
        
        # Add to dictionary, combining frequencies if char exists
        freq = int(num)
        char_freq[char] = char_freq.get(char, 0) + freq
    
    # Create compressed string with sorted characters
    result = ""
    for char in sorted(char_freq.keys()):
        result += char + str(char_freq[char])
    
    return result

# Test cases
test_strings = [
    "a3b2c1a2",      # Should become "a5b2c1"
    "b1a2c3b4",      # Should become "a2b5c3"
    "z2a1z1",        # Should become "a1z3"
]

for test in test_strings:
    print(f"Input: {test}")
    print(f"Output: {compress_string(test)}\n")
