#!/usr/bin/env python3
"""Tests for check_links.py. Run: python3 project/test_check_links.py"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_links  # noqa: E402


class Links(unittest.TestCase):
    def test_finds_links_pictures_and_reference_definitions(self):
        text = "See [the map](project/README.md#routes) and ![logo](brand/logo.svg \"The logo\").\n\n[ref]: <docs/a b.md>\n"
        self.assertEqual(
            check_links.links(text),
            [(1, "project/README.md#routes"), (1, "brand/logo.svg"), (3, "docs/a b.md")],
        )

    def test_code_blocks_and_code_spans_are_left_out(self):
        text = "```\n[not a link](missing.md)\n```\n\nWrite `[text](missing.md)` so.\n\n~~~sh\n[x](y)\n~~~\n[real](here.md)\n"
        self.assertEqual(check_links.links(text), [(10, "here.md")])

    def test_a_target_may_hold_brackets(self):
        self.assertEqual(check_links.links("[page](app/(docs)/page.tsx)\n"), [(1, "app/(docs)/page.tsx")])


class Anchors(unittest.TestCase):
    def test_headings_become_anchors_as_on_github(self):
        text = "# The Wordsmith project map\n\n## Where to look, where to write\n\n### Route A: a core change an app needs\n\n## website/wiki/\n\n## `project/` and **more**\n"
        self.assertEqual(
            check_links.anchors(text),
            {
                "the-wordsmith-project-map",
                "where-to-look-where-to-write",
                "route-a-a-core-change-an-app-needs",
                "websitewiki",
                "project-and-more",
            },
        )

    def test_a_repeated_heading_gets_a_number(self):
        self.assertEqual(check_links.anchors("## Today\n\n## Today\n\n## Today\n"), {"today", "today-1", "today-2"})

    def test_html_ids_count_and_headings_in_code_do_not(self):
        text = '<a id="route-a"></a>\n### Route A\n\n```\n## Not a heading\n```\n\nThe tag `<a id="quoted">` is only named.\n'
        self.assertEqual(check_links.anchors(text), {"route-a"})


class Problems(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "project").mkdir()
        (self.root / "website").mkdir()
        (self.root / "website" / "about.html").write_text("<html></html>", encoding="utf-8")
        (self.root / "project" / "README.md").write_text('# Map\n\n<a id="route-a"></a>\n### Route A\n', encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, text):
        file = self.root / "AGENTS.md"
        file.write_text(text, encoding="utf-8")
        return check_links.problems(file, root=self.root)

    def test_links_that_resolve_are_quiet(self):
        text = (
            "# Notes\n\n## Git\n\n[map](project/README.md) [route](project/README.md#route-a) [folder](project/)\n"
            "[here](#git) [heading](project/README.md#map) [site](https://example.org/missing) [mail](mailto:a@example.org)\n"
            "[root](/project/README.md) [page](website/about)\n"
        )
        self.assertEqual(self.check(text), [])

    def test_a_missing_file_and_a_missing_anchor_are_reported_with_their_line(self):
        found = self.check("# Notes\n\n[gone](project/GONE.md)\n\n[route](project/README.md#route-z)\n[here](#nowhere)\n")
        self.assertEqual([line for line, _ in found], [3, 5, 6])
        self.assertIn("no such file or folder", found[0][1])
        self.assertIn("no anchor `route-z` in project/README.md", found[1][1])
        self.assertIn("no anchor `nowhere` in this file", found[2][1])

    def test_a_page_link_needs_the_html_file(self):
        self.assertEqual(len(self.check("[page](website/missing)\n")), 1)


if __name__ == "__main__":
    unittest.main()
