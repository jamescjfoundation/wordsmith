#!/usr/bin/env python3
"""Tests for privacy.py. Run: python3 project/test_privacy.py

A line here that holds an example of something the check finds ends with the allow marker, so the
check passes on this file.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import privacy  # noqa: E402

NO_REPLY = "1234+someone@users.noreply.github.com"
PRIVATE = "someone@company.co.uk"  # privacy:allow


def found(line, **options):
    return len(privacy.line_problems(line, **options))


class Lines(unittest.TestCase):
    def test_email_addresses(self):
        self.assertEqual(found(f"contact: {PRIVATE}"), 1)
        self.assertEqual(found(f"Signed-off-by: A Writer <{NO_REPLY}>"), 0)
        self.assertEqual(found("Co-Authored-By: Claude <noreply@anthropic.com>"), 0)
        self.assertEqual(found("write to a@example.com or b@example.org"), 0)
        self.assertEqual(found("git@github.com:org/repo.git"), 0)
        self.assertEqual(found('"@types/node@26.6.6" and serde@1.2 and typescript@npm:other'), 0)

    def test_home_folders(self):
        self.assertEqual(found("see /home/alice/project"), 1)  # privacy:allow
        self.assertEqual(found("C:\\Users\\bob\\file"), 1)  # privacy:allow
        self.assertEqual(found("/Users/carol/x"), 1)  # privacy:allow
        self.assertEqual(found("/home/runner/work and /home/<name>/x"), 0)
        self.assertEqual(found("~/project and /usr/home"), 0)

    def test_private_network_addresses(self):
        for address in ("10.0.0.5", "172.16.4.1", "172.31.255.254", "192.168.1.20", "169.254.3.4", "100.64.0.1"):  # privacy:allow
            self.assertEqual(found(f"the box is at {address}."), 1, address)
        for address in ("127.0.0.1", "8.8.8.8", "172.32.0.1", "192.169.1.1", "100.128.0.1", "0.0.0.0"):
            self.assertEqual(found(f"listen on {address}:8000"), 0, address)

    def test_numbers_that_are_not_addresses(self):
        self.assertEqual(found("version v10.0.0.5, build 1.10.0.0.5, section 10.1.2.3.4"), 0)  # privacy:allow
        self.assertEqual(found("10.300.1.1"), 0)
        # An SVG's path data is numbers; a file of that kind is read without the address rule.
        self.assertEqual(found('<path d="M2 10.5.5.5"/>', addresses=False), 0)  # privacy:allow

    def test_private_host_names(self):
        self.assertEqual(found("the preview at https://mysite.test/wiki/ proxies"), 1)  # privacy:allow
        self.assertEqual(found("allowedDevOrigins: ['mysite.test'],"), 1)  # privacy:allow
        self.assertEqual(found("ssh nas.local, then studio.lan, then build.corp.internal."), 3)  # privacy:allow
        self.assertEqual(found("see https://example.test/ and docs.example.test"), 0)

    def test_words_that_are_not_host_names(self):
        self.assertEqual(found("if (/\\.mdx?$/.test(name) || pattern.test(name)) {"), 0)
        self.assertEqual(found("page.test.ts and settings.local.json and .env.local and .env*.local"), 0)
        self.assertEqual(found("run tools/check.test and unittest.test_case"), 0)
        self.assertEqual(found("http://localhost:8000 and wordsmithand.ink"), 0)

    def test_secrets(self):
        token = "gh" + "p_" + "a" * 36
        self.assertEqual(found(f'token = "{token}"'), 1)
        self.assertEqual(found("a token that starts gh" + "p_ is GitHub's"), 0)
        self.assertEqual(found("-----BEGIN " + "PRIVATE KEY-----"), 1)
        self.assertEqual(found("-----BEGIN " + "OPENSSH PRIVATE KEY-----"), 1)
        self.assertEqual(found("AK" + "IA" + "ABCDEFGHIJKLMNOP"), 1)

    def test_the_marker_lets_a_line_keep_a_match(self):
        self.assertEqual(found(f"{PRIVATE}  # {privacy.ALLOW_MARKER}"), 0)


class Identities(unittest.TestCase):
    def test_each_address_that_is_not_no_reply_is_a_problem(self):
        log = f"aaaaaaaaaaaa {NO_REPLY} noreply@github.com\nbbbbbbbbbbbb {PRIVATE} {NO_REPLY}\ncccccccccccc {PRIVATE} {PRIVATE}\n"
        problems = privacy.identity_problems(log)
        self.assertEqual(len(problems), 3)
        self.assertIn("commit bbbbbbbbbb: the author address", problems[0])
        self.assertNotIn(PRIVATE, "".join(problems))  # the address itself is not printed again

    def test_the_first_no_reply_commit_of_an_oldest_first_log(self):
        log = f"aaa {PRIVATE} {PRIVATE}\nbbb {NO_REPLY} {PRIVATE}\nccc {NO_REPLY} noreply@github.com\nddd {NO_REPLY} {NO_REPLY}\n"
        self.assertEqual(privacy.first_no_reply(log), "ccc")
        self.assertIsNone(privacy.first_no_reply(f"aaa {PRIVATE} {PRIVATE}\n"))


class Repository(unittest.TestCase):
    """The two scans, in a small repository made for the test."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        self.git("init", "--quiet", "--initial-branch=main")

    def tearDown(self):
        self.folder.cleanup()

    def git(self, *args, address=NO_REPLY):
        env = dict(
            os.environ,
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_NOSYSTEM="1",
            GIT_AUTHOR_NAME="A Writer",
            GIT_COMMITTER_NAME="A Writer",
            GIT_AUTHOR_EMAIL=address,
            GIT_COMMITTER_EMAIL=address,
        )
        subprocess.run(["git", *args], cwd=self.root, env=env, check=True, capture_output=True)

    def commit(self, name, text, address=NO_REPLY):
        (self.root / name).write_text(text, encoding="utf-8")
        self.git("add", name)
        self.git("commit", "--quiet", "-m", f"Add {name}", address=address)

    def test_commits_are_read_from_the_first_no_reply_commit_on(self):
        self.commit("one.md", "one\n", address=PRIVATE)  # before the rule: not read
        self.commit("two.md", "two\n")
        self.commit("three.md", "three\n")
        self.assertEqual(privacy.scan_identities(self.root), ([], 2))

        self.git("checkout", "--quiet", "-b", "topic")
        self.commit("four.md", "four\n", address=PRIVATE)
        problems, commits = privacy.scan_identities(self.root)
        self.assertEqual((len(problems), commits), (2, 3))  # the author and the committer of one commit
        self.assertEqual(privacy.scan_identities(self.root, head="main"), ([], 2))

    def test_a_repository_with_no_commit_has_nothing_to_read(self):
        self.assertEqual(privacy.scan_identities(self.root), ([], 0))

    def test_tracked_text_files_are_read_and_others_are_not(self):
        self.commit("notes.md", f"fine\nwrite to {PRIVATE}\n")
        self.commit("picture.png", f"\0{PRIVATE}\n")  # a NUL byte: not text
        self.commit("logo.svg", '<path d="M2 10.5.5.5"/>\n<!-- made on studio.lan -->\n')  # privacy:allow
        (self.root / "untracked.md").write_text(f"{PRIVATE}\n", encoding="utf-8")
        problems, files = privacy.scan_tree(self.root)
        self.assertEqual(files, 2)
        self.assertEqual(len(problems), 2)
        self.assertTrue(problems[0].startswith("logo.svg:2: private host name"))
        self.assertTrue(problems[1].startswith("notes.md:2: email address"))


if __name__ == "__main__":
    unittest.main()
