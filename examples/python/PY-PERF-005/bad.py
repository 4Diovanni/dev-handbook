"""PY-PERF-005, bad: a pure function recomputes the same expensive result."""

from decimal import Decimal

REGIONS = ["north", "south", "east", "west"]


def parse_rate_table() -> dict[str, Decimal]:
    lines = (f"{region}={10 + i}.{i * 25:02d}" for i, region in enumerate(REGIONS) for _ in range(500))
    table = "\n".join(lines)
    return {key: Decimal(value) for key, value in (line.split("=") for line in table.splitlines())}


def tax_rate(region: str) -> Decimal:
    return parse_rate_table()[region]


orders = [(REGIONS[i % 4], Decimal(i % 97)) for i in range(1000)]
print(sum(amount * tax_rate(region) / 100 for region, amount in orders))
