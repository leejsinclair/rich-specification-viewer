"""T005: the Host check (CH-016)."""

import unittest

import specview


class HostCheckTest(unittest.TestCase):
    def test_local_names_at_any_port_are_allowed(self):
        for header in ("localhost", "localhost:8000", "LOCALHOST:8123", "127.0.0.1", "127.0.0.1:8019"):
            with self.subTest(header=header):
                self.assertTrue(specview.host_allowed(header))

    def test_foreign_or_missing_hosts_are_refused(self):
        for header in (None, "", "evil.example", "evil.example:8000", "localhost.evil.example", "[::1]:8000", "0.0.0.0:8000"):
            with self.subTest(header=header):
                self.assertFalse(specview.host_allowed(header))


if __name__ == "__main__":
    unittest.main()
