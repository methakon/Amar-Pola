#!/usr/bin/env python3
"""Tests for the M1 OpenAPI linter: it must pass the real contract AND fail broken ones.

Run:  python3 backend/tests/test_lint_openapi_m1.py
Standard library only.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lint_openapi_m1 as linter  # noqa: E402

CONTRACT = HERE.parent.parent / "docs" / "openapi-m1.yaml"
REAL = json.loads(CONTRACT.read_text(encoding="utf-8"))


def op(doc, operation_id):
    for verbs in doc["paths"].values():
        for candidate in verbs.values():
            if candidate["operationId"] == operation_id:
                return candidate
    raise KeyError(operation_id)


def errors_for(doc):
    return linter.lint(doc)[0]


class RealContract(unittest.TestCase):
    def test_real_contract_passes(self):
        self.assertEqual(errors_for(REAL), [])

    def test_http_security_schemes_are_accepted(self):
        # Regression: the first linter rejected OpenAPI's "type: http" as a JSON Schema type.
        self.assertEqual(REAL["components"]["securitySchemes"]["ParentOIDC"]["type"], "http")
        self.assertFalse([e for e in errors_for(REAL) if "securityScheme" in e or "type http" in e])

    def test_operations_do_not_share_one_copied_error_set(self):
        error_sets = set()
        for verbs in REAL["paths"].values():
            for candidate in verbs.values():
                error_sets.add(tuple(sorted(c for c in candidate["responses"] if not c.startswith("2"))))
        self.assertGreaterEqual(len(error_sets), 5)


class BrokenContractsFail(unittest.TestCase):
    def mutate(self, fn):
        doc = copy.deepcopy(REAL)
        fn(doc)
        return errors_for(doc)

    def assertFails(self, fn, fragment):
        found = self.mutate(fn)
        self.assertTrue(any(fragment in e for e in found), f"expected '{fragment}' in {found}")

    def test_invalid_schema_type(self):
        self.assertFails(lambda d: d["components"]["schemas"]["Receipt"]["properties"]["id"]
                         .update(type="strin"), "invalid JSON Schema type")

    def test_bad_security_scheme_type(self):
        self.assertFails(lambda d: d["components"]["securitySchemes"]["DeviceBearer"]
                         .update(type="basic"), "invalid type")

    def test_http_scheme_without_scheme(self):
        self.assertFails(lambda d: d["components"]["securitySchemes"]["DeviceBearer"]
                         .pop("scheme"), "http scheme required")

    def test_get_with_413(self):
        def go(d):
            op(d, "getChild")["responses"]["413"] = copy.deepcopy(op(d, "getChild")["responses"]["404"])
        self.assertFails(go, "413 cannot occur on an operation without a request body")

    def test_gone_on_a_list(self):
        def go(d):
            op(d, "listChildren")["responses"]["410"] = copy.deepcopy(op(d, "listChildren")["responses"]["404"])
        self.assertFails(go, "410")

    def test_missing_429(self):
        self.assertFails(lambda d: op(d, "getChild")["responses"].pop("429"), "missing 429")

    def test_missing_400_when_operation_takes_input(self):
        self.assertFails(lambda d: op(d, "getChild")["responses"].pop("400"), "declares no 400")

    def test_400_on_operation_without_input(self):
        def go(d):
            op(d, "listFamilies")["responses"]["400"] = copy.deepcopy(op(d, "getChild")["responses"]["400"])
        self.assertFails(go, "400 cannot occur")

    def test_authenticated_operation_without_401(self):
        self.assertFails(lambda d: op(d, "getChild")["responses"].pop("401"), "must declare 401")

    def test_unexpected_anonymous_route(self):
        self.assertFails(lambda d: op(d, "getChild").update(security=[]), "anonymous route")

    def test_error_response_must_use_error_schema(self):
        def go(d):
            op(d, "getChild")["responses"]["404"]["content"]["application/json"]["schema"] = {"type": "object"}
        self.assertFails(go, "shared Error schema")

    def test_undefined_security_scheme(self):
        self.assertFails(lambda d: op(d, "getChild").update(security=[{"Nope": []}]), "undefined security scheme")

    def test_object_schema_must_forbid_extra_fields(self):
        self.assertFails(lambda d: d["components"]["schemas"]["Receipt"].pop("additionalProperties"),
                         "enforce explicit fields")

    def test_non_https_server(self):
        self.assertFails(lambda d: d["servers"][0].update(url="http://api.example.invalid/v1"), "HTTPS")

    def test_extra_operation_is_rejected(self):
        def go(d):
            d["paths"]["/extra"] = {"get": copy.deepcopy(op(d, "getChild"))}
            d["paths"]["/extra"]["get"]["operationId"] = "extra"
            d["paths"]["/extra"]["get"]["parameters"] = []
        self.assertFails(go, "not a permitted M1 operation")

    def test_unresolved_schema_ref(self):
        def go(d):
            d["components"]["schemas"]["Receipt"]["properties"]["id"] = {"$ref": "#/components/schemas/Missing"}
        self.assertFails(go, "unresolved ref")

    def test_property_named_type_is_not_a_false_positive(self):
        def go(d):
            d["components"]["schemas"]["Receipt"]["properties"]["type"] = {"type": "string"}
        self.assertEqual(self.mutate(go), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
