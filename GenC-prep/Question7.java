import java.util.Scanner;
public class Question7 {

    public static boolean isprime(int a){
        boolean isprime = true;
        int x;
        if (a<2)
            isprime = false;
        else if (a== 2)
            isprime = true;
        
        else{
            for (int i= 2; i<a; i++){
                x = a % i;
                if (x == 0){
                    isprime = false;
                    break;
                }
            }
            
        }

        return isprime;
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        if(a<0 || a > b){
            System.out.println("Invalid Input");
            System.exit(0);
        }
        sc.close();

        for(int j = a; j <= b; j++){
            boolean k = isprime(j);
            if (k == true)
                System.out.print(j + " ");
        }
    }
}
