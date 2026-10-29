"""Safety and migration-runner tests; do not require a running database."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('database_manage', Path(__file__).parents[3] / 'tools/database/manage.py')
manage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manage)


class RunnerSafety(unittest.TestCase):
    def test_only_named_loopback_databases_allowed(self):
        for host in ['db.example.com', '192.0.2.1', '/var/run/postgresql']:
            with self.assertRaises(ValueError):
                manage.validate_target({'host': host, 'port': 15432, 'dbname': 'madalasa_alarka_test'})
        for db in ['postgres', 'production', 'madalasa_alarka_dev; DROP DATABASE postgres']:
            with self.assertRaises(ValueError):
                manage.validate_target({'host': '127.0.0.1', 'port': 15432, 'dbname': db})
        manage.validate_target({'host': '127.0.0.1', 'port': 15432, 'dbname': 'madalasa_alarka_test'})

    def test_historical_transaction_removed_not_function_body(self):
        sql = '-- historical\nBEGIN;\nDO $x$\nBEGIN\nNULL;\nEND $x$;\nCOMMIT;\n-- note\n'
        result = manage.transaction_body(sql)
        self.assertNotIn('\nCOMMIT;', result)
        self.assertNotIn('\nBEGIN;', result)
        self.assertIn('\nBEGIN\nNULL;', result)

    def test_unsafe_restore_path_rejected(self):
        with self.assertRaises(ValueError):
            manage.safe_backup_path(Path('/etc/passwd'))

    def test_original_migration_hash_is_pinned(self):
        self.assertEqual(manage.BASELINE_SHA256, manage.sha256(manage.MIGRATIONS / '0001_m1_identity.sql'))


if __name__ == '__main__':
    unittest.main()
