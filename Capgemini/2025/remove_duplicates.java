import java.util.ArrayList;
import java.util.Scanner;

public class remove_duplicates {
    public static void main(String[] args) {
        System.out.println("how many elements");
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        ArrayList<Integer> list = new ArrayList<>();
        for(int i = 0; i < n; i++){
            list.add(sc.nextInt());
        }

        ArrayList<Integer> result = new ArrayList<>();
        for(int key : list){
            if(!result.contains(key)){
                result.add(key);
            }
        }
        for(int z : result){
            System.out.println(z);
        }
/* 
        // Remove duplicates while preserving order
        LinkedHashSet<Integer> set = new LinkedHashSet<>(list);
        ArrayList<Integer> result = new ArrayList<>(set);

        for(int num : result) {
            System.out.println(num);
        }
        */

    }
}