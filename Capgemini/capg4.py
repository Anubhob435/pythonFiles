import random

#comitting to make sure that github streak is maintained
#comitting to make sure that github streak is maintained
#COMMITING TO KEEP GITHUB STREAK ON TRACK

def generate_random_quote():
    quotes = [
        "Life is like a box of chocolates.",
        "The only way to do great work is to love what you do.",
        "Be yourself; everyone else is already taken.",
        "Strive not to be a success, but rather to be of value."
    ]
    return random.choice(quotes)

def main():
    print("Random quote:")
    print(generate_random_quote())
    random_number = random.randint(1, 100)
    print("A random number between 1 and 100:", random_number)

if __name__ == "__main__":
    main()