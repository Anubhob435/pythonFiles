import java.util.Scanner;
public class Question6 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter month number:");
        int month = sc.nextInt(); 

        if (month >12 || month < 1){
            System.out.println("invalid month");
            System.exit(0);
        }
        System.out.print("Season: ");
        if (month >= 3 && month <= 5){
            System.out.println("Spring");
        }
        if (month >= 6 && month <= 8){
            System.out.println("Summer");
        }
        if (month >= 9 && month <= 11){
            System.out.println("Autumn");
        }
        if (month ==12 && month <= 2){
            System.out.println("Winter");
        }

        sc.close();
    }   
}
