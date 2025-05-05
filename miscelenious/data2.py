import numpy as np

import matplotlib.pyplot as plt

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Generate prime numbers up to 100
numbers = range(2, 101)
primes = [num for num in numbers if is_prime(num)]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(primes, [1] * len(primes), 'ro', markersize=8)
plt.grid(True)
plt.title('Prime Numbers up to 100')
plt.xlabel('Numbers')
plt.yticks([])  # Hide y-axis ticks
plt.show()