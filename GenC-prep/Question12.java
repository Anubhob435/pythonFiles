import java.util.Scanner;

public class Question12 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("How many Items? ");
        int N = sc.nextInt();
        sc.nextLine(); // consume newline
        
        String[] itemNames = new String[N];
        double[] discountAmounts = new double[N];
        
        // Read items and calculate discount amounts
        for (int i = 0; i < N; i++) {
            String input = sc.nextLine();
            String[] parts = input.split(",");
            
            String name = parts[0];
            double price = Double.parseDouble(parts[1]);
            double discountPercentage = Double.parseDouble(parts[2]);
            
            itemNames[i] = name;
            discountAmounts[i] = (price * discountPercentage) / 100;
        }
        
        // Find minimum discount amount
        double minDiscount = discountAmounts[0];
        for (int i = 1; i < N; i++) {
            if (discountAmounts[i] < minDiscount) {
                minDiscount = discountAmounts[i];
            }
        }
        
        // Print all items with minimum discount
        for (int i = 0; i < N; i++) {
            if (discountAmounts[i] == minDiscount) {
                System.out.println(itemNames[i]);
            }
        }
        
        sc.close();
    }
}
