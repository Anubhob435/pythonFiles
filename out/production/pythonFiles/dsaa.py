import pyfiglet
import time

def show_word_in_figlet(word):
    # Render the word in figlet style
    ascii_art = pyfiglet.figlet_format(word, font="roman")
    print(ascii_art)

def read_lyrics_and_show_figlet(file_path):
    try:
        # Open the lyrics.txt file
        with open(file_path, 'r') as file:
            # Read the entire content of the file
            lyrics = file.read()

            # Split the text into individual words
            words = lyrics.split()

            # Loop through each word and display it in figlet
            for word in words:
                show_word_in_figlet(word)
                time.sleep(0.4)  # Optional: Pause between words for better visualization
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the lyrics.txt file
file_path = 'lyrics.txt'

# Call the function to read lyrics and display in figlet
read_lyrics_and_show_figlet(file_path)
#nothing comit
