import java.util.Scanner;
public class Question3 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the numbers: ");

        for(int i = 1; i<= 4; i++){
            int x = sc.nextInt();
            char y = (char) x;
            System.err.println(x + "- " + y);

        }

        sc.close();
    }
}
