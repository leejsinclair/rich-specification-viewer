"""T004: the Path guard (FR-018, CH-017)."""

import os
import tempfile
import unittest
from pathlib import Path

import specview


class PathGuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.start = Path(self.tmp.name) / "project"
        (self.start / "specs" / "001-x").mkdir(parents=True)
        (self.start / "specs" / "001-x" / "a.md").write_text("# A\n")
        (self.start / "secret.md").write_text("secret\n")
        self.guard = specview.PathGuard(self.start)

    def tearDown(self):
        self.tmp.cleanup()

    def test_path_inside_specs_is_accepted(self):
        self.assertEqual(self.guard.resolve("001-x/a.md"), (self.start / "specs/001-x/a.md").resolve())

    def test_dot_dot_leaving_specs_is_refused(self):
        self.assertIsNone(self.guard.resolve("../secret.md"))
        self.assertIsNone(self.guard.resolve("001-x/../../secret.md"))

    def test_dot_dot_staying_inside_is_accepted(self):
        self.assertIsNotNone(self.guard.resolve("001-x/../001-x/a.md"))

    def test_absolute_path_outside_is_refused(self):
        self.assertIsNone(self.guard.resolve("/etc/passwd"))
        self.assertIsNone(self.guard.resolve(str(self.start / "secret.md")))

    @unittest.skipUnless(hasattr(os, "symlink"), "needs symbolic links")
    def test_symbolic_link_resolving_outside_is_refused(self):
        link = self.start / "specs" / "001-x" / "escape.md"
        try:
            link.symlink_to(self.start / "secret.md")
        except OSError:
            self.skipTest("cannot create symbolic links here")
        self.assertIsNone(self.guard.resolve("001-x/escape.md"))
        self.assertIsNone(self.guard.read_bytes("001-x/escape.md"))

    def test_read_bytes_reads_inside_only(self):
        self.assertEqual(self.guard.read_bytes("001-x/a.md"), b"# A\n")
        self.assertIsNone(self.guard.read_bytes("../secret.md"))

    def test_has_specs(self):
        self.assertTrue(self.guard.has_specs)
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        self.assertFalse(specview.PathGuard(empty).has_specs)


if __name__ == "__main__":
    unittest.main()
