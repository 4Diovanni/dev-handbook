// JAVA-PERF-002, good: a primitive long accumulator.
public class Good {
    public static void main(String[] args) {
        long[] amounts = new long[5_000_000];
        for (int i = 0; i < amounts.length; i++) {
            amounts[i] = (i * 37L) % 1000;
        }

        long total = 0L;
        for (long amount : amounts) {
            total += amount;
        }
        System.out.println(total);
    }
}
