#!/usr/bin/env python3
"""Validate logical ERD references and counts without inferring SQL coverage."""
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
DEFAULT=ROOT/'docs/data-model/MADALASA_ALARKA_FIGMA_LOGICAL_ERD_V1_2026.json'
ARROW=re.compile(r'(?:→|->)\s*([a-z][a-z0-9_]*)')


def validate(erd):
    errors=[]
    domains=erd.get('domains',[])
    tables=[t for d in domains for t in d.get('tables',[])]
    names=[t['name'] for t in tables]
    if len(set(names))!=len(names):errors.append('duplicate ERD entity names')
    if erd.get('tableCount')!=len(tables):errors.append('ERD tableCount differs from actual entities')
    if erd.get('domainCount')!=len(domains):errors.append('ERD domainCount differs from actual domains')
    known=set(names)
    for table in tables:
        for column in table.get('columns',[]):
            if not isinstance(column,str):
                errors.append(table['name']+': non-string column entry')
                continue
            for target in ARROW.findall(column):
                if target not in known:errors.append(table['name']+': missing ERD entity '+target)
    return errors


if __name__=='__main__':
    errors=validate(json.loads((Path(sys.argv[1]) if len(sys.argv)>1 else DEFAULT).read_text()))
    if errors:
        print('ERD RELATION CHECK FAILED:\n- '+'\n- '.join(errors))
        raise SystemExit(1)
    print('ERD RELATION CHECK PASSED')
