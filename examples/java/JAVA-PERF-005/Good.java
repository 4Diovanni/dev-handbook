// JAVA-PERF-005, good: an EnumMap, backed by an array indexed by ordinal.
// The output is sorted the same way as in Bad.java.
import java.util.EnumMap;
import java.util.Map;
import java.util.TreeMap;

public class Good {
    enum Status { NEW, PAID, SHIPPED, CANCELLED }

    public static void main(String[] args) {
        Status[] statuses = Status.values();
        Map<Status, Long> counts = new EnumMap<>(Status.class);
        for (int i = 0; i < 1_000_000; i++) {
            counts.merge(statuses[(i * 7) % statuses.length], 1L, Long::sum);
        }
        System.out.println(new TreeMap<>(counts));
    }
}
