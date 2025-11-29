### **1) Sum of first n numbers**

📌 *Adds all numbers from n down to 0 using recursion.*

```java
static int sum(int n) {
    if(n == 0) return 0;
    return n + sum(n - 1);
}
```

---

### **2) Sum of squares of digits**

📌 *Adds the square of each digit of a number recursively.*

```java
static int sumSquareDigits(int n) {
    if(n == 0) return 0;
    int d = n % 10;
    return d*d + sumSquareDigits(n / 10);
}
```

---

### **3) Happy number helper**

📌 *Calculates one recursive step of squaring digits (used to check happy number).*

```java
static int happyStep(int n) {
    if(n == 0) return 0;
    int d = n % 10;
    return d*d + happyStep(n / 10);
}
```

---

### **4) GCD using recursion**

📌 *Finds the greatest common divisor using Euclid’s rule.*

```java
static int gcd(int a, int b) {
    if(b == 0) return a;
    return gcd(b, a % b);
}
```

---

### **5) Decimal to Binary**

📌 *Prints binary digits by dividing the number until zero and unwinding.*

```java
static void decToBin(int n) {
    if(n == 0) return;
    decToBin(n / 2);
    System.out.print(n % 2);
}
```

---

### **6) Recursive Binary Search**

📌 *Searches a sorted array by checking the middle element recursively.*

```java
static int search(int[] a, int low, int high, int key) {
    if(low > high) return -1;
    int mid = (low + high) / 2;
    if(a[mid] == key) return mid;
    if(key < a[mid]) return search(a, low, mid-1, key);
    return search(a, mid+1, high, key);
}
```

---

### **7) Fibonacci**

📌 *Returns the nth Fibonacci number by adding the previous two values.*

```java
static int fib(int n) {
    if(n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```

---

### **8) Power sum (x¹ + x² + … + xⁿ)**

📌 *Adds powers of x from n down to 1 using recursion.*

```java
static int powerSum(int x, int n) {
    if(n == 0) return 0;
    return (int)Math.pow(x, n) + powerSum(x, n - 1);
}
```

---

### **9) Reverse string**

📌 *Reverses a string by moving the first character to the end recursively.*

```java
static String reverse(String s) {
    if(s.length() <= 1) return s;
    return reverse(s.substring(1)) + s.charAt(0);
}
```

---

### **10) Palindrome check**

📌 *Checks if first and last characters match and recurses inward.*

```java
static boolean isPalindrome(String s) {
    if(s.length() <= 1) return true;
    if(s.charAt(0) != s.charAt(s.length()-1)) return false;
    return isPalindrome(s.substring(1, s.length()-1));
}
```

---

### **11) Count vowels**

📌 *Counts vowels by checking one character at a time recursively.*

```java
static int countVowels(String s) {
    if(s.length() == 0) return 0;
    char c = Character.toUpperCase(s.charAt(0));
    int add = (c=='A'||c=='E'||c=='I'||c=='O'||c=='U') ? 1 : 0;
    return add + countVowels(s.substring(1));
}
```

---

### **12) Disarium digit power sum**

📌 *Adds digits raised to their respective positions using recursion.*

```java
static int powerSum(int n, int p) {
    if(n == 0) return 0;
    return (int)Math.pow(n % 10, p) + powerSum(n / 10, p - 1);
}
```

---

### **13) Recursive prime check**

📌 *Checks if a number is prime by testing divisors downward recursively.*

```java
static int isPrime(int n, int d) {
    if(d == 1) return 1;
    if(n % d == 0) return 0;
    return isPrime(n, d - 1);
}
```

---

### **14) Unique digits check**

📌 *Returns false if any digit repeats in the number recursively.*

```java
static boolean unique(int n) {
    if(n < 10) return true;
    int d = n % 10;
    if(checkDigit(n / 10, d)) return false;
    return unique(n / 10);
}

static boolean checkDigit(int n, int d) {
    if(n == 0) return false;
    if(n % 10 == d) return true;
    return checkDigit(n / 10, d);
}
```

---

### **15) Prime factorization**

📌 *Prints all prime factors by dividing repeatedly using recursion.*

```java
static void factor(int x, int y) {
    if(x <= 1) return;
    if(x % y == 0) {
        System.out.print(y + " ");
        factor(x / y, y);
    } else {
        factor(x, y + 1);
    }
}
```

---

### **16) Modulus using subtraction**

📌 *Finds x % y by subtracting y repeatedly until x < y.*

```java
static int mod(int x, int y) {
    if(x < y) return x;
    return mod(x - y, y);
}
```

---

### **Example main**

```java
public static void main(String[] args) {
    System.out.println(sum(5));         // 15
    System.out.println(fib(6));         // 8
    decToBin(10);                       // prints 1010
}
```


