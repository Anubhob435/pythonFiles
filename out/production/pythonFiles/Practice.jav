import java.util.Scanner;
public class Practice {

    public static boolean isprime(int n){

        boolean isprime= true;

        if(n <= 1){
            return false;
        }
        else if(n == 2){
             return true;
        }
        else{
            for (int i = 2; i < n; i++) {

                if (n % i == 0) {
                    isprime = false;
                    break;
                }

            }
        }
        return isprime;
    }


    public static void main(String [] args){


    }


    }


