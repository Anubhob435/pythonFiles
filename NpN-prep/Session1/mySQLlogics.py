#Download SQL Dataset from https://github.com/datacharmer/test_db

import mysql.connector

# Replace with your MySQL credentials
config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'raise_on_warnings': True
}

try:
    conn = mysql.connector.connect(**config)
    print("Connected to MySQL server successfully!")

    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    print("Databases:")
    for db in cursor:
        print(f"- {db[0]}")

    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")