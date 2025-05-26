import java.util.*;
public class Question5 {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        int cost_of_k = 75;
        int cost_of_q = 150;
        int cost_of_refreshments = 50;
        int discount_percentage = 0;

        double total_bill = 0;

        System.out.println("enter the number of tickets: ");
        int tickets = sc.nextInt();
        if (tickets <5 && tickets > 40){
            System.out.println("invalid tickets");
            System.exit(0);
        }
        if(tickets >= 20){
            discount_percentage = 10;
        }
        sc.nextLine();
        System.out.println("Do You want refreshments? ");
        char op1 = sc.nextLine().charAt(0);
        if (op1 == 'y')
            total_bill += tickets * cost_of_refreshments;   

        System.out.println("Do You have Coupon?: ");
        char op2 = sc.nextLine().charAt(0);
        if (op2 == 'y')
            discount_percentage += 2;
        

        System.out.println("Enter circle: ");
        char circle = sc.nextLine().charAt(0);

        if (circle == 'q')
            total_bill += tickets * cost_of_q;
        else
            total_bill += tickets * cost_of_k;
        

        double finaal_bill = total_bill - (discount_percentage * total_bill /100);
        System.out.println("Ticket cost: " + finaal_bill);


        
    }
}
