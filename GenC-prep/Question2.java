import java.util.Scanner;
public class Question2 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter no. of pizzas bought: ");
        int pizza = sc.nextInt();

        System.out.println("Enter no. of puffs bought: ");
        int puffs = sc.nextInt();

        System.out.println("Enter no. of cool drinks bought: ");
        int cooldrinks = sc.nextInt();

        int price_pizza = 100;
        int price_puffs = 20;
        int prize_cooldrinks = 10;

        int total_bill = (pizza * price_pizza) + (puffs * price_puffs) + (cooldrinks * prize_cooldrinks);
        System.out.println("no. of pizaas: " + pizza);
        System.out.println("no. of Puffs: " + puffs);
        System.out.println("no. of cooldrinks: " + cooldrinks);
        System.out.println("Total price: " + total_bill);
        System.out.println("Enjoy the show!! ");

        sc.close();
    }
}
