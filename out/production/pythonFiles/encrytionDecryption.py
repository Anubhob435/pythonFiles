def caesar_cipher():
    try:
        choice = input("Choose operation - Encrypt (E) / Decrypt (D): ").upper()
        if choice not in ['E', 'D']:
            raise ValueError("Invalid choice. Please enter 'E' or 'D'.")

        text = input("Enter the text: ")
        shift = int(input("Enter the shift value (integer): "))

        result = ""
        for char in text:
            if char.isalpha():
                offset = 65 if char.isupper() else 97
                if choice == 'E':
                    shifted_char = chr((ord(char) - offset + shift) % 26 + offset)
                else:
                    shifted_char = chr((ord(char) - offset - shift) % 26 + offset)

                result += shifted_char
                print(f"{char} -> {shifted_char}")
            else:
                result += char

        print(f"Result: {result}")
    except ValueError as ve:
        print(f"Error: {ve}")


# Diffie-Hellman Key Exchange Implementation

def diffie_hellman():
    try:
        p = int(input("Enter a prime number (p): "))
        g = int(input("Enter a primitive root (g): "))

        alice_private = int(input("Alice's private key: "))
        bob_private = int(input("Bob's private key: "))

        alice_public = (g ** alice_private) % p
        bob_public = (g ** bob_private) % p

        print(f"Alice's Public Key: {alice_public}")
        print(f"Bob's Public Key: {bob_public}")

        alice_shared_secret = (bob_public ** alice_private) % p
        bob_shared_secret = (alice_public ** bob_private) % p

        print(f"Alice's Shared Secret: {alice_shared_secret}")
        print(f"Bob's Shared Secret: {bob_shared_secret}")

        if alice_shared_secret == bob_shared_secret:
            print("Shared secret keys match!")
        else:
            print("Error: Shared secrets do not match!")
    except ValueError:
        print("Error: Invalid input! Please enter integers only.")


if __name__ == "__main__":
    print("1. Caesar Cipher")
    print("2. Diffie-Hellman Key Exchange")
    choice = input("Choose an option (1/2): ")

    if choice == '1':
        caesar_cipher()
    elif choice == '2':
        diffie_hellman()
    else:
        print("Invalid choice! Please select either 1 or 2.")
