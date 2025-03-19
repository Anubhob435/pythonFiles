# creating user profile
import random
import mysql.connector

mydb = mysql.connector.connect(host="buh89x1pi8cgvaw4161i-mysql.services.clever-cloud.com",
                               user="ucwyejivetooukiz",
                               password="aAo8DieytbUo0FiYV4RY",
                               database="buh89x1pi8cgvaw4161i")

cursor = mydb.cursor()

if mydb.is_connected():
    print("Connection established")

if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")
records = {}
passwords = {}
birthday = {}


def complete_program():

    def old_user():
        while True:
            global q
            q = input("please enter your registered phone number: ")
            if len(q) != 10:
                print("enter a 10 digit number")
                continue
            elif q.isnumeric() and len(q) == 10:
                try:
                    mydb = mysql.connector.connect(host="buh89x1pi8cgvaw4161i-mysql.services.clever-cloud.com",
                                                   user="ucwyejivetooukiz",
                                                   password="aAo8DieytbUo0FiYV4RY",
                                                   database="buh89x1pi8cgvaw4161i")

                    sql_select_Query = """select * from abc WHERE phone = %s"""
                    cursor = mydb.cursor()
                    cursor.execute(sql_select_Query, (q,))
                    records = cursor.fetchall()
                    print("Total number of rows in table: ", cursor.rowcount)

                    print("\nPrinting each row")
                    global ph_no
                    global Name
                    global Passw
                    global date_of_b
                    global balance
                    for row in records:
                        ph_no = row[0]
                        Name = row[1]
                        Passw = row[2]
                        date_of_b = row[3]
                        balance = row[4]
                        print(ph_no, Name, Passw, date_of_b, balance)

                except mysql.connector.Error as e:
                    print("Error reading data from MySQL table", e)

                while True:
                    if ph_no is None:
                        print("no user found...")
                        old_user()
                    else:
                        pass2 = input("Enter password: ")
                        if pass2 == Passw:
                            print("welcome", Name)
                            print("your account balance is: ", balance)
                        else:
                            print("1.Try again 2.show password")
                            abc = int(input(">"))
                            if abc == 1:
                                continue
                            elif abc == 2:
                                a2 = input("Your birthday in DD.MM.YYY format: ")
                                if birthday.get(int(q)) == a2:
                                    print("Your password is: ", passwords.get(int(q)))
                                    old_user()
                                else:
                                    continue
                        break
                    break
                break

            else:
                print("Enter a valid 10 digit number")
                continue

    def new_user():
        global p
        p = input("Your Full name: ")
        while True:
            phone_number = input("Enter Phone Number")
            if len(phone_number) != 10:
                print("Enter a valid number")
                continue
            elif phone_number.isnumeric() and len(phone_number) == 10:
                print("account has been created")
                print(f"welcome {p} ")
                records[int(phone_number)] = p
                balance[p] = 3000
                print("As a welcome bonus you are given 3000 to spend")
                return str(p)
            else:
                print("Enter a valid 10 digit number")
                continue

    def new_user2():
        print("Welcome to NO MALL lets start by making an account")
        global p
        p = input("Your Full name: ")

        while True:
            global phone_number
            phone_number = input("Enter Phone Number: ")
            if len(phone_number) != 10:
                print("Enter a valid number")
                continue
            elif len(phone_number) == 10 and phone_number.isnumeric():
                q = phone_number

                try:
                    mydb = mysql.connector.connect(host="buh89x1pi8cgvaw4161i-mysql.services.clever-cloud.com",
                                                   user="ucwyejivetooukiz",
                                                   password="aAo8DieytbUo0FiYV4RY",
                                                   database="buh89x1pi8cgvaw4161i")

                    sql_select_Query = """select * from abc WHERE phone = %s"""
                    cursor = mydb.cursor()
                    cursor.execute(sql_select_Query, (q,))
                    records = cursor.fetchall()
                    print("Total number of rows in table: ", cursor.rowcount)

                    print("\nPrinting each row")
                    global ph_no
                    global Name
                    global Passw
                    global date_of_b
                    global balance
                    for row in records:
                        ph_no = row[0]
                        Name = row[1]
                        Passw = row[2]
                        date_of_b = row[3]
                        balance = row[4]
                        print(ph_no, Name)

                except mysql.connector.Error as e:
                    print("Error reading data from MySQL table", e)

                if cursor.rowcount != 0:
                    print("The number is already registered.\n"
                          "1.Sign in 2.Sign up with different number: ")
                    g = int(input(">"))
                    if g == 1:
                        old_user()
                        break
                    elif g == 2:
                        new_user2()
                elif cursor.rowcount == 0:
                    global apass
                    apass = input("Enter New password: ")
                    passwords[int(phone_number)] = apass
                    global date
                    date = input("Enter date of birth as DD.MM.YYYY: ")
                    birthday[int(phone_number)] = date
                    print("account has been created")
                    print(f"welcome {p} ")
                    print("As a welcome bonus you are given 3000 to spend")
                    global ph
                    ph = phone_number
                    bal = 3000
                    try:
                        mydb = mysql.connector.connect(host="buh89x1pi8cgvaw4161i-mysql.services.clever-cloud.com",
                                                       user="ucwyejivetooukiz",
                                                       password="aAo8DieytbUo0FiYV4RY",
                                                       database="buh89x1pi8cgvaw4161i")

                        cursor = mydb.cursor()
                        record = (ph, p, apass, date, bal)
                        quary = """INSERT INTO abc (phone, name, password, dob, balance) VALUES (%s, %s, %s, %s, %s)"""
                        cursor.execute(quary, record)
                        mydb.commit()
                        print("created successfully!!")
                    except mysql.connector.Error as error:
                        print("Failed to insert into MySQL table {}".format(error))

                    if mydb.is_connected():
                        mydb.close()
                        print("closed")

                    break
                else:
                    print("NOTHING HAPPENED")
            else:
                print("nothing")
    print("""
    Hello and welcome
    1. New user
    2. old user""")

    while True:
        user = input("> ")
        if int(user) == 1:
            new_user2()
        elif int(user) == 2:
            old_user()
            break
        else:
            print("Invalid")
            print("""1. New user
    2. old user""")
            continue
        break

    # start shopping

    items = []
    values = []
    quantity2 = []
    temporary_dict = {}
    gg = {1: "apple",
          2: "mango",
          3: "eggs",
          4: "milk"
          }
    available = {"apple": 200,
                 'mango': 100,
                 'eggs': 120,
                 "milk": 50
                 }
    choice = '+'
    print("lets get to shopping\n"
          "here are the list of items\n"
          "1. apple: rs. 200/ kg \n"
          "2. mango: rs. 100/ kg \n"
          "3. eggs: rs. 120/ dozen \n"
          "4. milk: rs. 50/ litre")
    while True:
        if choice == '+':
            item = int(input("what do you want: "))
            quantity = int(input("How much/many: "))
            quantity2.append(quantity)
            ll = gg.get(item)
            temporary_dict[ll] = quantity

            if ll is not None:
                items.append(ll)
                x = available.get(ll)
                values.append(x * quantity)
            else:
                print("We don't have that")
                continue
            j = input("'+' to continue shopping '-' exit shopping ")
            choice = j
        elif choice == '-':
            break
        else:
            print("invalid")
            break
    get = balance
    get = get - sum(values)
    try:
        mydb = mysql.connector.connect(host="buh89x1pi8cgvaw4161i-mysql.services.clever-cloud.com",
                                       user="ucwyejivetooukiz",
                                       password="aAo8DieytbUo0FiYV4RY",
                                       database="buh89x1pi8cgvaw4161i")
        cursor = mydb.cursor()
        quary2 = """UPDATE abc SET balance = %s WHERE phone = %s"""
        value2 = (get, ph_no)
        cursor.execute(quary2, value2)
        mydb.commit()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    if mydb.is_connected():
        mydb.close()
        print("closed")

    if balance > 0:
        print("Your items: ")
        print(('\n'.join('{} {} unit'.format(k, int(v)) for k, v in temporary_dict.items())))
        print("bonus time! chance to win 50% discount!")
        g = random.randint(1, 5)
        l = int(input("guess a random number between 1 and 5: "))
        if g == l:
            print("congratulations you saved ", (sum(values) - (0.5 * sum(values))), "🥳)")
            print("your total: ", (sum(values) - (0.5 * sum(values))))
            print("remaining balance is:", get)
        else:
            print("sorry no discount today ☹")
            print("your total: ", sum(values))
            print("remaining balance is:", get)
    elif balance < 0:
        print(f"Sorry! We cannot provide the items as you are short of {balance * -1}  ")
    print("Thank you for shopping with us! 🙏")

while True:
    complete_program()
