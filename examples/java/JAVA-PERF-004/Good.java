// JAVA-PERF-004, good: collections are sized once when the size is known.
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Good {
    public static void main(String[] args) {
        int size = 1_000_000;

        List<String> dtos = new ArrayList<>(size);
        Map<Integer, String> byId = HashMap.newHashMap(size);
        for (int i = 0; i < size; i++) {
            String dto = "order-" + i;
            dtos.add(dto);
            byId.put(i, dto);
        }
        System.out.println(dtos.size() + " " + byId.get(size / 2));
    }
}
