import java.util.Scanner;

public class Question10 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter a 4-digit number:");
        int number = scanner.nextInt();
        scanner.close();
        
        if (isValidCarNumber(number)) {
            System.out.println(number + " is a valid car number");
        } else {
            System.out.println(number + " is not a valid car number");
        }
    }
    
    public static boolean isValidCarNumber(int number) {
        // Check if it's a positive 4-digit number
        if (number < 1000 || number > 9999) {
            return false;
        }
        
        // Calculate sum of digits
        int sum = 0;
        int temp = number;
        
        while (temp > 0) {
            sum += temp % 10;
            temp /= 10;
        }
        
        // Check if sum is divisible by 3 or 5 or 7
        return sum % 3 == 0 || sum % 5 == 0 || sum % 7 == 0;
    }
}
