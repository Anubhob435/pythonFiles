public class question3 {
    public static int compoundfunc(int x){
        int sum = 1;
        int a = x - 1;
        int b = x - 2;
        int c = a * b;

        int p = 0;
        int q = 1;
        
        for (int i = 1; i < c; i++){
            int r = p + q;
            System.out.print(r + " ");
            sum += r;
            
            p = q;
            q = r;
        }
        
        return sum;
    }
    public static void main(String[] args) {
        System.out.print(compoundfunc(4));
    }  
}
