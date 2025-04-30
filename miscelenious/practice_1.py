import seaborn as sns

def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"

# Test the function
print(divide_numbers(10, 2))  # Normal division
print(divide_numbers(10, 0))  # Attempting division by zero

import matplotlib.pyplot as plt

# Load built-in dataset
tips = sns.load_dataset("tips")

# Create a scatterplot
sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.title("Tips vs Total Bill Amount")
plt.show()