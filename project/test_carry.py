#!/usr/bin/env python3
"""Tests for carry.py. Run: python3 project/test_carry.py"""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import carry  # noqa: E402

BLOCK = "wordsmith project block"
BEGIN = f"<!-- BEGIN {BLOCK} -->"
END = f"<!-- END {BLOCK} -->"


class Blocks(unittest.TestCase):
    def test_extract_takes_the_marker_lines_and_what_is_between(self):
        text = f"# Title\n\n{BEGIN}\n## Map\n\nrow\n{END}\n\nown rules\n"
        self.assertEqual(carry.extract(text, BLOCK), f"{BEGIN}\n## Map\n\nrow\n{END}")

    def test_extract_reads_crlf_files_as_lf(self):
        text = f"top\r\n{BEGIN}\r\nrow\r\n{END}\r\nend\r\n"
        self.assertEqual(carry.extract(text, BLOCK), f"{BEGIN}\nrow\n{END}")

    def test_a_marker_named_in_a_sentence_is_not_a_marker_line(self):
        text = f"The block starts at `{BEGIN}` and is carried.\n\n{BEGIN}\nrow\n{END}\n"
        self.assertEqual(carry.extract(text, BLOCK), f"{BEGIN}\nrow\n{END}")

    def test_words_may_follow_the_name_but_another_name_does_not_match(self):
        marker = carry.core_block("app")
        other = "<!-- BEGIN open-source-core: app-and-core -->\nx\n<!-- END open-source-core: app-and-core -->\n"
        self.assertIsNone(carry.extract(other, marker))
        noted = "<!-- BEGIN open-source-core: app. Copied by a tool. -->\ny\n<!-- END open-source-core: app -->\n"
        self.assertEqual(carry.extract(other + noted, marker), noted.rstrip("\n"))

    def test_missing_markers(self):
        self.assertIsNone(carry.extract("no markers here\n", BLOCK))
        self.assertIsNone(carry.extract(f"{BEGIN}\nnever closed\n", BLOCK))
        self.assertIsNone(carry.extract(f"{END}\n{BEGIN}\n", BLOCK))
        self.assertIsNone(carry.replace("no markers here\n", BLOCK, f"{BEGIN}\n{END}"))

    def test_replace_keeps_everything_outside_the_block(self):
        before, after = "# Title\n\nintro\n\n", "\n\n## Own rules\n\n- one\n"
        text = f"{before}{BEGIN}\nold\n{END}{after}"
        new = f"{BEGIN}\nnew line\nand another\n{END}"
        self.assertEqual(carry.replace(text, BLOCK, new), f"{before}{new}{after}")
        self.assertEqual(carry.extract(carry.replace(text, BLOCK, new), BLOCK), new)

    def test_replace_keeps_a_files_crlf_line_endings(self):
        text = f"top\r\n{BEGIN}\r\nold\r\n{END}\r\nend\r\n"
        self.assertEqual(carry.replace(text, BLOCK, f"{BEGIN}\nnew\n{END}"), f"top\r\n{BEGIN}\r\nnew\r\n{END}\r\nend\r\n")


class Tags(unittest.TestCase):
    def test_the_newest_tag_is_the_highest_by_number(self):
        listed = (
            "aaa\trefs/tags/v0.1.9\n"
            "bbb\trefs/tags/v0.1.16\n"
            "ccc\trefs/tags/v0.1.16^{}\n"
            "ddd\trefs/tags/v0.1.2\n"
            "eee\trefs/tags/book-view-1.1\n"
            "fff\trefs/tags/v0.2.0-rc1\n"
        )
        self.assertEqual(carry.newest_tag(listed), "v0.1.16")
        self.assertEqual(carry.newest_tag(listed + "ggg\trefs/tags/v0.2.0\n"), "v0.2.0")
        self.assertIsNone(carry.newest_tag("eee\trefs/tags/book-view-1.1\n"))


class WholeFiles(unittest.TestCase):
    """A file carried whole from the core, with a stand-in for the core and for this checkout."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.kept = (carry.HERE, carry.Repository, carry.CORE_FILES)
        carry.HERE = Path(self.folder.name)
        carry.CORE_FILES = [("template/CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.md")]
        self.source = "# Code of conduct\n\nBe kind.\n"
        test = self

        class Core:
            def __init__(self, name, remote):
                self.folder = None

            def where(self):
                return "a stand-in"

            def at(self):
                return "v0.0.0"

            def read(self, file):
                if test.source is None:
                    raise carry.CannotRead(f"{file}: no such file", missing=True)
                return test.source

        carry.Repository = Core

    def tearDown(self):
        carry.HERE, carry.Repository, carry.CORE_FILES = self.kept
        self.folder.cleanup()

    def run_it(self, write):
        report = carry.Report()
        with contextlib.redirect_stdout(io.StringIO()):
            carry.core_files(report, write, remote=True)
        return report

    def test_a_missing_or_changed_copy_is_stale_and_write_makes_it_the_source(self):
        copy = carry.HERE / "CODE_OF_CONDUCT.md"
        self.assertEqual(self.run_it(write=False).stale, 1)  # no file yet
        self.assertFalse(copy.exists())
        self.assertEqual(self.run_it(write=True).written, 1)
        self.assertEqual(copy.read_text(encoding="utf-8"), self.source)
        report = self.run_it(write=False)
        self.assertEqual((report.stale, report.written, report.unread), (0, 0, 0))
        copy.write_text(self.source + "\nAn edit made here.\n", encoding="utf-8")
        self.assertEqual(self.run_it(write=False).stale, 1)

    def test_line_endings_alone_are_not_a_difference(self):
        with open(carry.HERE / "CODE_OF_CONDUCT.md", "w", encoding="utf-8", newline="") as handle:
            handle.write(self.source.replace("\n", "\r\n"))
        self.assertEqual(self.run_it(write=False).stale, 0)

    def test_a_core_without_the_file_is_reported_and_nothing_is_written(self):
        self.source = None
        report = self.run_it(write=True)
        self.assertEqual((report.stale, report.written), (1, 0))
        self.assertFalse((carry.HERE / "CODE_OF_CONDUCT.md").exists())


if __name__ == "__main__":
    unittest.main()
