def greet(name):
    """A simple function that prints a greeting message"""
    return f"Hello, {name}!"

def main():
    # Example usage
    user_name = input("Enter your name: ")
    message = greet(user_name)
    print(message)

if __name__ == "__main__":
    main()