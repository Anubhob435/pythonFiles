import pandas as pd

# Create a sample DataFrame
data = {
    'Name': ['John', 'Emma', 'Alex', 'Sarah'],
    'Age': [25, 28, 22, 30],
    'City': ['New York', 'London', 'Paris', 'Tokyo']
}

# Create DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print("Original DataFrame:")
print(df)

# Basic operations
print("\nFirst 2 rows:")
print(df.head(2))

# Get basic statistics
print("\nBasic statistics of Age:")
print(df['Age'].describe())

# Filter data
print("\nPeople older than 25:")
print(df[df['Age'] > 25])