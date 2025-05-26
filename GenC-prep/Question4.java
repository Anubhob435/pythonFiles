
import java.util.Scanner;

public class Question4 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        System.out.println("Enter the no of students placed in CSE");
        int cse = sc.nextInt();
        if (cse < 0)
            System.out.println("invalid Input");

        System.out.println("Enter the no of students placed in ECE");
        int ece = sc.nextInt();
        if (ece < 0)
            System.out.println("invalid Input");        

        System.out.println("Enter the no of students placed in MECH");
        int mech = sc. nextInt();
        if (mech < 0)
            System.out.println("invalid Input");

        if(cse == ece & ece == mech)
            System.out.println("None got highest placements");

        else{
            System.out.println("HIGHEST PLACEMENT: ");
            if (cse>= ece && cse>= mech)
                System.out.println("CSE");
            if (ece>= cse && ece >= mech)
                System.err.println("ECE");
            if (mech >= cse && mech> ece)
                System.out.println("MECH");
        } 
        
        
    }
    
}
