// JAVA-PERF-003, bad: String.matches compiles the regex on every call.
import java.util.ArrayList;
import java.util.List;

public class Bad {
    public static void main(String[] args) {
        List<String> lines = new ArrayList<>();
        for (int i = 0; i < 200_000; i++) {
            lines.add(i % 3 == 0 ? "2026-11-%02d event %d".formatted(i % 28 + 1, i) : "event " + i);
        }

        List<String> dated = new ArrayList<>();
        for (String line : lines) {
            if (line.matches("\\d{4}-\\d{2}-\\d{2}.*")) {
                dated.add(line);
            }
        }
        System.out.println(dated.size() + " " + dated.get(dated.size() - 1));
    }
}
