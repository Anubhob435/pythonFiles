
import java.util.ArrayList;

public class Test {
    public static void main(String[] args) {
        ArrayList<Integer> arr = new ArrayList<>();
        arr.add(10);
        arr.add(20);
        arr.add(30);
        arr.add(40);
        arr.add(50);
        arr.add(60);

        for(int i = 0; i<2; i++){
            int k = arr.get(5);
            arr.remove(5);
            arr.add(0, k);
            
        }

        for(int i = 0; i< arr.size(); i++){
            System.out.println(arr.get(i));
        }
    }   
}
