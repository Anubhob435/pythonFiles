import java.util.Scanner;
public class Question8 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int x = n;
        int rev = 0;
        while(n !=0){
            int z = n %10;
            rev = rev *10 + z;
            n = n/10;
        }

        if(x == rev)
            System.out.println("palindrome");
        else    
            System.out.println("Not a palindrome");
        
        sc.close();
    }
}
