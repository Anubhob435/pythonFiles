import java.util.HashMap;
public class Java_hash_map{
    public static void main(String[] args) {
        HashMap<Character, Integer> maped = new HashMap<>();

        String input = "aabbbbccccdddddkkkk";

        for(int i = 0; i< input.length(); i++){
            maped.put(input.charAt(i), 0);
        }
        for(int j = 0; j<input.length(); j++){
            char c = input.charAt(j);
            maped.put(c, maped.getOrDefault(c, 0) + 1);
        }
        for(Character key : maped.keySet()){
            System.out.print(key +""+ maped.get(key));
        }
    }
}