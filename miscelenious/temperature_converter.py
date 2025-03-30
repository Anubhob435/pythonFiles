def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin."""
    celsius = fahrenheit_to_celsius(fahrenheit)
    return celsius_to_kelvin(celsius)

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    celsius = kelvin_to_celsius(kelvin)
    return celsius_to_fahrenheit(celsius)

def get_valid_temperature():
    """Get a valid temperature input from the user."""
    while True:
        try:
            temp = float(input("Enter the temperature value: "))
            return temp
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_menu():
    """Display the temperature conversion menu."""
    print("\nTemperature Converter")
    print("---------------------")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")
    print("7. Exit")

def main():
    """Main function to run the temperature converter."""
    while True:
        display_menu()
        
        try:
            choice = int(input("\nEnter your choice (1-7): "))
            
            if choice == 7:
                print("Thank you for using the Temperature Converter. Goodbye!")
                break
                
            if choice < 1 or choice > 7:
                print("Invalid choice. Please select a number between 1 and 7.")
                continue
                
            temperature = get_valid_temperature()
            
            if choice == 1:
                result = celsius_to_fahrenheit(temperature)
                print(f"{temperature}°C = {result:.2f}°F")
            elif choice == 2:
                result = fahrenheit_to_celsius(temperature)
                print(f"{temperature}°F = {result:.2f}°C")
            elif choice == 3:
                result = celsius_to_kelvin(temperature)
                print(f"{temperature}°C = {result:.2f}K")
            elif choice == 4:
                result = kelvin_to_celsius(temperature)
                print(f"{temperature}K = {result:.2f}°C")
            elif choice == 5:
                result = fahrenheit_to_kelvin(temperature)
                print(f"{temperature}°F = {result:.2f}K")
            elif choice == 6:
                result = kelvin_to_fahrenheit(temperature)
                print(f"{temperature}K = {result:.2f}°F")
                
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
