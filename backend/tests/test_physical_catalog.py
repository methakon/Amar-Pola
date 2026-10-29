"""The catalog checker must also fail when things drift (a checker that cannot fail proves nothing)."""
import copy, json, pathlib, sys, tempfile, unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_physical_catalog as cc  # noqa: E402
import physical_schema as ps  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.mapping = json.loads(cc.MAPPING.read_text())
        self.erd = json.loads((cc.ROOT / self.mapping["erd"]).read_text())
        self.physical = ps.physical_tables()
        self.logical = ps.logical_entities(self.erd)

    def errors(self, mapping=None, physical=None, logical=None):
        return cc.check(mapping or self.mapping, self.erd, physical or self.physical, logical or self.logical)


class RealRepository(Base):
    def test_clean(self):
        self.assertEqual(self.errors(), [])

    def test_report_in_sync(self):
        self.assertEqual(cc.REPORT.read_text(), cc.render(self.mapping, self.erd, self.physical, self.logical))

    def test_every_m1_table_accounted_for(self):
        names = {t["physical"] for t in self.mapping["tables"]} | {w["physical"] for w in self.mapping["physical_without_entity"]}
        self.assertEqual(names, set(self.physical))


class DriftIsCaught(Base):
    def test_new_unmapped_table(self):
        p = copy.deepcopy(self.physical); p["new_table"] = {"id"}
        self.assertTrue(any("new_table" in e and "not in the mapping" in e for e in self.errors(physical=p)))

    def test_new_column_on_mapped_table(self):
        p = copy.deepcopy(self.physical); p["children"].add("birth_date")
        self.assertTrue(any("children" in e and "physical-only" in e for e in self.errors(physical=p)))

    def test_dropped_column(self):
        p = copy.deepcopy(self.physical); p["pairing_codes"].discard("attempt_count")
        self.assertTrue(any("pairing_codes" in e for e in self.errors(physical=p)))

    def test_erd_column_added(self):
        l = copy.deepcopy(self.logical); l["families"].add("extra")
        self.assertTrue(any("families" in e and "ERD-only" in e for e in self.errors(logical=l)))

    def test_erd_entity_removed(self):
        l = copy.deepcopy(self.logical); del l["children"]
        self.assertTrue(any("children" in e and "does not exist" in e for e in self.errors(logical=l)))

    def test_bad_rename_source_and_target(self):
        m = copy.deepcopy(self.mapping)
        next(t for t in m["tables"] if t["physical"] == "families")["column_renames"] = {"nope": "status"}
        self.assertTrue(any("rename source nope" in e for e in self.errors(mapping=m)))
        m = copy.deepcopy(self.mapping)
        next(t for t in m["tables"] if t["physical"] == "families")["column_renames"] = {"state": "nope"}
        self.assertTrue(any("rename target nope" in e for e in self.errors(mapping=m)))

    def test_entity_mapped_twice(self):
        m = copy.deepcopy(self.mapping)
        next(t for t in m["tables"] if t["physical"] == "devices")["logical"] = "children"
        self.assertTrue(any("already mapped" in e for e in self.errors(mapping=m)))

    def test_missing_note(self):
        m = copy.deepcopy(self.mapping); m["tables"][0]["note"] = " "
        self.assertTrue(any("note" in e for e in self.errors(mapping=m)))

    def test_mapping_names_table_no_migration_creates(self):
        m = copy.deepcopy(self.mapping); m["tables"].append({**m["tables"][0], "physical": "ghost"})
        self.assertTrue(any("ghost" in e for e in self.errors(mapping=m)))

    def test_entity_count_change(self):
        e = copy.deepcopy(self.erd); e["tableCount"] = 121
        self.assertTrue(any("tableCount" in x for x in cc.check(self.mapping, e, self.physical, self.logical)))

    def test_stale_report(self):
        text = cc.render(self.mapping, self.erd, self.physical, self.logical)
        m = copy.deepcopy(self.mapping); m["tables"][0]["note"] += " changed"
        self.assertNotEqual(text, cc.render(m, self.erd, self.physical, self.logical))


class Parser(unittest.TestCase):
    def test_duplicate_create_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate CREATE TABLE'):
            self.parse('CREATE TABLE ap_m1.a(id int); CREATE TABLE ap_m1.a(other int);')

    def parse(self, sql):
        with tempfile.TemporaryDirectory() as d:
            pathlib.Path(d, "0001_x.sql").write_text(sql)
            return ps.physical_tables(d)

    def test_columns_constraints_comments_and_alter(self):
        t = self.parse("""
          CREATE TABLE ap_m1.a (
            id uuid PRIMARY KEY, -- comment, with comma
            n numeric(10,2) NOT NULL,
            expires_at timestamptz,
            CHECK(expires_at > now()),
            UNIQUE(id, n),
            CONSTRAINT c CHECK (n > 0)
          );
          ALTER TABLE ap_m1.a ADD COLUMN extra text, ADD COLUMN IF NOT EXISTS more int;
          CREATE TABLE ap_m1.gone (id int);
          DROP TABLE ap_m1.gone;
        """)
        self.assertEqual(t, {"a": {"id", "n", "expires_at", "extra", "more"}})

    def test_erd_column_forms(self):
        erd = {"domains": [{"tables": [{"name": "x", "columns": [
            "PK FK device_id", "PK (a, b)", "FK c → y", "d, e : time", "f : enum?", "g, h optional", "invalidate cached child scopes"]}]}]}
        self.assertEqual(ps.logical_entities(erd)["x"], {"device_id", "a", "b", "c", "d", "e", "f", "g", "h"})


if __name__ == "__main__":
    unittest.main()
