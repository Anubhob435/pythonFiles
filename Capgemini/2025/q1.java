import java.util.*;

public class q1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        Set<Integer> set = new HashSet<>();
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
            set.add(arr[i]);
        }
        int count = 0;
        for (int num : arr) {
            boolean special = false;
            for (int f = 2; f <= Math.sqrt(num); f++) {
                if (num % f == 0) {
                    if (set.contains(f) || set.contains(num / f)) {
                        special = true;
                        break;
                    }
                }
            }
            if (special) count++;
        }
        System.out.println(count);
    }
}
