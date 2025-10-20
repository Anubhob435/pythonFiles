# Diwali Greeting Card Generator

import pyfiglet
from termcolor import cprint, colored
import datetime

# Get current date
today = datetime.date.today()
diwali_message = "Happy Diwali!"

# Recipient name input
recipient = input("Enter the recipient's name: ")

# Create Diwali ASCII art
ascii_art = pyfiglet.figlet_format(diwali_message)
cprint(ascii_art, 'yellow')

# Print festive message
cprint(f"\nWishing you lots of happiness, prosperity, and joy this Diwali, {recipient}!", 'green')
cprint("May the festival of lights bring brightness to your life!", 'magenta')
cprint(f"Date: {today}", 'cyan')

cprint("\n🪔🪔🪔\n", 'red')
