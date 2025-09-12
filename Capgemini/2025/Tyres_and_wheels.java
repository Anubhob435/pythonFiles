import java.util.Scanner;

public class Tyres_and_wheels {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("How many Dealers? ");
        int x = sc.nextInt();
        sc.nextLine();
        String[] array = new String[x];

        for (int i = 0; i < x; i++) {
            array[i] = sc.nextLine();
        }

        for (int i = 0; i < x; i++) {
            String input = array[i];
            String[] parts = input.split(" ");

            int car = Integer.parseInt(parts[0]);
            int bike = Integer.parseInt(parts[1]);
            
            int totalTyres = car * 4 + bike * 2;
            System.out.println(totalTyres);
        }
    }
}