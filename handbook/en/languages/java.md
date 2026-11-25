# Java

Java language rules (Java 21 LTS baseline). Load together with `core/`.

- Rule prefix: `JAVA`
- Formatting is left to google-java-format or the project's formatter and is not a rule here.

## Security

### JAVA-SEC-001: Use `PreparedStatement` parameters, never string concatenation in SQL

**Level:** MUST · **Lens:** security

Concatenated input becomes part of the SQL text and can change the query. Bound parameters are sent separately and always treated as data.

```java
// Bad
Statement st = conn.createStatement();
ResultSet rs = st.executeQuery("SELECT id FROM users WHERE email = '" + email + "'");

// Good
PreparedStatement ps = conn.prepareStatement("SELECT id FROM users WHERE email = ?");
ps.setString(1, email);
ResultSet rs = ps.executeQuery();
```

**Exceptions:** table or column names, which must come from a fixed allowlist.
**Source:** [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### JAVA-SEC-002: Disable external entities in XML parsers

**Level:** MUST · **Lens:** security

JDK XML parsers resolve external entities and DTDs by default, which lets a crafted document read local files or call internal URLs (XXE). Turn them off before parsing untrusted XML.

```java
// Bad
DocumentBuilder db = DocumentBuilderFactory.newInstance().newDocumentBuilder();
Document doc = db.parse(input);

// Good
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
Document doc = dbf.newDocumentBuilder().parse(input);
```

**Exceptions:** documents that need a DTD; then disable external entities individually as the cheat sheet shows.
**Source:** [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

### JAVA-SEC-003: Never deserialize untrusted data with `ObjectInputStream`

**Level:** MUST · **Lens:** security

Native deserialization can instantiate any class on the classpath, and gadget chains turn that into remote code execution. Use a data format such as JSON mapped to known types.

```java
// Bad
try (var in = new ObjectInputStream(request.getInputStream())) {
    Order order = (Order) in.readObject();
}

// Good
Order order = objectMapper.readValue(request.getInputStream(), Order.class);
```

**Exceptions:** trusted, internal streams; even then, set an `ObjectInputFilter` allowlist.
**Source:** [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)

### JAVA-SEC-004: Use `SecureRandom` for tokens, keys and passwords

**Level:** MUST · **Lens:** security

`java.util.Random` and `Math.random()` are predictable linear generators; a few outputs reveal the rest. `SecureRandom` draws from a cryptographic source.

```java
// Bad
String token = Long.toHexString(new Random().nextLong());

// Good
private static final SecureRandom RANDOM = new SecureRandom();

byte[] bytes = new byte[32];
RANDOM.nextBytes(bytes);
String token = Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
```

**Exceptions:** non-security uses such as simulations or shuffling test data.
**Source:** [Java SE 21 API, SecureRandom](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/SecureRandom.html)

### JAVA-SEC-005: Start processes with an argument list, never through a shell

**Level:** MUST · **Lens:** security

Passing a command string to `sh -c` or `cmd /c` lets `;`, `&&` or `|` in input run extra commands. `ProcessBuilder` with separate arguments runs one program with literal arguments.

```java
// Bad
Runtime.getRuntime().exec(new String[] {"sh", "-c", "convert " + fileName + " out.png"});

// Good
Process p = new ProcessBuilder("convert", fileName, "out.png").start();
```

**Exceptions:** fixed commands with no external input.
**Source:** [OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)

### JAVA-SEC-006: Normalize file paths and keep them inside the allowed directory

**Level:** MUST · **Lens:** security

`../` segments or absolute paths in a file name escape the folder you meant to serve. Resolve and normalize, then check the result still starts with the base directory.

```java
// Bad
Path file = uploadDir.resolve(fileName);
return Files.readAllBytes(file);

// Good
Path base = uploadDir.toAbsolutePath().normalize();
Path file = base.resolve(fileName).normalize();
if (!file.startsWith(base)) {
    throw new SecurityException("invalid path: " + fileName);
}
return Files.readAllBytes(file);
```

**Source:** [OWASP, path traversal](https://owasp.org/www-community/attacks/Path_Traversal)

## Performance

### JAVA-PERF-001: Use `StringBuilder` to build strings in loops

**Level:** SHOULD · **Lens:** performance

`+=` on a `String` inside a loop creates a new string and copies all previous content each time, O(n²) overall. One `StringBuilder` (or `String.join` / `Collectors.joining`) appends in place.

```java
// Bad
String csv = "";
for (String name : names) {
    csv += name + ",";
}

// Good
StringBuilder csv = new StringBuilder();
for (String name : names) {
    csv.append(name).append(',');
}
```

**Exceptions:** concatenation outside loops, which the compiler already optimizes.
**Source:** [Java SE 21 API, StringBuilder](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/StringBuilder.html)

### JAVA-PERF-002: Avoid boxed types in hot loops and numeric streams

**Level:** SHOULD · **Lens:** performance

`Long`, `Integer` and `Stream<Integer>` allocate an object for many values and add unboxing on every operation. Primitives and `IntStream` / `LongStream` avoid that.

```java
// Bad
Long total = 0L;
for (long amount : amounts) {
    total += amount;  // unbox, add, box a new Long
}

// Good
long total = 0L;
for (long amount : amounts) {
    total += amount;
}
```

**Exceptions:** values that can be `null` or must go into a collection.
**Source:** [Java tutorials, autoboxing and unboxing](https://docs.oracle.com/javase/tutorial/java/data/autoboxing.html)

### JAVA-PERF-003: Compile regular expressions once

**Level:** SHOULD · **Lens:** performance

`String.matches`, `replaceAll` and `split` with a regex compile the pattern on every call. Keep a `static final Pattern` and reuse it.

```java
// Bad
for (String line : lines) {
    if (line.matches("\\d{4}-\\d{2}-\\d{2}.*")) {
        dated.add(line);
    }
}

// Good
private static final Pattern DATED = Pattern.compile("\\d{4}-\\d{2}-\\d{2}.*");

for (String line : lines) {
    if (DATED.matcher(line).matches()) {
        dated.add(line);
    }
}
```

**Exceptions:** code that runs once, such as startup configuration.
**Source:** [Java SE 21 API, Pattern](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/regex/Pattern.html)

### JAVA-PERF-004: Give collections an initial capacity when the size is known

**Level:** SHOULD · **Lens:** performance

A default `ArrayList` or `HashMap` grows by copying its backing array several times while filling. Sizing it once avoids those copies.

```java
// Bad
List<OrderDto> dtos = new ArrayList<>();
for (Order order : orders) {
    dtos.add(OrderDto.from(order));
}

// Good
List<OrderDto> dtos = new ArrayList<>(orders.size());
for (Order order : orders) {
    dtos.add(OrderDto.from(order));
}
```

**Exceptions:** small or unknown sizes. For maps on Java 19+, use `HashMap.newHashMap(n)`, which accounts for the load factor.
**Source:** [Java SE 21 API, HashMap.newHashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html#newHashMap(int))

### JAVA-PERF-005: Use `EnumMap` and `EnumSet` for enum keys

**Level:** SHOULD · **Lens:** performance

`EnumMap` and `EnumSet` are backed by arrays and bit vectors indexed by ordinal: faster and smaller than hash-based collections, and they iterate in declaration order.

```java
// Bad
Map<Status, Long> counts = new HashMap<>();

// Good
Map<Status, Long> counts = new EnumMap<>(Status.class);
```

**Exceptions:** none for new code. When replacing an existing map, iteration order changes from hash order to declaration order; label it "behavior change" if anything depends on it.
**Source:** [Java SE 21 API, EnumMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/EnumMap.html)

## Maintainability

### JAVA-MAINT-001: Close resources with try-with-resources

**Level:** MUST · **Lens:** maintainability

Streams, connections and readers closed by hand leak when an exception skips the `close()` call. try-with-resources closes them on every path and keeps suppressed exceptions.

```java
// Bad
BufferedReader reader = Files.newBufferedReader(path);
String first = reader.readLine();
reader.close();

// Good
try (BufferedReader reader = Files.newBufferedReader(path)) {
    String first = reader.readLine();
}
```

**Source:** [Java tutorials, try-with-resources](https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html)

### JAVA-MAINT-002: Never swallow exceptions; keep the cause when wrapping

**Level:** MUST · **Lens:** maintainability

An empty `catch` hides failures and leaves the program in an unknown state. Handle the exception, or rethrow it wrapped with the original as the cause.

```java
// Bad
try {
    return mapper.readValue(json, Config.class);
} catch (IOException e) {
    return null;
}

// Good
try {
    return mapper.readValue(json, Config.class);
} catch (IOException e) {
    throw new ConfigException("invalid config", e);
}
```

**Exceptions:** an expected, harmless failure, with a comment explaining why it is ignored.
**Source:** Joshua Bloch, *Effective Java*, 3rd ed., item 77

### JAVA-MAINT-003: Override `equals` and `hashCode` together

**Level:** MUST · **Lens:** maintainability

Equal objects must have equal hash codes. Overriding only `equals` breaks `HashMap` and `HashSet`, which then fail to find objects that are equal.

```java
// Bad
final class Money {
    @Override
    public boolean equals(Object o) {
        return o instanceof Money m && amount.equals(m.amount) && currency.equals(m.currency);
    }
}

// Good
record Money(BigDecimal amount, Currency currency) {}  // equals, hashCode and toString generated
```

**Source:** [Java SE 21 API, Object.hashCode](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#hashCode())

### JAVA-MAINT-004: Return empty collections, not `null`

**Level:** SHOULD · **Lens:** maintainability

A `null` collection forces every caller to check for it, and the one that forgets throws `NullPointerException`. An empty collection works in loops and streams as is.

```java
// Bad
List<Order> findOrders(long customerId) {
    List<Order> orders = repo.byCustomer(customerId);
    return orders.isEmpty() ? null : orders;
}

// Good
List<Order> findOrders(long customerId) {
    return repo.byCustomer(customerId);  // empty list when there are none
}
```

**Exceptions:** for a single value that may be absent, return `Optional<T>`.
**Source:** Joshua Bloch, *Effective Java*, 3rd ed., item 54

### JAVA-MAINT-005: Use records for immutable data carriers

**Level:** SHOULD · **Lens:** maintainability

A class with private final fields, a constructor, getters, `equals`, `hashCode` and `toString` is dozens of lines to read and keep in sync. A record declares the same in one line.

```java
// Bad
public final class Point {
    private final int x;
    private final int y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int getX() { return x; }
    public int getY() { return y; }
    // equals, hashCode, toString ...
}

// Good
public record Point(int x, int y) {}
```

**Exceptions:** types that need mutable state, inheritance, or a JavaBeans API required by a framework. Accessors change from `getX()` to `x()`, so replacing a public class is a behavior change for its callers.
**Source:** [JEP 395, records](https://openjdk.org/jeps/395)
