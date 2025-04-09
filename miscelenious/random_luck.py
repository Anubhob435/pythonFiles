import random

def lucky_draw():
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print("Welcome to the Lucky Number Game!")
    print(f"Guess a number between 1 and 100. You have {max_attempts} attempts.")

    while attempts < max_attempts:
        try:
            # Get player's guess
            guess = int(input("Enter your guess: "))
            attempts += 1

            # Check the guess
            if guess == secret_number:
                print(f"Congratulations! You won in {attempts} attempts!")
                return
            elif guess < secret_number:
                print("Too low! Try again.")
            else:
                print("Too high! Try again.")
            
            print(f"Attempts remaining: {max_attempts - attempts}")

        except ValueError:
            print("Please enter a valid number!")
            
    print(f"Game Over! The number was {secret_number}")

if __name__ == "__main__":
    lucky_draw()