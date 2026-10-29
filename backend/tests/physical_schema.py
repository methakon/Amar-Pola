"""Static reader for the M1 migrations: table and column names, without a database."""
import pathlib, re

MIGRATIONS = pathlib.Path(__file__).resolve().parents[1] / "persistence" / "migrations"
SKIP = ("PRIMARY", "UNIQUE", "CHECK", "FOREIGN", "CONSTRAINT", "EXCLUDE", "LIKE")


def _strip_comments(sql):
    return "\n".join(re.sub(r"--.*$", "", line) for line in sql.splitlines())


def _split_top_level(body):
    parts, depth, cur = [], 0, []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def physical_tables(migrations_dir=MIGRATIONS):
    """Return {table: set(columns)} after applying every migration in file order (CREATE, ADD/DROP COLUMN)."""
    tables = {}
    for path in sorted(pathlib.Path(migrations_dir).glob("*.sql")):
        sql = _strip_comments(path.read_text())
        for m in re.finditer(r"CREATE TABLE\s+(?:IF NOT EXISTS\s+)?ap_m1\.(\w+)\s*\(", sql):
            start, depth, i = m.end(), 1, m.end()
            while depth:
                depth += {"(": 1, ")": -1}.get(sql[i], 0); i += 1
            cols = set()
            for part in _split_top_level(sql[start:i - 1]):
                first = re.match(r'"?(\w+)', part).group(1)
                if first.upper() not in SKIP:
                    cols.add(first)
            tables[m.group(1)] = cols
        for m in re.finditer(r"ALTER TABLE\s+(?:ONLY\s+)?ap_m1\.(\w+)\s+([^;]+);", sql):
            for act in _split_top_level(m.group(2)):
                a = re.match(r"ADD COLUMN\s+(?:IF NOT EXISTS\s+)?(\w+)", act, re.I)
                if a and m.group(1) in tables:
                    tables[m.group(1)].add(a.group(1))
                d = re.match(r"DROP COLUMN\s+(?:IF EXISTS\s+)?(\w+)", act, re.I)
                if d and m.group(1) in tables:
                    tables[m.group(1)].discard(d.group(1))
        for m in re.finditer(r"DROP TABLE\s+(?:IF EXISTS\s+)?ap_m1\.(\w+)", sql):
            tables.pop(m.group(1), None)
    return tables


def logical_entities(erd):
    """Return {entity: set(columns)} from the logical ERD JSON (column text like 'PK id : uuid', 'a, b : unique')."""
    out = {}
    for dom in erd["domains"]:
        for t in dom["tables"]:
            cols = set()
            for c in t.get("columns", []):
                head = re.split(r":|\u2192", c)[0]
                head = re.sub(r"^((PK/FK|PK|FK|UK)\s+)+", "", head.strip()).strip("() ")
                for name in head.split(","):
                    # A bare identifier (optionally "optional" or "?"); prose lines such as
                    # "invalidate cached child scopes" in the ERD are not columns.
                    m = re.fullmatch(r"([a-z_][a-z0-9_]*)\??(\s+optional)?", name.strip().strip("() "))
                    if m:
                        cols.add(m.group(1))
            out[t["name"]] = cols
    return out
