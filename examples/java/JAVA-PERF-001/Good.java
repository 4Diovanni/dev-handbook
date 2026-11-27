// JAVA-PERF-001, good: one StringBuilder appends in place.
import java.util.ArrayList;
import java.util.List;

public class Good {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        for (int i = 0; i < 20_000; i++) {
            names.add("name-" + i);
        }

        StringBuilder builder = new StringBuilder();
        for (String name : names) {
            builder.append(name).append(',');
        }
        String csv = builder.toString();
        System.out.println(csv.length() + " " + csv.substring(csv.length() - 20));
    }
}
