#!/usr/bin/env python3
"""Offline strict structural linter for Madalasa–Alarka M1 OpenAPI 3.1 JSON-as-YAML.
Purpose: no network/pip required. Not a full OpenAPI conformance validator.
CI can additionally run Redocly/Spectral/openapi-spec-validator later.
"""
import json
import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/openapi-m1.yaml")
errors = []
try:
    doc = json.loads(path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"FAIL: unreadable JSON/YAML subset {path}: {exc}", file=sys.stderr)
    raise SystemExit(1)
def check(cond, message):
    if not cond:
        errors.append(message)
check(doc.get("openapi") == "3.1.0", "OpenAPI version must be 3.1.0")
check(doc.get("servers") and all(
    isinstance(s.get("url"), str) and s["url"].startswith("https://")
    for s in doc.get("servers", [])), "M1 servers require HTTPS")
sch = doc.get("components", {}).get("schemas", {})
sec = doc.get("components", {}).get("securitySchemes", {})
check("ParentOIDC" in sec and "DeviceBearer" in sec, "Missing M1 auth schemes")
expected = {
    "createFamily", "createChild", "listChildren", "getChild",
    "listChildDevices", "issuePairingCode", "redeemEnrollmentCode",
    "finishEnrollmentProof", "recordCapabilities", "recordHealth",
    "revokeDevice",
}
ids = []
operations = 0
for url, verbs in doc.get("paths", {}).items():
    check(url.startswith("/") and "?" not in url, f"Invalid route: {url}")
    for method, op in verbs.items():
        operations += 1
        where = f"{method.upper()} {url}"
        check(method in {"get", "post", "put", "patch", "delete"}, f"{where}: invalid verb")
        oid = op.get("operationId")
        ids.append(oid)
        check(oid in expected, f"{where}: not a permitted M1 operation {oid}")
        check(bool(op.get("tags")) and bool(op.get("summary")), f"{where}: tags/summary required")
        check("x-required-scope" in op, f"{where}: missing child/action scope declaration")
        check("security" in op, f"{where}: explicit principal security required")
        if op.get("security"):
            for requirement in op["security"]:
                for name in requirement:
                    check(name in sec, f"{where}: undefined security scheme {name}")
        else:
            check(url in {"/enrollment", "/enrollment/{enrollmentId}/proof"},
                  f"{where}: anonymous route beyond narrow pairing/proof")
        if method in {"post", "put", "patch"}:
            check(op.get("requestBody", {}).get("required") is True,
                  f"{where}: write operation requires typed body")
        declared = set(re.findall(r"\{(\w+)\}", url))
        actual = {p.get("name") for p in op.get("parameters", []) if p.get("in") == "path"}
        check(declared == actual, f"{where}: path params {declared} != {actual}")
        codes = op.get("responses", {})
        check(any(x in codes for x in ("200", "201", "202", "204")), f"{where}: no success")
        check("401" in codes and "403" in codes and "429" in codes,
              f"{where}: missing standardized 401/403/429 responses")
check(operations == 11, f"Expected exactly 11 M1 operations, got {operations}")
check(set(ids) == expected and len(ids) == len(set(ids)),
      f"Expected unique exact operationId set: {expected ^ set(ids)}")
for name, schema in sch.items():
    if schema.get("type") == "object":
        req = schema.get("required")
        check(isinstance(req, list), f"{name}: missing required[]")
        if isinstance(req, list):
            check(len(req) == len(set(req)), f"{name}: duplicate required")
            check(set(req).issubset(set(schema.get("properties", {}))),
                  f"{name}: required fields not declared")
        check(schema.get("additionalProperties") is False,
              f"{name}: enforce explicit fields")
def walk(value, at="root"):
    if isinstance(value, dict):
        if "$ref" in value:
            ref = value["$ref"]
            check(isinstance(ref, str) and
                  ref.startswith("#/components/schemas/") and
                  ref.split("/")[-1] in sch, f"{at}: unresolved ref {ref}")
        if "type" in value:
            ty = value["type"]
            # OpenAPI Security Scheme Objects have a separate 'type' vocabulary.
            # In particular, 'http' is valid in components.securitySchemes but
            # it is NOT a JSON Schema type inside components.schemas.
            if at.startswith("root/components/securitySchemes/") and at.count("/") == 3:
                security_types = {"apiKey", "http", "mutualTLS", "oauth2", "openIdConnect"}
                check(isinstance(ty, str) and ty in security_types,
                      f"{at}: invalid OpenAPI Security Scheme type {ty}")
            else:
                allowed = {"null", "integer", "number", "boolean", "string", "array", "object"}
                items = [ty] if isinstance(ty, str) else ty
                check(isinstance(items, list) and all(x in allowed for x in items),
                      f"{at}: invalid JSON Schema type {ty}")
        if isinstance(value.get("required"), str):
            errors.append(f"{at}: required field must be array")
        for k, v in value.items():
            walk(v, at + "/" + str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            walk(v, at + f"/{i}")
walk(doc)
if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    print(f"M1 OpenAPI FAIL ({len(errors)} errors; {operations} operations)", file=sys.stderr)
    raise SystemExit(1)
print(f"M1 OpenAPI structural lint PASS ({operations} M1 operations, {len(sch)} schemas, {len(ids)} unique operationIds)")
