// JAVA-PERF-005, bad: a hash map keyed by an enum.
// The output is sorted so it does not depend on hash iteration order.
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

public class Bad {
    enum Status { NEW, PAID, SHIPPED, CANCELLED }

    public static void main(String[] args) {
        Status[] statuses = Status.values();
        Map<Status, Long> counts = new HashMap<>();
        for (int i = 0; i < 1_000_000; i++) {
            counts.merge(statuses[(i * 7) % statuses.length], 1L, Long::sum);
        }
        System.out.println(new TreeMap<>(counts));
    }
}
