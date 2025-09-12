public class move_hash {
    public static String moveHashesToFront(String input) {
        if (input == null) return null;
        String hashes = "";
        String others = "";
        for (char c : input.toCharArray()) {
            if (c == '#') hashes += c;
            else others += c;
        }
        return hashes + others;
    }

    public static void main(String[] args) {
        String s = "a#b# #c # d";
        System.out.println(moveHashesToFront(s)); // prints "####abcd"
    }
}
