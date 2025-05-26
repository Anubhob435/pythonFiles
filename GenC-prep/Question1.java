import java.text.DecimalFormat;
import java.util.Scanner;

public class Question1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        DecimalFormat df2 =new DecimalFormat("0.00");

        System.out.print("Enter Total fuel to fill the tank: ");
        double total_fuel = sc.nextDouble();

        System.out.print("Enter Total distance covered: ");
        double total_distance = sc.nextDouble();

        if(total_fuel <=0 || total_distance<=0 ){
            System.out.println("Invalid Input");
        }
        else{
        double total_distance_miles = total_distance/0.6214;
        double total_fuel_gallons = total_fuel/0.2642;


        double per100_km_fuel = (total_fuel/total_distance)*100;  
        System.out.println(df2.format(per100_km_fuel));

        double miles_per_gallons = total_distance_miles/total_fuel_gallons;

        System.out.println(df2.format(miles_per_gallons));
        }
       
        
        sc.close();
    }
}