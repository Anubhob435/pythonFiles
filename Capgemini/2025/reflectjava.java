import java.lang.reflect.Method;
import java.util.HashMap;

public class reflectjava {
    public static void main(String[] args) {
        Method[] methods = HashMap.class.getDeclaredMethods();
        for (Method m : methods) {
            System.out.println(m);
        }
    }

}