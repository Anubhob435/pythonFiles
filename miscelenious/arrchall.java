import java.util.*;

public class arrchall {
    public static int arrayChallenge(int num) {
        List<Integer> list = new ArrayList<>();
        String numStr = String.valueOf(num);
        
        // Populate the initial list with the digits of num
        for (char c : numStr.toCharArray()) {
            list.add(c - '0');
        }
        //int xyz = 0;
        int count = 0;
        
        while (true) {
            // Pick a digit from num to multiply
            int multiplier = list.get(count % list.size());
            num *= multiplier; // Multiply num by one of its digits
            count++;
            
            // Append digits of the new number to the list
            numStr = String.valueOf(num);
            for (char c : numStr.toCharArray()) {
                list.add(c - '0');
            }
            
            // Check for adjacent duplicates
            for (int i = 1; i < list.size(); i++) {
                if (list.get(i).equals(list.get(i - 1))) {
                    return count;
                }
            }
        }
    }

    public static void main(String[] args) {
        // Test cases
        System.out.println(arrayChallenge(8));    // Output: 3
        System.out.println(arrayChallenge(198));  // Output: 2
        System.out.println(arrayChallenge(134));  // Output: 1
        System.out.println(arrayChallenge(46));   // Output: 2
    }
}
