import time

def fibonacci(n):
    fib_series = [0, 1]
    while len(fib_series) < n:
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series[:n]

# Example usage
n = int(input("Enter the number of terms: "))
print(f"Fibonacci series up to {n} terms: {fibonacci(n)}")
print("\nNow, let's have some fun with the Fibonacci sequence!")
time.sleep(1)
print("Watch how each term builds on the last...\n")
time.sleep(1)

for index, num in enumerate(fibonacci(n), start=1):
    print(f"Term {index}: {num}")
    time.sleep(0.5)

print("\nFun fact: The Fibonacci sequence pops up in nature such as in the arrangement of leaves, pinecones, and even in the spirals of galaxies!")