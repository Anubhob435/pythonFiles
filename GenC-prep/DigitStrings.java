public class DigitStrings {
    public static int CountSurroundingNumbers(String str){

        int surrond_count = 0;
        int temp = 0;
        int len = str.length();

        for (int i = 0; i < len; i++){
            if (Character.isDigit(str.charAt(i)))
                System.err.println("hi");
        }

        return 0;
    }
}
