def dec_to_n_base(n, num):

    if num == 0:
        return "0"
    
    # Digits used for representation (0-9, A-Z)
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Validate base is within allowed range
    if n < 2 or n > len(digits):
        raise ValueError(f"Base must be between 2 and {len(digits)}")
        
    result = []
    while num > 0:
        result.append(digits[num % n])
        num //= n
    return "".join(reversed(result))

# Test cases
if __name__ == "__main__":
    print(f"Decimal 10 in binary (base 2): {dec_to_n_base(2, 10)}")     # Should output: 1010
    print(f"Decimal 15 in hex (base 16): {dec_to_n_base(16, 15)}")      # Should output: F
    print(f"Decimal 255 in hex (base 16): {dec_to_n_base(16, 255)}")    # Should output: FF
    print(f"Decimal 125 in base 7: {dec_to_n_base(7, 125)}")            # Should output: 236
    print(f"Decimal 0 in any base: {dec_to_n_base(16, 0)}")             # Should output: 0
