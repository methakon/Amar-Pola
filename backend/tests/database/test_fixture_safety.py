"""Direct unittest invocation must be as isolated as the lifecycle wrapper."""
import os
import unittest
from unittest.mock import patch
import fixtures


class FixtureTargetSafetyTests(unittest.TestCase):
    def test_direct_fixture_connections_reject_non_test_targets_before_connect(self):
        for dsn in (
            'host=remote.invalid port=15432 dbname=madalasa_alarka_test',
            'host=127.0.0.1 port=5432 dbname=madalasa_alarka_test',
            'host=127.0.0.1 port=15432 dbname=madalasa_alarka_dev',
            'host=127.0.0.1 hostaddr=192.0.2.1 port=15432 dbname=madalasa_alarka_test',
        ):
            with self.subTest(dsn=dsn), patch.dict(os.environ, {'MA_TEST_DSN':dsn}):
                with self.assertRaises(ValueError):fixtures._dsn('admin')
