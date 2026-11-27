// JAVA-PERF-003, good: the regex is compiled once into a static final Pattern.
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class Good {
    private static final Pattern DATED = Pattern.compile("\\d{4}-\\d{2}-\\d{2}.*");

    public static void main(String[] args) {
        List<String> lines = new ArrayList<>();
        for (int i = 0; i < 200_000; i++) {
            lines.add(i % 3 == 0 ? "2026-11-%02d event %d".formatted(i % 28 + 1, i) : "event " + i);
        }

        List<String> dated = new ArrayList<>();
        for (String line : lines) {
            if (DATED.matcher(line).matches()) {
                dated.add(line);
            }
        }
        System.out.println(dated.size() + " " + dated.get(dated.size() - 1));
    }
}
