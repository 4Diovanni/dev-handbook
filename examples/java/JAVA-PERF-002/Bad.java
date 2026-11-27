// JAVA-PERF-002, bad: a boxed Long accumulator allocates on every addition.
public class Bad {
    public static void main(String[] args) {
        long[] amounts = new long[5_000_000];
        for (int i = 0; i < amounts.length; i++) {
            amounts[i] = (i * 37L) % 1000;
        }

        Long total = 0L;
        for (long amount : amounts) {
            total += amount;
        }
        System.out.println(total);
    }
}
