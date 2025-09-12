import java.util.HashMap;
public class Count_occurances{
    public static void main(String[] args) {
        HashMap<Integer, Integer> maped = new HashMap<>();

        int n = 10;
        int[] array = {1, 2, 3, 3, 4, 1, 4, 5, 1, 2};

        for(int i = 0; i< n; i++){
            maped.put(array[i], 0);
        }
        for(int j = 0; j<n; j++){
            int c = array[j];
            maped.put(c, maped.getOrDefault(c, 0) + 1);
        }
        for(Integer key : maped.keySet()){
            System.out.println(key +" occurs "+ maped.get(key) + " times");
        }
    }
}