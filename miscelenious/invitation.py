import random
import datetime

bride_names = ["Aarohi", "Meera", "Sarah", "Isha", "Ananya"]
groom_names = ["Arjun", "Rohan", "Kabir", "Aditya", "Vikram"]

venues = [
    "The Grand Palace, Mumbai",
    "Riverside Pavilion, Goa",
    "Royal Heritage Hall, Jaipur",
    "Sunset Gardens, Kerala",
    "Emerald Banquet, Kolkata"
]

themes = [
    "Classic Elegance ✨",
    "Royal Maharaja Style 👑",
    "Beachside Bliss 🌊",
    "Fairy Light Dream ✨",
    "Floral Fantasy 🌸"
]

messages = [
    "Two hearts about to become one.",
    "Join us in celebrating love and new beginnings.",
    "Your presence will make our day even more special!",
    "A journey of love begins with your blessings.",
    "Come witness the magic of love and togetherness!"
]

def generate_wedding_invite():
    bride = random.choice(bride_names)
    groom = random.choice(groom_names)
    venue = random.choice(venues)
    theme = random.choice(themes)
    message = random.choice(messages)

    wedding_date = datetime.date(2025, random.randint(1, 12), random.randint(1, 28))

    invite = f"""
    ╔════════════════════════════════════════╗
               💍  WEDDING INVITATION  💍
    ╚════════════════════════════════════════╝

        {bride}  ❤️  {groom}
              REQUEST YOUR PRESENCE

        📅 Date : {wedding_date.strftime('%B %d, %Y')}
        📍 Venue: {venue}
        🎨 Theme: {theme}

        ✉️  {message}

    ╔════════════════════════════════════════╗
             We hope to see you there!
    ╚════════════════════════════════════════╝
    """

    return invite


print(generate_wedding_invite())