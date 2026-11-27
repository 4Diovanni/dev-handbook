// JAVA-PERF-004, bad: collections grow by copying while they fill up.
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Bad {
    public static void main(String[] args) {
        int size = 1_000_000;

        List<String> dtos = new ArrayList<>();
        Map<Integer, String> byId = new HashMap<>();
        for (int i = 0; i < size; i++) {
            String dto = "order-" + i;
            dtos.add(dto);
            byId.put(i, dto);
        }
        System.out.println(dtos.size() + " " + byId.get(size / 2));
    }
}
