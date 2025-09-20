/* 
Problem Statement
Evaluate the expression a^3 + a^2 b + 2 a^2 b + 2 a b^2 + a b^2 + b^3. 
Write a program that accepts values for a and b and outputs the result of the expression.
*/

// Simplified expression: (a + b)^3
import java.util.Scanner;

public class Evaluate {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the value of a:");
        int a = sc.nextInt();
        
        System.out.println("Enter the value of b:");
        int b = sc.nextInt();

        // Calculate the expression: a^3 + a^2 b + 2 a^2 b + 2 a b^2 + a b^2 + b^3
        // Which simplifies to: (a + b)^3
        double result = Math.pow(a + b, 3);
        System.out.println("Result: " + result);

        sc.close();
    }
}
