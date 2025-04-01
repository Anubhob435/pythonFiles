# creating user profile
import random
import mysql.connector
import sys

# Initialize global variables with default values
ph_no = None
Name = None
Passw = None
date_of_b = None
balance = 0
records = {}
passwords = {}
birthday = {}

def connect_to_database():
    """Establish a connection to the database with error handling"""
    try:
        mydb = mysql.connector.connect(host="buh89x1pi8cgvaw4161i-mysql.services.clever-cloud.com",
                                    user="ucwyejivetooukiz",
                                    password="aAo8DieytbUo0FiYV4RY",
                                    database="buh89x1pi8cgvaw4161i")
        if mydb.is_connected():
            print("Connection established")
            return mydb
        else:
            print("Failed to connect to database")
            return None
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error connecting to database: {e}")
        return None

def close_database_connection(mydb, cursor=None):
    """Safely close database connection and cursor"""
    try:
        if cursor:
            cursor.close()
        if mydb and mydb.is_connected():
            mydb.close()
            print("MySQL connection is closed")
    except mysql.connector.Error as e:
        print(f"Error closing database connection: {e}")
    except Exception as e:
        print(f"Unexpected error closing connection: {e}")

def get_user_numeric_input(prompt, digits=None, error_msg=None):
    """Get validated numeric input from the user"""
    while True:
        try:
            user_input = input(prompt)
            if not user_input.isdigit():
                print(error_msg or "Please enter a numeric value")
                continue
            if digits and len(user_input) != digits:
                print(f"Input must be {digits} digits long")
                continue
            return user_input
        except Exception as e:
            print(f"Error with input: {e}")

