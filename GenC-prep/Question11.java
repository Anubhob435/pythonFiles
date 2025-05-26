import java.util.Scanner;
public class Question11 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the number of courses available ");
        int num = sc.nextInt();

        if (num < 1 || num >20){
            System.out.println("Invalid number of courses: ");
            System.exit(0);
        }
        
        String[] Courses = new String[num];

        System.out.println("Enter Course Names: ");
        sc.nextLine();
        for (int i = 0; i < num; i++){
            Courses[i] = sc.nextLine();
        }

        System.out.println("Enter the course to be searched: ");
        String st = sc.nextLine().toLowerCase();

        boolean course_avalable = false;
        for( int j = 0; j <num; j++){
            if(Courses[j].toLowerCase().equals(st)){
                course_avalable = true;
                break;
            }
            //System.out.println(st + " Course Available ");            
        }
        if (course_avalable)
            System.out.println(st + " Course Available ");
        else 
            System.out.println(st +" Course not available ");
    }
}
