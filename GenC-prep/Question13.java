import java.util.Scanner;
public class Question13 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter number of Semester: ");
        int x  = sc.nextInt();
        int[] max_marks_arr = new int[x];
        int[] number_of_subjects = new int[x];

        for(int i = 0; i< x; i++){
            System.out.println("How many subjects in " + (i+1) + " semester?");
            number_of_subjects[i] = sc.nextInt();
        }

       // for (int a = 0; a<)

/* 
            for(int j =0; j < z; j++){
                System.out.println("marks in Subject " + (j+1) + ": ");
                int y = sc.nextInt();
                if (y < 0 || y > 100)
                    System.exit(0);

                if(y> max_this_sem)
                    max_this_sem = y;
            }
            max_marks_arr[i] = max_this_sem;
            max_this_sem = 0;

        }

        for (int k =0; k < x; k++){
            System.out.println("Highest Marks in " + (k+1) + " smester is " + (max_marks_arr[k]));
        }
*/

    }
    
}
