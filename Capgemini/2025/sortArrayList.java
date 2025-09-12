
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class sortArrayList {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        ArrayList<Integer> arr1 = new ArrayList<>();
        ArrayList<Integer> arr2 = new ArrayList<>();
        
        System.out.println();

        int x= sc.nextInt();
        int y = sc.nextInt();

        for(int i = 0; i < x; i++){
            int  temp = sc.nextInt();
            arr1.add(temp);            
        }
        for(int i = 0; i < y; i++){
            int  temp = sc.nextInt();
            arr2.add(temp);            
        }
        for(int key : arr2){
            if(!arr1.contains(key)){
                arr1.add(key);
            }
        }
        Collections.sort(arr1);

        for(int keys : arr1)
        System.out.println(keys);
    }
    
}
