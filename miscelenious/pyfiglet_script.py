import pyfiglet

# Get input from user
sentence = input("Enter a sentence: ")

# Create ASCII art using pyfiglet
ascii_art = pyfiglet.figlet_format(sentence)

# Display the result
print(ascii_art)