def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"

# Test the function
print(divide_numbers(10, 2))  # Normal division
print(divide_numbers(10, 0))  # Attempting division by zero