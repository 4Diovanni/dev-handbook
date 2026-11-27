// JAVA-PERF-001, bad: String += inside a loop copies everything built so far.
import java.util.ArrayList;
import java.util.List;

public class Bad {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        for (int i = 0; i < 20_000; i++) {
            names.add("name-" + i);
        }

        String csv = "";
        for (String name : names) {
            csv += name + ",";
        }
        System.out.println(csv.length() + " " + csv.substring(csv.length() - 20));
    }
}
