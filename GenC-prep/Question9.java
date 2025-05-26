import java.util.Scanner;
public class Question9 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter Salary");
        double Salary = sc.nextDouble();
        if (Salary <= 0){
            System.out.println("Invalid Input");
            System.exit(0);
        }
        System.out.print("Enter the performance appraisal rating: ");
        double appraisal = sc.nextDouble();
        if (appraisal< 1 || appraisal > 5){
            System.out.println("Invalid Input");
            System.exit(0);
        }

        double new_salary = 0;

        if(appraisal >= 1 && appraisal <= 3){
            new_salary = Salary + (0.1 * Salary);
        }
        else if(appraisal >= 3.1 && appraisal <= 4){
            new_salary = Salary + (0.25 * Salary);
        }
        else 
            new_salary = Salary + (0.3 * Salary );
        
        
        System.out.println(new_salary);
        
    
    }
    
}
