#!/usr/bin/env python3
"""Build the local Drogon backend with installed or checksum-pinned rootless SDK."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import urllib.request
import manage


def prefixes():
    local = manage.LOCAL
    reuse = local / 'backend-prefixes.json'
    if os.environ.get('DB_SDK_PREFIX'):
        return [str(local / 'sysroot/usr'), os.environ['DB_SDK_PREFIX']]
    if reuse.exists():
        values = json.loads(reuse.read_text())
        if all(Path(p).is_dir() for p in values):
            return values
    # The packaged Drogon CMake config also requires SQLite/MariaDB client SDKs;
    # these do NOT install or use additional database servers.
    lock = json.loads((manage.ROOT / 'tools/database/backend-sdk.lock.json').read_text())
    cache = local / 'sdk-downloads'
    cache.mkdir(exist_ok=True)
    destination = local / 'sysroot'
    for item in lock['packages']:
        if not item['url'].startswith('https://archive.ubuntu.com/ubuntu/'):
            raise ValueError('Unexpected SDK mirror')
        path = cache / (item['sha256'] + '.deb')
        if not path.exists():
            with urllib.request.urlopen(item['url'], timeout=60) as response, path.open('wb') as stream:
                shutil.copyfileobj(response, stream)
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            path.unlink()
            raise ValueError('SDK checksum mismatch')
        subprocess.run(['dpkg-deb', '-x', str(path), str(destination)], check=True)
    values = [str(destination / 'usr')]
    manage.private_write(reuse, json.dumps(values) + '\n')
    return values


def environment(values):
    env = os.environ.copy()
    libraries = [str(Path(p)/'lib/x86_64-linux-gnu') for p in values]
    env['LD_LIBRARY_PATH'] = ':'.join(libraries + ([env['LD_LIBRARY_PATH']] if env.get('LD_LIBRARY_PATH') else []))
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--database', choices=manage.DATABASES, default='dev')
    args = parser.parse_args()
    values = prefixes()
    env = environment(values)
    build = manage.LOCAL / 'build'
    subprocess.run(['nice','-n','15','ionice','-c','3','cmake','-S',str(manage.ROOT/'backend'),'-B',str(build),'-DCMAKE_BUILD_TYPE=Debug','-DCMAKE_PREFIX_PATH='+';'.join(values)],env=env,check=True)
    subprocess.run(['nice','-n','15','ionice','-c','3','cmake','--build',str(build),'--parallel','1'],env=env,check=True)
    subprocess.run(['ctest','--test-dir',str(build),'--output-on-failure'],env=env,check=True)
    if args.run:
        from psycopg.conninfo import conninfo_to_dict
        conn = conninfo_to_dict(manage.configuration()[args.database]['runtime'])
        manage.validate_target(conn)
        env.update(DB_HOST=conn['host'],DB_PORT=conn['port'],DB_NAME=conn['dbname'],DB_USER=conn['user'],DB_PASSWORD=conn['password'])
        # exec replaces the launcher; credentials are environment, never argv.
        os.execve(str(build/'madalasa_backend'),['madalasa_backend'],env)


if __name__ == '__main__':
    main()
