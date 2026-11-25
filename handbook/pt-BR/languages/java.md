# Java

Regras da linguagem Java (base: Java 21 LTS). Carregue junto com `core/`.

- Prefixo das regras: `JAVA`
- Formatação fica com o google-java-format ou com o formatador do projeto e não é regra aqui.

## Segurança

### JAVA-SEC-001: Use parâmetros de `PreparedStatement`, nunca concatenação no SQL

**Nível:** MUST · **Lente:** segurança

A entrada concatenada vira parte do texto SQL e pode mudar a query. Parâmetros vinculados são enviados separados e sempre tratados como dado.

```java
// Ruim
Statement st = conn.createStatement();
ResultSet rs = st.executeQuery("SELECT id FROM users WHERE email = '" + email + "'");

// Bom
PreparedStatement ps = conn.prepareStatement("SELECT id FROM users WHERE email = ?");
ps.setString(1, email);
ResultSet rs = ps.executeQuery();
```

**Exceções:** nomes de tabela ou coluna, que precisam vir de uma lista fixa de permitidos.
**Fonte:** [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### JAVA-SEC-002: Desative entidades externas nos parsers de XML

**Nível:** MUST · **Lente:** segurança

Os parsers XML do JDK resolvem entidades externas e DTDs por padrão, o que permite a um documento malicioso ler arquivos locais ou chamar URLs internas (XXE). Desligue isso antes de ler XML não confiável.

```java
// Ruim
DocumentBuilder db = DocumentBuilderFactory.newInstance().newDocumentBuilder();
Document doc = db.parse(input);

// Bom
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
Document doc = dbf.newDocumentBuilder().parse(input);
```

**Exceções:** documentos que precisam de DTD; nesse caso, desative as entidades externas uma a uma, como mostra o cheat sheet.
**Fonte:** [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

### JAVA-SEC-003: Nunca desserialize dados não confiáveis com `ObjectInputStream`

**Nível:** MUST · **Lente:** segurança

A desserialização nativa pode instanciar qualquer classe do classpath, e cadeias de gadgets transformam isso em execução remota de código. Use um formato de dados como JSON mapeado para tipos conhecidos.

```java
// Ruim
try (var in = new ObjectInputStream(request.getInputStream())) {
    Order order = (Order) in.readObject();
}

// Bom
Order order = objectMapper.readValue(request.getInputStream(), Order.class);
```

**Exceções:** fluxos internos e confiáveis; mesmo assim, configure uma allowlist com `ObjectInputFilter`.
**Fonte:** [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)

### JAVA-SEC-004: Use `SecureRandom` para tokens, chaves e senhas

**Nível:** MUST · **Lente:** segurança

`java.util.Random` e `Math.random()` são geradores lineares previsíveis; poucas saídas revelam as próximas. `SecureRandom` usa uma fonte criptográfica.

```java
// Ruim
String token = Long.toHexString(new Random().nextLong());

// Bom
private static final SecureRandom RANDOM = new SecureRandom();

byte[] bytes = new byte[32];
RANDOM.nextBytes(bytes);
String token = Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
```

**Exceções:** usos sem relação com segurança, como simulações ou embaralhar dados de teste.
**Fonte:** [API do Java SE 21, SecureRandom](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/SecureRandom.html)

### JAVA-SEC-005: Inicie processos com lista de argumentos, nunca através de um shell

**Nível:** MUST · **Lente:** segurança

Passar uma string de comando para `sh -c` ou `cmd /c` deixa `;`, `&&` ou `|` na entrada executarem comandos extras. `ProcessBuilder` com argumentos separados roda um único programa com argumentos literais.

```java
// Ruim
Runtime.getRuntime().exec(new String[] {"sh", "-c", "convert " + fileName + " out.png"});

// Bom
Process p = new ProcessBuilder("convert", fileName, "out.png").start();
```

**Exceções:** comandos fixos, sem nenhuma entrada externa.
**Fonte:** [OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)

### JAVA-SEC-006: Normalize caminhos de arquivo e mantenha-os dentro do diretório permitido

**Nível:** MUST · **Lente:** segurança

Segmentos `../` ou caminhos absolutos no nome do arquivo escapam da pasta que você queria servir. Resolva e normalize, depois confira se o resultado ainda começa no diretório base.

```java
// Ruim
Path file = uploadDir.resolve(fileName);
return Files.readAllBytes(file);

// Bom
Path base = uploadDir.toAbsolutePath().normalize();
Path file = base.resolve(fileName).normalize();
if (!file.startsWith(base)) {
    throw new SecurityException("invalid path: " + fileName);
}
return Files.readAllBytes(file);
```

**Fonte:** [OWASP, path traversal](https://owasp.org/www-community/attacks/Path_Traversal)

## Desempenho

### JAVA-PERF-001: Use `StringBuilder` para montar strings em laços

**Nível:** SHOULD · **Lente:** desempenho

`+=` numa `String` dentro de um laço cria uma string nova e copia todo o conteúdo anterior a cada volta, O(n²) no total. Um único `StringBuilder` (ou `String.join` / `Collectors.joining`) acrescenta no lugar.

```java
// Ruim
String csv = "";
for (String name : names) {
    csv += name + ",";
}

// Bom
StringBuilder csv = new StringBuilder();
for (String name : names) {
    csv.append(name).append(',');
}
```

**Exceções:** concatenação fora de laços, que o compilador já otimiza.
**Fonte:** [API do Java SE 21, StringBuilder](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/StringBuilder.html)

### JAVA-PERF-002: Evite tipos boxed em laços quentes e streams numéricos

**Nível:** SHOULD · **Lente:** desempenho

`Long`, `Integer` e `Stream<Integer>` alocam um objeto para muitos valores e fazem unboxing a cada operação. Primitivos e `IntStream` / `LongStream` evitam isso.

```java
// Ruim
Long total = 0L;
for (long amount : amounts) {
    total += amount;  // unbox, add, box a new Long
}

// Bom
long total = 0L;
for (long amount : amounts) {
    total += amount;
}
```

**Exceções:** valores que podem ser `null` ou que precisam ir para uma coleção.
**Fonte:** [Tutoriais Java, autoboxing e unboxing](https://docs.oracle.com/javase/tutorial/java/data/autoboxing.html)

### JAVA-PERF-003: Compile expressões regulares uma vez só

**Nível:** SHOULD · **Lente:** desempenho

`String.matches`, `replaceAll` e `split` com regex compilam o padrão a cada chamada. Guarde um `static final Pattern` e reutilize.

```java
// Ruim
for (String line : lines) {
    if (line.matches("\\d{4}-\\d{2}-\\d{2}.*")) {
        dated.add(line);
    }
}

// Bom
private static final Pattern DATED = Pattern.compile("\\d{4}-\\d{2}-\\d{2}.*");

for (String line : lines) {
    if (DATED.matcher(line).matches()) {
        dated.add(line);
    }
}
```

**Exceções:** código que roda uma vez só, como a configuração na inicialização.
**Fonte:** [API do Java SE 21, Pattern](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/regex/Pattern.html)

### JAVA-PERF-004: Defina a capacidade inicial das coleções quando o tamanho é conhecido

**Nível:** SHOULD · **Lente:** desempenho

Um `ArrayList` ou `HashMap` padrão cresce copiando o array interno várias vezes enquanto é preenchido. Dimensionar uma vez evita essas cópias.

```java
// Ruim
List<OrderDto> dtos = new ArrayList<>();
for (Order order : orders) {
    dtos.add(OrderDto.from(order));
}

// Bom
List<OrderDto> dtos = new ArrayList<>(orders.size());
for (Order order : orders) {
    dtos.add(OrderDto.from(order));
}
```

**Exceções:** tamanhos pequenos ou desconhecidos. Para mapas no Java 19+, use `HashMap.newHashMap(n)`, que já considera o fator de carga.
**Fonte:** [API do Java SE 21, HashMap.newHashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html#newHashMap(int))

### JAVA-PERF-005: Use `EnumMap` e `EnumSet` para chaves enum

**Nível:** SHOULD · **Lente:** desempenho

`EnumMap` e `EnumSet` usam arrays e vetores de bits indexados pelo ordinal: são mais rápidos e menores que coleções baseadas em hash, e iteram na ordem de declaração.

```java
// Ruim
Map<Status, Long> counts = new HashMap<>();

// Bom
Map<Status, Long> counts = new EnumMap<>(Status.class);
```

**Exceções:** nenhuma para código novo. Ao trocar um mapa existente, a ordem de iteração passa da ordem do hash para a ordem de declaração; marque como "behavior change" se algo depender disso.
**Fonte:** [API do Java SE 21, EnumMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/EnumMap.html)

## Manutenibilidade

### JAVA-MAINT-001: Feche recursos com try-with-resources

**Nível:** MUST · **Lente:** manutenibilidade

Streams, conexões e readers fechados à mão vazam quando uma exceção pula a chamada de `close()`. O try-with-resources fecha em todos os caminhos e preserva as exceções suprimidas.

```java
// Ruim
BufferedReader reader = Files.newBufferedReader(path);
String first = reader.readLine();
reader.close();

// Bom
try (BufferedReader reader = Files.newBufferedReader(path)) {
    String first = reader.readLine();
}
```

**Fonte:** [Tutoriais Java, try-with-resources](https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html)

### JAVA-MAINT-002: Nunca engula exceções; preserve a causa ao embrulhar

**Nível:** MUST · **Lente:** manutenibilidade

Um `catch` vazio esconde falhas e deixa o programa num estado desconhecido. Trate a exceção, ou relance embrulhada com a original como causa.

```java
// Ruim
try {
    return mapper.readValue(json, Config.class);
} catch (IOException e) {
    return null;
}

// Bom
try {
    return mapper.readValue(json, Config.class);
} catch (IOException e) {
    throw new ConfigException("invalid config", e);
}
```

**Exceções:** uma falha esperada e inofensiva, com um comentário explicando por que é ignorada.
**Fonte:** Joshua Bloch, *Effective Java*, 3ª ed., item 77

### JAVA-MAINT-003: Sobrescreva `equals` e `hashCode` juntos

**Nível:** MUST · **Lente:** manutenibilidade

Objetos iguais precisam ter o mesmo hash code. Sobrescrever só `equals` quebra `HashMap` e `HashSet`, que deixam de encontrar objetos iguais.

```java
// Ruim
final class Money {
    @Override
    public boolean equals(Object o) {
        return o instanceof Money m && amount.equals(m.amount) && currency.equals(m.currency);
    }
}

// Bom
record Money(BigDecimal amount, Currency currency) {}  // equals, hashCode and toString generated
```

**Fonte:** [API do Java SE 21, Object.hashCode](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#hashCode())

### JAVA-MAINT-004: Devolva coleções vazias, não `null`

**Nível:** SHOULD · **Lente:** manutenibilidade

Uma coleção `null` obriga cada chamador a checar, e quem esquece toma `NullPointerException`. Uma coleção vazia funciona direto em laços e streams.

```java
// Ruim
List<Order> findOrders(long customerId) {
    List<Order> orders = repo.byCustomer(customerId);
    return orders.isEmpty() ? null : orders;
}

// Bom
List<Order> findOrders(long customerId) {
    return repo.byCustomer(customerId);  // empty list when there are none
}
```

**Exceções:** para um valor único que pode não existir, devolva `Optional<T>`.
**Fonte:** Joshua Bloch, *Effective Java*, 3ª ed., item 54

### JAVA-MAINT-005: Use records para portadores de dados imutáveis

**Nível:** SHOULD · **Lente:** manutenibilidade

Uma classe com campos private final, construtor, getters, `equals`, `hashCode` e `toString` tem dezenas de linhas para ler e manter em sincronia. Um record declara o mesmo numa linha.

```java
// Ruim
public final class Point {
    private final int x;
    private final int y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int getX() { return x; }
    public int getY() { return y; }
    // equals, hashCode, toString ...
}

// Bom
public record Point(int x, int y) {}
```

**Exceções:** tipos que precisam de estado mutável, herança ou de uma API JavaBeans exigida por um framework. Os acessores mudam de `getX()` para `x()`, então trocar uma classe pública é uma mudança de comportamento para quem a usa.
**Fonte:** [JEP 395, records](https://openjdk.org/jeps/395)