def complete_program():
    def old_user():
        global ph_no, Name, Passw, date_of_b, balance
        
        while True:
            q = get_user_numeric_input("Please enter your registered phone number: ", 
                                      digits=10, 
                                      error_msg="Enter a 10 digit number")
            
            mydb = None
            cursor = None
            try:
                mydb = connect_to_database()
                if not mydb:
                    print("Cannot proceed without database connection. Please try again later.")
                    continue
                
                cursor = mydb.cursor()
                sql_select_Query = """select * from abc WHERE phone = %s"""
                cursor.execute(sql_select_Query, (q,))
                user_records = cursor.fetchall()
                
                if cursor.rowcount == 0:
                    print("No user found with this phone number. Please try again or create a new account.")
                    continue
                
                print("User found!")
                for row in user_records:
                    ph_no = row[0]
                    Name = row[1]
                    Passw = row[2]
                    date_of_b = row[3]
                    balance = row[4]

                login_attempts = 0
                while login_attempts < 3:
                    pass2 = input("Enter password: ")
                    if pass2 == Passw:
                        print(f"Welcome, {Name}")
                        print(f"Your account balance is: {balance}")
                        break
                    else:
                        login_attempts += 1
                        if login_attempts < 3:
                            print(f"Incorrect password. {3 - login_attempts} attempts remaining.")
                            print("1. Try again 2. Show password hint")
                            try:
                                abc = int(input("> "))
                                if abc == 1:
                                    continue
                                elif abc == 2:
                                    a2 = input("Your birthday in DD.MM.YYYY format: ")
                                    if date_of_b == a2:
                                        print(f"Your password is: {Passw}")
                                        break
                                    else:
                                        print("Incorrect birthday")
                                        continue
                                else:
                                    print("Invalid option")
                            except ValueError:
                                print("Please enter a number")
                                continue
                        else:
                            print("Too many failed attempts. Please try again later.")
                            return
                
                if login_attempts < 3:  # Successfully logged in
                    break
                    
            except mysql.connector.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally:
                close_database_connection(mydb, cursor)

    def new_user2():
        print("Welcome to NO MALL. Let's start by making an account")
        
        p = input("Your Full name: ")
        if not p.strip():
            print("Name cannot be empty")
            return

        while True:
            phone_number = get_user_numeric_input("Enter Phone Number: ", 
                                                digits=10, 
                                                error_msg="Enter a valid 10 digit number")
            
            mydb = None
            cursor = None
            try:
                mydb = connect_to_database()
                if not mydb:
                    print("Database connection failed. Please try again later.")
                    return
                
                cursor = mydb.cursor()
                sql_select_Query = """select * from abc WHERE phone = %s"""
                cursor.execute(sql_select_Query, (phone_number,))
                user_records = cursor.fetchall()
                
                if cursor.rowcount != 0:
                    print("This phone number is already registered.")
                    print("1. Sign in 2. Sign up with different number")
                    try:
                        g = int(input("> "))
                        if g == 1:
                            old_user()
                            break
                        elif g == 2:
                            continue
                        else:
                            print("Invalid option, please try again")
                            continue
                    except ValueError:
                        print("Please enter a number")
                        continue
                else:
                    # Phone number is available, proceed with registration
                    apass = input("Enter New password: ")
                    if not apass:
                        print("Password cannot be empty")
                        continue
                        
                    date = input("Enter date of birth as DD.MM.YYYY: ")
                    # Add date format validation here if needed
                    
                    bal = 3000
                    
                    try:
                        record = (phone_number, p, apass, date, bal)
                        query = """INSERT INTO abc (phone, name, password, dob, balance) VALUES (%s, %s, %s, %s, %s)"""
                        cursor.execute(query, record)
                        mydb.commit()
                        
                        print("Account created successfully!")
                        print(f"Welcome {p}")
                        print("As a welcome bonus you are given 3000 to spend")
                        
                        # Set global variables for the new user
                        global ph_no, Name, Passw, date_of_b, balance
                        ph_no = phone_number
                        Name = p
                        Passw = apass
                        date_of_b = date
                        balance = bal
                        
                        break
                    except mysql.connector.Error as e:
                        print(f"Failed to create account: {e}")
                        mydb.rollback()
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                        mydb.rollback()
            except mysql.connector.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally:
                close_database_connection(mydb, cursor)

    # Start the main program
    print("""
    Hello and welcome
    1. New user
    2. Old user""")

    while True:
        try:
            user_choice = input("> ")
            if not user_choice.isdigit():
                print("Please enter a number")
                continue
                
            user_choice = int(user_choice)
            if user_choice == 1:
                new_user2()
                break
            elif user_choice == 2:
                old_user()
                break
            else:
                print("Invalid option")
                print("""1. New user
    2. Old user""")
                continue
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # Shopping section
    if ph_no is None:
        print("You need to be logged in to shop")
        return

    items = []
    values = []
    quantity2 = []
    temporary_dict = {}
    gg = {1: "apple", 2: "mango", 3: "eggs", 4: "milk"}
    available = {"apple": 200, 'mango': 100, 'eggs': 120, "milk": 50}
    
    print("Let's get to shopping!")
    print("Here are the list of items:")
    print("1. apple: rs. 200/kg")
    print("2. mango: rs. 100/kg")
    print("3. eggs: rs. 120/dozen")
    print("4. milk: rs. 50/litre")
    
    choice = '+'
    while True:
        if choice == '+':
            try:
                item = int(input("What do you want (enter item number): "))
                if item not in gg:
                    print("Invalid item number. Please select from 1-4.")
                    continue
                    
                quantity = input("How much/many: ")
                if not quantity.isdigit() or int(quantity) <= 0:
                    print("Please enter a valid positive quantity")
                    continue
                    
                quantity = int(quantity)
                quantity2.append(quantity)
                
                ll = gg.get(item)
                temporary_dict[ll] = quantity
                
                items.append(ll)
                x = available.get(ll)
                values.append(x * quantity)
                
                j = input("'+' to continue shopping '-' to exit shopping: ")
                choice = j
            except ValueError:
                print("Please enter valid numbers")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '-':
            break
        else:
            print("Invalid choice. Press '+' to continue or '-' to exit.")
            choice = input("> ")
    
    # Calculate total and update balance
    total_cost = sum(values)
    new_balance = balance - total_cost
    
    mydb = None
    cursor = None
    try:
        mydb = connect_to_database()
        if not mydb:
            print("Failed to connect to database. Your order is processed but balance is not updated.")
        else:
            cursor = mydb.cursor()
            query = """UPDATE abc SET balance = %s WHERE phone = %s"""
            values_to_update = (new_balance, ph_no)
            cursor.execute(query, values_to_update)
            mydb.commit()
            print("Balance updated successfully")
    except mysql.connector.Error as e:
        print(f"Database error when updating balance: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        close_database_connection(mydb, cursor)

    # Show receipt and remaining balance
    if total_cost <= balance:
        print("\nYour items: ")
        for item, qty in temporary_dict.items():
            print(f"{item}: {qty} unit(s)")
        
        print("\nBonus time! Chance to win 50% discount!")
        try:
            g = random.randint(1, 5)
            l = int(input("Guess a random number between 1 and 5: "))
            
            if g == l:
                discount = total_cost * 0.5
                final_cost = total_cost - discount
                print(f"Congratulations! You saved {discount} 🥳")
                print(f"Your total: {final_cost}")
            else:
                print("Sorry, no discount today ☹")
                print(f"Your total: {total_cost}")
                
            print(f"Remaining balance: {new_balance}")
        except ValueError:
            print("Invalid input for guessing. No discount applied.")
            print(f"Your total: {total_cost}")
            print(f"Remaining balance: {new_balance}")
    else:
        print(f"Sorry! We cannot complete your purchase as you are short of {abs(new_balance)} rupees.")
        print("Please remove some items or add funds to your account.")

    print("Thank you for shopping with us! 🙏")

def main():
    try:
        while True:
            complete_program()
            try:
                continue_shopping = input("Would you like to shop again? (y/n): ").lower()
                if continue_shopping != 'y':
                    print("Thank you for using our shopping system. Goodbye!")
                    break
            except Exception:
                print("Invalid input. Exiting program.")
                break
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Exiting program. Have a nice day!")

if __name__ == "__main__":
    main()
