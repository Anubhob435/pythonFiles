/* 
Problem Statement
Evaluate the expression a^3 + a^2 b + 2 a^2 b + 2 a b^2 + a b^2 + b^3. Write a program that accepts values for a, b (and c if required by your interface) and outputs the result of the expression.

(Clarify whether c is needed; the expression uses only a and b.)
*/

// bacially (a + b)^3
import java.util.Scanner;
public class Evaluate {
    public static void main(String[] args) {
        
        Scanner sc = new Scanner(System.in);

        int a,b;

        System.out.println("Enter the value of a");
        a = sc.nextInt();
        System.out.println("Enter the value of b");
        b = sc.nextInt();   
        
        System.out.println(Math.pow((a+b), 3));

        sc.close();
    }
    
}
