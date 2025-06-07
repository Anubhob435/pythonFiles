public class StrongerKnights {

    public static int CountSpecialKnights(int N, int[] arr){

        int special_knights_count = 0;

        for(int i = 0; i< N; i++){
            int left = 0;
            int right = 0;

            for (int j =0; j< i; j++ ){
                if (arr[j]> arr[i])
                    left+=1;
            }
            for (int k = i+1; k<N; k ++){
                if (arr[k] > arr[i])
                    right += 1;
            }
            if (left > right)
                special_knights_count += 1;

        }

        if (special_knights_count > 0)
            return special_knights_count-1;

        return 0;

    }
    public static void main(String[] args) {
        int[] array = {5,4,3,2,1};

        int x = CountSpecialKnights(5, array);
        System.out.print(x);
    }   
}
