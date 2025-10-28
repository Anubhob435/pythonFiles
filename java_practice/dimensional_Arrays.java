package java_practice;
import java.util.Scanner;
public class dimensional_Arrays {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Hello");

        int[][] grid = {
                {10, 20, 30},  // Row 0
                {40, 50, 60},  // Row 1
                {70, 80, 90}   // Row 2
        };
        System.out.println(grid[1][1]);

        for (int i= 0; i< grid.length; i++ ){
            for (int j  = 0; j< grid[i].length; j++){
                System.out.print(grid[i][j] + " ");
            }
            System.out.println();
        }

        System.out.println();
        for (int i= grid.length -1; i>=0; i-- ){
            for (int j = grid.length - 1; j>= 0; j--){
                System.out.print(grid[i][j] + " ");
            }
            System.out.println();
        }

        int[][] arr = new int[2][2];

        for(int a = 0; a < arr.length; a++){
            for(int b = 0; b< arr[a].length; b++){
                System.out.println("enter Number: ");
                arr[b][a] = sc.nextInt();
            }
        }
        System.out.println();

        for (int i= 0; i< arr.length; i++ ){
            for (int j  = 0; j< arr[i].length; j++){
                System.out.print(arr[i][j] + " ");
            }
            System.out.println();
        }
        System.out.println();

    }
}
