#!/usr/bin/env python3
"""Bounded, synthetic-only local PostgreSQL lifecycle and atomic migrations.

Secrets remain in .local-db (0700/0600), never command arguments or logs.
Only two exact database names, loopback and our labelled Docker container are accepted.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import time
from uuid import uuid4,uuid5,NAMESPACE_URL

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo, conninfo_to_dict

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-db'
CONFIG = LOCAL / 'connection.json'
MIGRATIONS = ROOT / 'backend/persistence/migrations'
CONTAINER = 'madalasa-local-postgres'
MEMORY_CONTAINER = 'madalasa-memory-test-postgres'
BASELINE_SHA256 = 'e6014a2e2512a793efc320b39be8d0f1b5a4de8b9f7560d444d88aa2ffa5b3fe'
DATABASES = {'dev': 'madalasa_alarka_dev', 'test': 'madalasa_alarka_test'}
COMPOSE = ['docker', 'compose', '-f', str(ROOT / 'infra/local/compose.yaml')]
ROLES = {'migration': ('madalasa_migrator', ['ap_m1_owner', 'ap_m1_auth', 'ap_db_executor']),
         'runtime': ('madalasa_dev', ['ap_m1_api']),
         'auth': ('madalasa_auth', ['ap_auth_issuer']),
         'billing': ('madalasa_billing', ['ap_billing_verifier'])}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def private_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, 'w') as stream:
        stream.write(content)
    path.chmod(0o600)


def validate_target(config):
    if config.get('host') not in ('127.0.0.1', 'localhost', '::1') or config.get('hostaddr',config.get('host')) not in ('127.0.0.1','localhost','::1') or config.get('service'):
        raise ValueError('Refusing non-loopback database target')
    if config.get('dbname') not in DATABASES.values():
        raise ValueError('Refusing database outside the two named synthetic databases')
    if int(config.get('port', 0)) not in (15432,15433) or (int(config.get('port',0))==15433 and config.get('dbname')!=DATABASES['test']):
        raise ValueError('Refusing an unconfigured database port')


def configuration():
    if not CONFIG.exists():
        raise ValueError('Run tools/database/db init first')
    if CONFIG.stat().st_mode & 0o077:
        raise ValueError('connection.json must have mode 0600')
    return json.loads(CONFIG.read_text())


def connect(database='test', role='migration', autocommit=True):
    dsn = configuration()[database][role]
    validate_target(conninfo_to_dict(dsn))
    return psycopg.connect(dsn, autocommit=autocommit, connect_timeout=5)


def container_for(database='test'):
    name=configuration()[database].get('container',CONTAINER)
    if name not in (CONTAINER,MEMORY_CONTAINER) or (name==MEMORY_CONTAINER and database!='test'):
        raise ValueError('Unrecognized local database container')
    return name


def assert_container(database='test'):
    name=container_for(database)
    info = subprocess.run(['docker', 'inspect', name], capture_output=True, text=True, check=True)
    item = json.loads(info.stdout)[0]
    if item['Config'].get('Labels', {}).get('com.madalasa.local-db') != 'synthetic':
        raise ValueError('Container is not the labelled synthetic database')
    mounts = item.get('Mounts', [])
    if name==MEMORY_CONTAINER:
        if item['Config'].get('Labels',{}).get('com.madalasa.local-db-root')!=str(ROOT):
            raise ValueError('Memory test container belongs to a different checkout')
        if '/var/lib/postgresql/data' not in item.get('HostConfig',{}).get('Tmpfs',{}) and not any(m.get('Type')=='tmpfs' and m['Destination']=='/var/lib/postgresql/data' for m in mounts):
            raise ValueError('Memory test container has unexpected storage')
        return
    expected = str((LOCAL / 'pgdata').resolve())
    if not any(m['Source'] == expected and m['Destination'] == '/var/lib/postgresql/data' for m in mounts):
        raise ValueError('Container belongs to a different checkout; refusing to touch it')


def quarantine_marker(database):
    suffix='-memory' if container_for(database)==MEMORY_CONTAINER else ''
    return LOCAL/('quarantine-'+database+suffix+'.json')


def init():
    LOCAL.mkdir(exist_ok=True)
    LOCAL.chmod(0o700)
    if CONFIG.exists():
        configuration()
        print('Existing local credentials preserved')
        return
    password = secrets.token_urlsafe(36)
    passwords = {key: secrets.token_urlsafe(36) for key in ROLES}
    config = {}
    for database, name in DATABASES.items():
        base = dict(host='127.0.0.1', port=15432, dbname=name, sslmode='disable', application_name='madalasa-local')
        config[database] = {'admin': make_conninfo(**base, user='postgres', password=password)}
        for role, (user, _) in ROLES.items():
            config[database][role] = make_conninfo(**base, user=user, password=passwords[role])
    private_write(LOCAL / 'postgres-password', password + '\n')
    private_write(CONFIG, json.dumps(config, indent=2) + '\n')
    private_write(LOCAL / 'backend.env', 'DB_HOST=127.0.0.1\nDB_PORT=15432\nDB_NAME=madalasa_alarka_dev\nDB_USER=madalasa_dev\nDB_PASSWORD=' + passwords['runtime'] + '\nDB_SSLMODE=disable\n')
    print('Created ignored private credentials (0600); no password printed')


def start():
    init()
    if shutil.disk_usage(LOCAL).free < 2 * 1024**3:
        raise ValueError('At least 2 GiB free disk required for bounded local DB')
    existing = subprocess.run(['docker', 'container', 'inspect', CONTAINER], capture_output=True)
    if existing.returncode == 0:
        assert_container('dev')
    subprocess.run(COMPOSE + ['up', '-d', '--wait'], cwd=ROOT, check=True)
    assert_container('dev')
    print('Dedicated PostgreSQL healthy on 127.0.0.1:15432 (512 MiB / 1 CPU)')


def start_memory_test():
    """Use a separate volatile test instance; never move/reset persistent dev."""
    cfg=configuration()
    env=os.environ.copy();env['MA_LOCAL_CHECKOUT']=str(ROOT)
    command=['docker','compose','-f',str(ROOT/'infra/local/compose.memory-test.yaml')]
    existing=subprocess.run(['docker','inspect',MEMORY_CONTAINER],capture_output=True)
    if existing.returncode==0:
        item=json.loads(existing.stdout)[0]
        if item['Config'].get('Labels',{}).get('com.madalasa.local-db-root')!=str(ROOT):
            raise ValueError('Refusing another checkout memory test container')
    subprocess.run(command+['up','-d','--wait'],cwd=ROOT,env=env,check=True)
    for kind in ('admin',*ROLES):
        values=conninfo_to_dict(cfg['test'][kind]);values['port']='15433'
        cfg['test'][kind]=make_conninfo(**values)
    cfg['test']['container']=MEMORY_CONTAINER
    private_write(CONFIG,json.dumps(cfg,indent=2)+'\n')
    assert_container('test')
    create(targets=['test'])
    print('Isolated RAM-backed test database on 127.0.0.1:15433; persistent dev unchanged; fsync remains enabled')


def create(targets=None):
    cfg = configuration()
    for target in targets or DATABASES:
        assert_container(target)
        admin_args = conninfo_to_dict(cfg[target]['admin'])
        admin_args['dbname'] = 'postgres'
        with psycopg.connect(**admin_args, autocommit=True) as admin:
            for name, bypass in [('ap_m1_owner', False), ('ap_m1_api', False), ('ap_m1_auth', True),
                                 ('ap_db_executor', True), ('ap_auth_issuer', False), ('ap_billing_verifier', False), ('ap_service_worker', False), ('ap_privacy_worker', False)]:
                if not admin.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (name,)).fetchone():
                    admin.execute(sql.SQL('CREATE ROLE {} NOLOGIN NOSUPERUSER {}').format(sql.Identifier(name), sql.SQL('BYPASSRLS' if bypass else 'NOBYPASSRLS')))
            for kind, (name, groups) in ROLES.items():
                args = conninfo_to_dict(cfg[target][kind])
                if not admin.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (name,)).fetchone():
                    admin.execute(sql.SQL('CREATE ROLE {} LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE').format(sql.Identifier(name)))
                admin.execute(sql.SQL('ALTER ROLE {} PASSWORD {}').format(sql.Identifier(name), sql.Literal(args['password'])))
                for group in groups:
                    admin.execute(sql.SQL('GRANT {} TO {}').format(sql.Identifier(group), sql.Identifier(name)))
            name=DATABASES[target]
            if not admin.execute('SELECT 1 FROM pg_database WHERE datname=%s', (name,)).fetchone():
                admin.execute(sql.SQL("CREATE DATABASE {} OWNER madalasa_migrator TEMPLATE template0 ENCODING 'UTF8'").format(sql.Identifier(name)))
        with connect(target, 'admin') as conn:
            conn.execute('REVOKE CREATE ON SCHEMA public FROM PUBLIC')
            conn.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto')
            conn.execute('CREATE EXTENSION IF NOT EXISTS postgis')
            conn.execute('CREATE SCHEMA IF NOT EXISTS ap_m1 AUTHORIZATION ap_m1_owner')
            conn.execute('GRANT CREATE ON SCHEMA ap_m1 TO ap_m1_auth,ap_db_executor')
            conn.execute('GRANT CREATE ON SCHEMA public TO madalasa_migrator')
            # ALTER FUNCTION OWNER requires the target owner CREATE on its schema.
            # No runtime user is a member of any function-owner role.
            conn.execute('ALTER DATABASE ' + DATABASES[target] + " SET timezone TO 'UTC'")
            conn.execute('REVOKE ALL ON DATABASE ' + DATABASES[target] + ' FROM PUBLIC')
            for kind in ROLES:
                if kind != 'migration' and quarantine_marker(target).exists():
                    continue
                conn.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO {}').format(sql.Identifier(DATABASES[target]), sql.Identifier(ROLES[kind][0])))
    print('Development and test databases created; PostGIS and pgcrypto installed')


def transaction_body(text):
    # Historical migration owns a transaction. Remove only its outer top-level
    # pair, not BEGIN/END inside dollar-quoted PL/pgSQL. Do not edit its file.
    opening = re.search(r'(?m)^BEGIN;\s*$', text)
    closing = list(re.finditer(r'(?m)^COMMIT;\s*$', text))
    if opening and closing:
        last = closing[-1]
        return text[:opening.start()] + text[opening.end():last.start()] + text[last.end():]
    return text


def load_migration_manifest(verify=True):
    """Explicit identities, never infer lineage from a numeric filename prefix."""
    data = json.loads((ROOT / 'backend/persistence/migration-lineages.json').read_text())
    entries = data['migrations']
    ids, paths = set(), set()
    for entry in entries:
        identity, relative = entry['id'], entry['path']
        if identity in ids or relative in paths:
            raise ValueError('Duplicate migration identity or path')
        ids.add(identity); paths.add(relative)
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT.resolve()):
            raise ValueError('Migration outside checkout')
        digest = entry['sha256']
        if digest is None and entry.get('published', True):
            raise ValueError('Published migration has no checksum: ' + identity)
        if digest is not None and not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('Invalid migration checksum: ' + identity)
        if verify and digest is not None and (not path.is_file() or sha256(path) != digest):
            raise ValueError('Migration checksum drift: ' + identity)
    expected = {'common:0001', 'compat:m1_pre_v2_0016'} | {'m1:%04d' % n for n in range(2, 5)} | {'v2:%04d' % n for n in range(2, 19)}
    if ids != expected:
        raise ValueError('Incomplete or unknown manifest identities')
    return entries


def migration_plan(entries, lineage='v2', through=None, applied=()):
    if lineage not in ('m1', 'v2'):
        raise ValueError('Unknown lineage')
    known = {e['id']: e for e in entries}
    applied = set(applied)
    if applied - known.keys():
        raise ValueError('Unknown applied identity')
    if lineage == 'm1' and any(i.startswith(('v2:', 'compat:')) for i in applied):
        raise ValueError('V2 to M1 downgrade forbidden')
    upgrade = lineage == 'v2' and any(i.startswith('m1:') for i in applied)
    ids = ['common:0001']
    if lineage == 'm1':
        ids += ['m1:%04d' % n for n in range(2, 5)]
    else:
        ids += ['v2:%04d' % n for n in range(2, 16)]
        if upgrade:
            ids += ['compat:m1_pre_v2_0016']
        ids += ['v2:0016', 'v2:0017', 'v2:0018']
    if through:
        target = through if ':' in through else ('common:0001' if through == '0001' else lineage + ':' + through)
        if target not in ids:
            raise ValueError('Through identity outside selected lineage')
        ids = ids[:ids.index(target) + 1]
    return [known[i] for i in ids]


def validate_migration_history(entries, legacy_rows, lineage_rows, schema_has_objects=False):
    """Read-only validation of *all* rows, including failures outside --through."""
    known = {e['id']: e for e in entries}
    by_name = {Path(e['path']).name: e for e in entries}
    applied, legacy_lineages = set(), set()
    for rows, namespaced in ((legacy_rows, False), (lineage_rows, True)):
        seen = {}
        for version, filename, checksum, status in rows:
            entry = known.get(version) if namespaced or ':' in version else by_name.get(filename)
            if (entry is None or filename != Path(entry['path']).name
                    or checksum is None or checksum != entry['sha256']
                    or status not in ('APPLIED', 'FAILED')
                    or version not in (entry['id'], entry['id'].split(':')[-1])):
                raise ValueError('Unknown or drifting migration history: ' + str(version))
            identity = entry['id']
            if identity in seen and (namespaced or seen[identity] == status):
                raise ValueError('Duplicate migration history identity')
            seen[identity] = status
            if not namespaced and ':' not in version and identity != 'common:0001':
                legacy_lineages.add(identity.split(':')[0])
            if status == 'APPLIED':
                applied.add(identity)
    if len(legacy_lineages) > 1:
        raise ValueError('Mixed legacy migration lineages')
    if not applied and schema_has_objects:
        raise ValueError('Untracked manual application schema; refusing adoption')
    if applied:
        if 'common:0001' not in applied:
            raise ValueError('Missing common baseline history')
        m1 = sorted(i for i in applied if i.startswith('m1:'))
        if m1 != ['m1:%04d' % n for n in range(2, 2 + len(m1))]:
            raise ValueError('Gapped M1 history')
        v2 = sorted(i for i in applied if i.startswith('v2:'))
        if v2 != ['v2:%04d' % n for n in range(2, 2 + len(v2))]:
            raise ValueError('Gapped V2 history')
        bridge = 'compat:m1_pre_v2_0016' in applied
        if bridge and (not m1 or 'v2:0015' not in applied):
            raise ValueError('Out-of-order compatibility bridge')
        if m1 and 'v2:0016' in applied and not bridge:
            raise ValueError('M1 upgrade missing compatibility bridge')
    return applied


def preflight_migration_plan(plan):
    """Pin and buffer every selected source before the first DDL statement."""
    sources = {}
    for entry in plan:
        path = ROOT / entry['path']
        if entry['sha256'] is None or not path.is_file():
            raise ValueError('Unpublished migration must be pinned before apply: ' + entry['id'])
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != entry['sha256']:
            raise ValueError('Migration checksum drift: ' + entry['id'])
        sources[entry['id']] = transaction_body(content.decode('utf-8'))
    return sources


def migrate(database, through=None, lineage='v2'):
    entries = load_migration_manifest()
    if sha256(MIGRATIONS / '0001_m1_identity.sql') != BASELINE_SHA256:
        raise ValueError('Historical 0001 checksum changed')
    migration_plan(entries, lineage, through)
    assert_container(database)
    with connect(database) as conn:
        conn.execute("SELECT pg_advisory_lock(hashtextextended('madalasa-migrations',0))")
        try:
            legacy_rows, lineage_rows = [], []
            for table, rows in (('history', legacy_rows), ('lineage_history', lineage_rows)):
                if conn.execute('SELECT to_regclass(%s)', ('ma_migrations.' + table,)).fetchone()[0]:
                    rows.extend(conn.execute('SELECT version,filename,checksum,status FROM ma_migrations.' + table).fetchall())
            objects = conn.execute("""SELECT EXISTS (
                SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
                WHERE n.nspname='ap_m1'
                UNION ALL SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
                WHERE n.nspname='ap_m1')""").fetchone()[0]
            applied = validate_migration_history(entries, legacy_rows, lineage_rows, objects)
            plan = migration_plan(entries, lineage, through, applied)
            sources = preflight_migration_plan(plan)
            upgrading = lineage == 'v2' and any(i.startswith('m1:') for i in applied)
            external_quarantine = False
            if upgrading:
                marker = quarantine_marker(database)
                external_quarantine = marker.exists() and json.loads(marker.read_text()).get('state') != 'LINEAGE_UPGRADE'
                quarantine(database)
                if not external_quarantine:
                    private_write(marker, json.dumps({'database': DATABASES[database], 'state': 'LINEAGE_UPGRADE'}) + '\n')
            conn.execute('CREATE SCHEMA IF NOT EXISTS ma_migrations')
            conn.execute('REVOKE ALL ON SCHEMA ma_migrations FROM PUBLIC')
            for table in ('history', 'lineage_history'):
                conn.execute("""CREATE TABLE IF NOT EXISTS ma_migrations.""" + table + """ (
                    version text PRIMARY KEY, filename text NOT NULL, checksum text NOT NULL,
                    executed_at timestamptz NOT NULL DEFAULT now(), status text NOT NULL CHECK(status IN ('APPLIED','FAILED')),
                    sqlstate text, execution_ms integer NOT NULL DEFAULT 0)""")
                conn.execute('REVOKE ALL ON ma_migrations.' + table + ' FROM PUBLIC')
            known = {e['id']: e for e in entries}
            # Adoption never changes the original history rows, even FAILED rows.
            for identity in sorted(applied):
                entry = known[identity]
                conn.execute("""INSERT INTO ma_migrations.lineage_history(version,filename,checksum,status)
                    VALUES(%s,%s,%s,'APPLIED') ON CONFLICT(version) DO NOTHING""",
                    (identity, Path(entry['path']).name, entry['sha256']))
            for entry in plan:
                identity, checksum = entry['id'], entry['sha256']
                filename = Path(entry['path']).name
                if identity in applied:
                    print('UNCHANGED ' + filename)
                    continue
                begun = time.monotonic()
                try:
                    with conn.transaction():
                        conn.execute(sources[identity], prepare=False)
                        if identity == 'common:0001':
                            conn.execute('GRANT CREATE ON SCHEMA ap_m1 TO ap_m1_auth,ap_db_executor')
                            conn.execute('GRANT USAGE ON SCHEMA ap_m1 TO ap_auth_issuer,ap_billing_verifier')
                        elapsed = int((time.monotonic()-begun)*1000)
                        conn.execute("""INSERT INTO ma_migrations.lineage_history(version,filename,checksum,status,execution_ms)
                            VALUES(%s,%s,%s,'APPLIED',%s) ON CONFLICT(version) DO UPDATE SET
                            status='APPLIED',executed_at=now(),sqlstate=NULL,execution_ms=excluded.execution_ms
                            WHERE ma_migrations.lineage_history.status='FAILED' """,
                            (identity,filename,checksum,elapsed))
                        # Preserve numeric versions for old status/export readers
                        # unless occupied by immutable rows from another lineage.
                        version = identity.split(':')[-1] if identity.startswith(('common:', 'v2:', 'm1:')) else identity
                        if upgrading or any(row[0] == version for row in legacy_rows):
                            version = identity
                        conn.execute("""INSERT INTO ma_migrations.history(version,filename,checksum,status,execution_ms)
                            VALUES(%s,%s,%s,'APPLIED',%s) ON CONFLICT(version) DO NOTHING""",
                            (version,filename,checksum,elapsed))
                        applied.add(identity)
                    print('APPLIED ' + filename)
                except psycopg.Error as exc:
                    conn.execute("""INSERT INTO ma_migrations.lineage_history(version,filename,checksum,status,sqlstate)
                        VALUES(%s,%s,%s,'FAILED',%s) ON CONFLICT(version) DO UPDATE SET
                        status='FAILED',sqlstate=excluded.sqlstate,executed_at=now()
                        WHERE ma_migrations.lineage_history.status='FAILED' """,
                        (identity,filename,checksum,exc.sqlstate))
                    print('FAILED ' + filename + ' SQLSTATE=' + str(exc.sqlstate), file=sys.stderr)
                    raise
            if upgrading and 'v2:0018' in applied:
                verify_lineage_security(database)
                if not external_quarantine:
                    open_after_restore(database)
        finally:
            conn.execute("SELECT pg_advisory_unlock(hashtextextended('madalasa-migrations',0))")


def verify_lineage_security(database):
    """Final upgrade gate: FORCE RLS plus PUBLIC/role ACL checks before reopening."""
    verify(database)
    with connect(database, 'admin') as conn:
        public_execute = conn.execute("""SELECT p.proname FROM pg_proc p
            JOIN pg_namespace n ON n.oid=p.pronamespace
            CROSS JOIN LATERAL aclexplode(coalesce(p.proacl,acldefault('f',p.proowner))) a
            WHERE n.nspname IN ('ap_m1','ma_recovery')
            AND a.grantee=0 AND a.privilege_type='EXECUTE'""").fetchall()
        if public_execute:
            raise ValueError('PUBLIC function execute ACL remains after lineage upgrade')
        unsafe = conn.execute("""SELECT r.rolname FROM pg_roles r
            WHERE r.rolname=ANY(%s) AND (r.rolsuper OR r.rolbypassrls OR r.rolcreaterole
              OR pg_has_role(r.oid,'ap_m1_owner','MEMBER')
              OR pg_has_role(r.oid,'ap_m1_auth','MEMBER')
              OR pg_has_role(r.oid,'ap_db_executor','MEMBER'))""",
            ([ROLES[k][0] for k in ('runtime','auth','billing')] + ['ap_m1_api'],)).fetchall()
        if unsafe:
            raise ValueError('Unsafe runtime role ACL after lineage upgrade')
        writable_schema = conn.execute("""SELECT n.nspname FROM pg_namespace n
            CROSS JOIN LATERAL aclexplode(coalesce(n.nspacl,acldefault('n',n.nspowner))) a
            WHERE n.nspname IN ('ap_m1','ma_recovery','ma_migrations')
            AND a.grantee=0 AND a.privilege_type='CREATE'""").fetchall()
        if writable_schema:
            raise ValueError('PUBLIC writable application schema')


def verify(database):
    with connect(database, 'admin') as conn:
        result = {'database': DATABASES[database], 'postgresql': conn.execute('SHOW server_version').fetchone()[0],
                  'postgis': conn.execute('SELECT public.postgis_lib_version()').fetchone()[0]}
        for key, query in {
            'schemas': "SELECT count(*) FROM pg_namespace WHERE nspname IN ('ap_m1','ma_migrations','ma_recovery')",
            'tables': "SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname IN ('ap_m1','ma_migrations','ma_recovery') AND c.relkind IN ('r','p')",
            'application_tables': "SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ap_m1' AND c.relkind IN ('r','p')",
            'indexes': "SELECT count(*) FROM pg_indexes WHERE schemaname IN ('ap_m1','ma_migrations','ma_recovery')",
            'policies': "SELECT count(*) FROM pg_policies WHERE schemaname IN ('ap_m1','ma_recovery')",
            'views': "SELECT count(*) FROM pg_views WHERE schemaname='ap_m1'",
            'functions': "SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname IN ('ap_m1','ma_recovery')",
            'migrations': "SELECT count(*) FROM ma_migrations.history WHERE status='APPLIED'",
        }.items():
            result[key] = conn.execute(query).fetchone()[0]
        unprotected = conn.execute("SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname IN ('ap_m1','ma_recovery') AND c.relkind IN ('r','p') AND NOT(c.relrowsecurity AND c.relforcerowsecurity)").fetchall()
        if unprotected:
            raise ValueError('Missing forced RLS: ' + str(unprotected))
        bad = conn.execute("SELECT rolname FROM pg_roles WHERE rolname IN ('madalasa_dev','madalasa_auth','madalasa_billing','ap_m1_api') AND (rolsuper OR rolbypassrls)").fetchall()
        if bad:
            raise ValueError('Privileged runtime role: ' + str(bad))
        result['forced_rls'] = True
        print(json.dumps(result, indent=2))
        private_write(LOCAL / ('verification-' + database + '.json'), json.dumps(result, indent=2)+'\n')
        return result


def test_environment(database='test'):
    cfg = configuration()[database]
    env = os.environ.copy()
    env.update(MA_TEST_DSN=cfg['admin'], MA_RUNTIME_DSN=cfg['runtime'], MA_AUTH_DSN=cfg['auth'], MA_BILLING_DSN=cfg['billing'])
    return env


def seed(database):
    sys.path.insert(0, str(ROOT / 'backend/tests/database'))
    import fixtures
    fixtures.NS=uuid5(NAMESPACE_URL,'madalasa-local-'+database+'-seed-v1')
    with connect(database,'admin',autocommit=False) as conn:
        fixtures.seed_core(conn)
    print('Synthetic fixture inserted in ' + DATABASES[database])


def tests(pattern):
    assert_container()
    command = [sys.executable, '-m', 'unittest', 'discover', '-s', 'backend/tests/database', '-p', pattern, '-v']
    completed = subprocess.run(command, cwd=ROOT, env=test_environment())
    if completed.returncode:
        raise SystemExit(completed.returncode)


def reset(database, allow_dev=False):
    if database == 'dev' and not allow_dev:
        raise ValueError('Development reset requires --allow-dev; test reset is isolated')
    assert_container(database)
    with connect(database, 'admin') as conn:
        # Dedicated database only; never drop cluster roles or any other database.
        conn.execute('DROP SCHEMA IF EXISTS ap_m1 CASCADE')
        conn.execute('DROP SCHEMA IF EXISTS ma_migrations CASCADE')
    print('Reset synthetic schema in ' + DATABASES[database])


def safe_backup_path(path):
    path = Path(path).resolve()
    base = (LOCAL / 'backups').resolve()
    if not path.is_relative_to(base) or path.suffix != '.dump':
        raise ValueError('Backup must be a .dump under ignored .local-db/backups')
    return path


def backup(database):
    assert_container(database)
    folder = LOCAL / 'backups'
    folder.mkdir(exist_ok=True)
    folder.chmod(0o700)
    path = safe_backup_path(folder / (DATABASES[database] + '-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.dump'))
    with open(path, 'wb') as stream:
        subprocess.run(['docker','exec',container_for(database),'pg_dump','-U','postgres','-d',DATABASES[database],'-Fc','--exclude-schema=ma_recovery'], stdout=stream, check=True)
    path.chmod(0o600)
    ledger_path = export_ledger(database)
    meta = {'source_database':DATABASES[database], 'backup_ref':str(uuid4()), 'sha256':sha256(path), 'created_at':datetime.now(timezone.utc).isoformat(), 'erasure_ledger_sha256':sha256(ledger_path)}
    private_write(path.with_suffix('.json'),json.dumps(meta,indent=2)+'\n')
    print(str(path))
    return path


def export_ledger(database):
    path = LOCAL / ('erasure-ledger-' + database + '.json')
    previous = json.loads(path.read_text()) if path.exists() else []
    with connect(database,'admin') as conn:
        rows = []
        for table in ('ap_m1.child_erasure_tombstones','ma_recovery.erasure_ledger'):
            if conn.execute('SELECT to_regclass(%s)',(table,)).fetchone()[0]:
                rows += conn.execute(sql.SQL('SELECT child_id,erased_at,reason_code FROM {}').format(sql.Identifier(*table.split('.')))).fetchall()
    merged = {str(row[0]):[str(row[0]),str(row[1]),row[2]] for row in previous + rows}
    private_write(path,json.dumps(list(merged.values()),indent=2)+'\n')
    return path


def quarantine(database):
    """Close the exact target database, including already-pooled connections."""
    private_write(quarantine_marker(database), json.dumps({'database':DATABASES[database], 'state':'RESTORE_IN_PROGRESS'})+'\n')
    with connect(database,'admin') as conn:
        if conn.execute("SELECT to_regclass('ma_recovery.control')").fetchone()[0]:
            conn.execute('UPDATE ma_recovery.control SET quarantined=true,revision=revision+1,updated_at=now()')
        for kind in ('runtime','auth','billing'):
            role = ROLES[kind][0]
            conn.execute(sql.SQL('REVOKE CONNECT ON DATABASE {} FROM {}').format(sql.Identifier(DATABASES[database]),sql.Identifier(role)))
        conn.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=current_database() AND usename=ANY(%s) AND pid<>pg_backend_pid()",([ROLES[k][0] for k in ('runtime','auth','billing')],))


def open_after_restore(database):
    with connect(database,'admin') as conn:
        if conn.execute("SELECT to_regclass('ma_recovery.control')").fetchone()[0]:
            conn.execute('UPDATE ma_recovery.control SET quarantined=false,revision=revision+1,updated_at=now()')
        for kind in ('runtime','auth','billing'):
            conn.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO {}').format(sql.Identifier(DATABASES[database]),sql.Identifier(ROLES[kind][0])))
    quarantine_marker(database).unlink(missing_ok=True)


def restore(database, path, allow_dev=False, lineage='v2'):
    if database == 'dev' and not allow_dev:
        raise ValueError('Development restore requires --allow-dev')
    path = safe_backup_path(path)
    meta = json.loads(path.with_suffix('.json').read_text())
    if sha256(path) != meta['sha256']:
        raise ValueError('Backup checksum mismatch')
    assert_container(database)
    quarantine(database)
    # Existing destination tombstones MUST survive restore of an older backup.
    # This also prevents test reset from being used as a restoration bypass.
    ledger_path = LOCAL / ('erasure-ledger-' + database + '.json')
    previous = json.loads(ledger_path.read_text()) if ledger_path.exists() else []
    source = next((key for key,value in DATABASES.items() if value==meta.get('source_database')),None)
    if source is None:
        raise ValueError('Backup source is not a named synthetic database')
    source_ledger = LOCAL / ('erasure-ledger-' + source + '.json')
    if source_ledger.exists() and source_ledger != ledger_path:
        previous += json.loads(source_ledger.read_text())
    with connect(database,'admin') as conn:
        exists = conn.execute("SELECT to_regclass('ap_m1.child_erasure_tombstones')").fetchone()[0]
        tombstones = conn.execute('SELECT child_id,erased_at,reason_code FROM ap_m1.child_erasure_tombstones').fetchall() if exists else []
        if conn.execute("SELECT to_regclass('ma_recovery.erasure_ledger')").fetchone()[0]:
            tombstones += conn.execute('SELECT child_id,erased_at,reason_code FROM ma_recovery.erasure_ledger').fetchall()
    merged = {str(row[0]):[str(row[0]),str(row[1]),row[2]] for row in previous + tombstones}
    private_write(ledger_path,json.dumps(list(merged.values()),indent=2)+'\n')
    reset(database, allow_dev)
    with path.open('rb') as stream:
        subprocess.run(['docker','exec','-i',container_for(database),'pg_restore','-U','postgres','-d',DATABASES[database],'--exit-on-error'],stdin=stream,check=True)
    # Upgrade an older backup while the database is still closed to runtime.
    migrate(database,lineage=lineage)
    if lineage == 'm1':
        print('Restored historical M1 checkpoint for inspection; runtime remains quarantined. Restore with --lineage v2 to complete recovery suppression.')
        return
    # Archive preserves owner roles, function ownership, grants and RLS policies.
    # Restoring with --no-owner/--no-acl would silently break the security model.
    with connect(database,'admin') as conn:
        for child,erased,reason in merged.values():
            conn.execute('INSERT INTO ap_m1.child_erasure_tombstones(child_id,erased_at,reason_code) VALUES(%s,%s,%s) ON CONFLICT(child_id) DO NOTHING',(child,erased,reason))
        backup_ref=meta.get('backup_ref') or str(uuid5(NAMESPACE_URL,meta['sha256']))
        conn.execute('INSERT INTO ap_m1.backup_inventory(backup_ref,completed_at) VALUES(%s::uuid,%s::timestamptz) ON CONFLICT(backup_ref) DO NOTHING',(backup_ref,meta['created_at']))
        backup_id=conn.execute('SELECT id FROM ap_m1.backup_inventory WHERE backup_ref=%s::uuid',(backup_ref,)).fetchone()[0]
        restore_id=conn.execute('INSERT INTO ap_m1.restore_runs(backup_id) VALUES(%s) RETURNING id',(backup_id,)).fetchone()[0]
        # The checkpoint is computed from the independent current ledger, not
        # inferred from an empty/stale snapshot's application tombstone set.
        conn.execute('SELECT ap_m1.import_restore_ledger(%s,%s)',(restore_id,bytes.fromhex(sha256(ledger_path))))
        conn.execute('SELECT ap_m1.suppress_restore(%s)',(restore_id,))
        if not conn.execute('SELECT ap_m1.restore_can_open(%s)',(restore_id,)).fetchone()[0]:
            raise ValueError('Restore suppression is not complete; runtime stays closed')
    # Failure anywhere above deliberately leaves CONNECT revoked and the marker
    # present. Never open a partially restored database in a finally block.
    open_after_restore(database)
    print('Restored checksum-verified synthetic backup; destination tombstones preserved')


def legacy_test():
    assert_container()
    with (ROOT / 'backend/tests/m1_tenant_isolation.sql').open('rb') as stream:
        subprocess.run(['docker','exec','-i',container_for('test'),'psql','-X','-U','postgres','-d',DATABASES['test'],'-v','ON_ERROR_STOP=1'],stdin=stream,check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['init','start','start-memory-test','create','migrate','verify','seed','test','reset','backup','restore','export-ledger','legacy-test','stop','psql','exec-test'])
    parser.add_argument('--database', choices=DATABASES, default='test')
    parser.add_argument('--lineage', choices=('m1','v2'), default='v2')
    parser.add_argument('--through')
    parser.add_argument('--pattern',default='test_*.py')
    parser.add_argument('--allow-dev',action='store_true')
    parser.add_argument('--file', type=Path)
    args, extra = parser.parse_known_args()
    if extra and args.command not in ('psql','exec-test'):
        parser.error('Unexpected arguments')
    if args.command=='init': init()
    elif args.command=='start': start()
    elif args.command=='start-memory-test': start_memory_test()
    elif args.command=='create': create()
    elif args.command=='migrate': migrate(args.database,args.through,args.lineage)
    elif args.command=='verify': verify(args.database)
    elif args.command=='seed': seed(args.database)
    elif args.command=='test': tests(args.pattern)
    elif args.command=='reset': reset(args.database,args.allow_dev)
    elif args.command=='backup': backup(args.database)
    elif args.command=='export-ledger': print(export_ledger(args.database))
    elif args.command=='restore':
        if not args.file: parser.error('restore requires --file')
        restore(args.database,args.file,args.allow_dev,args.lineage)
    elif args.command=='legacy-test': legacy_test()
    elif args.command=='stop':
        assert_container(args.database);subprocess.run(['docker','stop',container_for(args.database)],check=True)
    elif args.command=='psql':
        assert_container(args.database);raise SystemExit(subprocess.run(['docker','exec','-i',container_for(args.database),'psql','-X','-U','postgres','-d',DATABASES[args.database],'-v','ON_ERROR_STOP=1']+extra).returncode)
    elif args.command=='exec-test':
        if extra and extra[0]=='--': extra.pop(0)
        if not extra: parser.error('exec-test requires executable after --')
        raise SystemExit(subprocess.run(extra,cwd=ROOT,env=test_environment()).returncode)


if __name__=='__main__':
    try:
        main()
    except psycopg.Error as exc:
        # PostgreSQL errors may contain row values. Keep server SQLSTATE and safe
        # primary message, never conninfo/password/query arguments.
        print('DATABASE_ERROR SQLSTATE='+str(exc.sqlstate)+' '+str(exc.diag.message_primary),file=sys.stderr)
        raise SystemExit(1)
    except (ValueError,subprocess.CalledProcessError,OSError) as exc:
        print(type(exc).__name__+': '+str(exc),file=sys.stderr)
        raise SystemExit(1)
