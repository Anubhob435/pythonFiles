import java.util.*;
public class javaArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int array[] = {1,3,5,7,2,2,1};
        Arrays.sort(array);
        for (int i = 0; i<= 6; i++)
            System.out.print(array[i] + ", ");
        
        System.out.println();

        String arr[] = {"boys", "apple", "girls", "zebra", "hello" };
        for (int j = 0; j<= 4; j++)
            System.out.print(arr[j] + ", ");

        System.out.println();

        Arrays.sort(arr);
        for (int j = 0; j<= 4; j++)
            System.out.print(arr[j] + ", ");
    }
}
