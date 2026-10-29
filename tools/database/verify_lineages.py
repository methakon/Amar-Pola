#!/usr/bin/env python3
"""Destructive acceptance replay on the explicitly configured synthetic test DB only.

Exercises historical M1, populated upgrade, immutable-history adoption and clean
V2 convergence. Never targets development/production or clears recovery ledgers.
Run with the project's database virtualenv after building the native backend.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend/tests/database'))
sys.path.insert(0, str(ROOT / 'backend/tests'))
import manage as db

from test_m1_compatibility import seed_historical_compatibility, assert_historical_compatibility
from physical_schema import physical_tables


def application_shape(conn):
    columns = conn.execute("""SELECT table_name,column_name,data_type,udt_name,is_nullable,column_default
      FROM information_schema.columns WHERE table_schema='ap_m1'
      ORDER BY table_name,ordinal_position""").fetchall()
    acl = conn.execute("""SELECT c.relname,c.relkind,c.relrowsecurity,c.relforcerowsecurity,
      pg_get_userbyid(c.relowner),ARRAY(SELECT concat(a.grantee,':',a.grantor,':',a.privilege_type,':',a.is_grantable)
        FROM aclexplode(coalesce(c.relacl,acldefault('r',c.relowner))) a
        ORDER BY a.grantee,a.grantor,a.privilege_type,a.is_grantable) FROM pg_class c
      JOIN pg_namespace n ON n.oid=c.relnamespace
      WHERE n.nspname='ap_m1' AND c.relkind IN ('r','p','v') ORDER BY c.relname""").fetchall()
    constraints = conn.execute("""SELECT c.relname,k.conname,k.contype,k.convalidated,
      pg_get_constraintdef(k.oid) FROM pg_constraint k JOIN pg_class c ON c.oid=k.conrelid
      JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ap_m1'
      ORDER BY c.relname,k.conname""").fetchall()
    indexes = conn.execute("SELECT indexname,indexdef FROM pg_indexes WHERE schemaname='ap_m1' ORDER BY indexname").fetchall()
    functions = conn.execute("""SELECT p.proname,pg_get_function_identity_arguments(p.oid),p.prosrc,
      p.prosecdef,p.proconfig,p.provolatile,pg_get_userbyid(p.proowner),
      ARRAY(SELECT concat(a.grantee,':',a.grantor,':',a.privilege_type,':',a.is_grantable)
        FROM aclexplode(coalesce(p.proacl,acldefault('f',p.proowner))) a
        ORDER BY a.grantee,a.grantor,a.privilege_type,a.is_grantable)
      FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='ap_m1'
      ORDER BY p.proname,pg_get_function_identity_arguments(p.oid)""").fetchall()
    return dict(columns=columns, acl=acl, constraints=constraints, indexes=indexes, functions=functions)


def main():
    for role in ('admin', *db.ROLES):
        target = db.conninfo_to_dict(db.configuration()['test'][role])
        db.validate_target(target)
        if target['dbname'] != db.DATABASES['test']:
            raise RuntimeError('refusing non-test database')
    db.assert_container('test')
    print('RESETTING ONLY synthetic test database; recovery ledger retained', flush=True)
    db.reset('test')
    db.create(targets=['test'])
    db.migrate('test', lineage='m1')
    container = db.container_for('test')
    # Original scripts retain their exact upstream bytes. Role switches inside
    # SQL exercise restricted M1 API roles; fixtures alone use local admin.
    for name in ('m1_tenant_isolation.sql', 'm1_credential_lifecycle.sql', 'm1_enrollment.sql', 'm1_idempotency.sql'):
        subprocess.run(['docker','exec','-i',container,'psql','-X','-v','ON_ERROR_STOP=1',
                '-U','postgres','-d',db.DATABASES['test']], input=(ROOT/'backend/tests'/name).read_text(), text=True, check=True, timeout=30)
    subprocess.run(['docker','exec','-i',container,'env','PGUSER=postgres','PGDATABASE='+db.DATABASES['test'],
            'bash','-s'], input=(ROOT/'backend/tests/m1_idempotency_concurrency.sh').read_text(), text=True, check=True, timeout=30)
    with db.connect('test','admin',autocommit=False) as conn:
        actual = {r[0]: set() for r in conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='ap_m1'")}
        for table, col in conn.execute("SELECT table_name,column_name FROM information_schema.columns WHERE table_schema='ap_m1'"):
            if table in actual:
                actual[table].add(col)
        assert actual == physical_tables(), 'historical M1 live/static catalog divergence'
        assert len(actual) == 18, 'historical checkpoint is exactly 18 tables'
        expected = seed_historical_compatibility(conn)
        conn.commit()
    print('Historical M1: original SQL + concurrency + 18-table live catalog PASS', flush=True)
    db.migrate('test')
    db.verify_lineage_security('test')
    with db.connect('test','admin',autocommit=False) as conn:
        assert_historical_compatibility(conn, expected)
        upgraded_shape = application_shape(conn)
    print('Populated M1 -> V2: rows, device/key state and fail-closed credentials PASS', flush=True)
    db.reset('test')
    db.create(targets=['test'])
    db.migrate('test')
    db.verify_lineage_security('test')
    with db.connect('test','admin',autocommit=False) as conn:
        fresh = application_shape(conn)
        for category in fresh:
            if fresh[category] != upgraded_shape[category]:
                expected = {repr(row) for row in upgraded_shape[category]}
                actual = {repr(row) for row in fresh[category]}
                print('UPGRADE ONLY',category,sorted(expected-actual),flush=True)
                print('FRESH ONLY',category,sorted(actual-expected),flush=True)
                raise AssertionError('fresh/upgrade schema or ACL divergence: '+category)
        old = conn.execute('SELECT * FROM ma_migrations.history ORDER BY version').fetchall()
        conn.execute('TRUNCATE ma_migrations.lineage_history')
        conn.commit()
    db.migrate('test')
    with db.connect('test','admin',autocommit=False) as conn:
        assert conn.execute('SELECT * FROM ma_migrations.history ORDER BY version').fetchall() == old
        assert conn.execute('SELECT count(*) FROM ma_migrations.lineage_history').fetchone()[0] == 18
    print('Clean V2 convergence + exact legacy adoption without history mutation PASS', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
