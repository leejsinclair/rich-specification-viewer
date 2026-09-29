"""T006: container detection and the bind address (DEC-008)."""

import tempfile
import unittest
from pathlib import Path

import specview


class StartupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.missing = Path(self.tmp.name) / "no-dockerenv"
        self.present = Path(self.tmp.name) / ".dockerenv"
        self.present.write_text("")

    def tearDown(self):
        self.tmp.cleanup()

    def test_host_machine_binds_to_loopback(self):
        host, reason = specview.choose_host(None, {}, self.missing)
        self.assertEqual(host, "127.0.0.1")
        self.assertIn("no container", reason)

    def test_dockerenv_binds_to_all_interfaces(self):
        host, reason = specview.choose_host(None, {}, self.present)
        self.assertEqual(host, "0.0.0.0")
        self.assertIn(".dockerenv", reason)

    def test_environment_markers_bind_to_all_interfaces(self):
        for name in ("REMOTE_CONTAINERS", "CODESPACES"):
            with self.subTest(name=name):
                host, reason = specview.choose_host(None, {name: "true"}, self.missing)
                self.assertEqual(host, "0.0.0.0")
                self.assertIn(name, reason)

    def test_host_flag_overrides_detection(self):
        host, reason = specview.choose_host("127.0.0.1", {"CODESPACES": "true"}, self.present)
        self.assertEqual(host, "127.0.0.1")
        self.assertIn("--host", reason)


if __name__ == "__main__":
    unittest.main()
