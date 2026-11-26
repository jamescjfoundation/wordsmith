#!/usr/bin/env python3
"""Tests for releases.py: `python3 -m unittest discover -s website/tools`. No network is used."""
import io, json, pathlib, sys, tempfile, unittest, urllib.error
from contextlib import redirect_stdout

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import releases


def release(tag, published="2026-12-01T10:00:00Z", prerelease=False, draft=False, assets=()):
    return {"tag_name": tag, "published_at": published, "prerelease": prerelease, "draft": draft,
            "html_url": f"https://github.com/example/app/releases/tag/{tag}",
            "assets": [{"name": name, "browser_download_url": f"https://github.com/example/app/releases/download/{tag}/{name}",
                        "size": size, "state": "uploaded", "digest": digest} for name, size, digest in assets]}


FILES = (("app-0.9.0-macos-aarch64.dmg", 50 * 1024 ** 2, "sha256:" + "a" * 64),
         ("app-0.9.0-windows-x64-portable.zip", 61 * 1024 ** 2, None),
         ("app-0.9.0-linux-x86_64.tar.gz", 48 * 1024 ** 2, None),
         ("SHA256SUMS.txt", 300, None))
APP = {"slug": "app", "order": 1, "name": "The App", "repository": "example/app",
       "state": {"none": {"chip": "", "line": "Free"}, "preview": {"chip": "Preview {version}", "line": "Preview, {date}"},
                 "released": {"chip": "Version {version}", "line": "Released {date}"}}}


class Versions(unittest.TestCase):
    def test_order(self):
        order = ["nonsense", "0.9.0", "1.0.0-rc.1", "1.0.0-rc.2", "1.0.0", "v1.0.1", "1.10.0"]
        self.assertEqual(sorted(reversed(order), key=releases.version_key), order)

    def test_state(self):
        self.assertEqual(releases.state_of(None), "none")
        self.assertEqual(releases.state_of({"version": "0.9.0", "prerelease": False}), "preview")
        self.assertEqual(releases.state_of({"version": "1.0.0", "prerelease": False}), "released")
        self.assertEqual(releases.state_of({"version": "1.1.0-beta.1", "prerelease": True}), "preview")


class Normalize(unittest.TestCase):
    def test_nothing_published(self):
        self.assertIsNone(releases.normalize([]))
        self.assertIsNone(releases.normalize([release("v1.0.0", draft=True), release("v0.9.0", published=None)]))

    def test_the_newest_full_release_wins(self):
        found = releases.normalize([release("v0.9.0"), release("v1.0.0", "2026-12-20T08:00:00Z"), release("v1.1.0-beta.1", "2026-12-25T08:00:00Z", prerelease=True)])
        self.assertEqual((found["version"], found["tag"], found["date"], found["prerelease"]), ("1.0.0", "v1.0.0", "2026-12-20", False))

    def test_a_pre_release_shows_only_while_nothing_else_exists(self):
        found = releases.normalize([release("v0.9.0-rc.1", prerelease=True)])
        self.assertEqual((found["version"], found["prerelease"]), ("0.9.0-rc.1", True))
        self.assertEqual(releases.state_of(found), "preview")

    def test_files(self):
        found = releases.normalize([release("v0.9.0", assets=FILES)])
        self.assertEqual([file["name"] for file in found["files"]], sorted(name for name, _, _ in FILES))
        mac = next(file for file in found["files"] if "macos" in file["name"])
        self.assertEqual(mac["sha256"], "a" * 64)
        self.assertEqual(mac["url"], "https://github.com/example/app/releases/download/v0.9.0/app-0.9.0-macos-aarch64.dmg")
        self.assertNotIn("sha256", next(file for file in found["files"] if "linux" in file["name"]))


class Platforms(unittest.TestCase):
    def test_every_platform_finds_its_file_and_no_other(self):
        found = releases.normalize([release("v0.9.0", assets=FILES + (("app-0.9.0-macos-aarch64.dmg.sha256", 90, None),))])
        names = {platform["id"]: [file["name"] for file in releases.files_for(found, platform)] for platform in releases.read_platforms()}
        self.assertEqual(names, {"macos-arm64": ["app-0.9.0-macos-aarch64.dmg"],
                                 "windows-x64": ["app-0.9.0-windows-x64-portable.zip"],
                                 "linux-x64": ["app-0.9.0-linux-x86_64.tar.gz"]})

    def test_other_spellings(self):
        platforms = {platform["id"]: platform for platform in releases.read_platforms()}
        one = lambda name: {"files": [{"name": name, "url": "u", "size": 1}]}
        self.assertTrue(releases.files_for(one("wordsmith-book-1.0.0-macos-arm64.dmg"), platforms["macos-arm64"]))
        self.assertTrue(releases.files_for(one("wordsmith-manuscript-1.0.0-windows-x86_64.zip"), platforms["windows-x64"]))
        self.assertFalse(releases.files_for(one("wordsmith-script-1.0.0-macos-x86_64.dmg"), platforms["macos-arm64"]))
        self.assertFalse(releases.files_for(one("wordsmith-script-1.0.0-linux-aarch64.tar.gz"), platforms["linux-x64"]))
        self.assertEqual(releases.files_for(None, platforms["linux-x64"]), [])


    def test_checksums(self):
        self.assertTrue(releases.has_checksums(releases.normalize([release("v0.9.0", assets=FILES)])))
        self.assertTrue(releases.has_checksums({"files": [{"name": "a.zip", "url": "u", "size": 1, "sha256": "b" * 64}]}))
        self.assertFalse(releases.has_checksums({"files": [{"name": "a.zip", "url": "u", "size": 1}]}))


class Words(unittest.TestCase):
    def test_dates_and_sizes(self):
        self.assertEqual(releases.long_date("2026-12-01"), "1 December 2026")
        self.assertEqual(releases.size_words(50 * 1024 ** 2), "50 MB")
        self.assertEqual(releases.size_words(300), "1 KB")
        self.assertEqual(releases.size_words(int(1.25 * 1024 ** 3)), "1.3 GB")
        self.assertEqual(releases.size_words(int(2.5 * 1024 ** 2)), "3 MB")

    def test_state_words(self):
        self.assertEqual(releases.state_words(APP, None), {"chip": "", "line": "Free"})
        found = releases.normalize([release("v0.9.0")])
        self.assertEqual(releases.state_words(APP, found), {"chip": "Preview 0.9.0", "line": "Preview, 1 December 2026"})
        found = releases.normalize([release("v1.0.0")])
        self.assertEqual(releases.state_words(APP, found), {"chip": "Version 1.0.0", "line": "Released 1 December 2026"})


class Gather(unittest.TestCase):
    def test_reads_github(self):
        asked = []

        def get(url, token=None):
            asked.append((url, token))
            return [release("v1.0.0")]

        found, failed = releases.gather([APP], {"apps": {}}, get=get, token="t", say=lambda text: None)
        self.assertEqual(asked, [("https://api.github.com/repos/example/app/releases?per_page=30", "t")])
        self.assertEqual((found["app"]["version"], failed), ("1.0.0", []))

    def test_falls_back_to_the_last_known_answer_and_says_so(self):
        def get(url, token=None):
            raise urllib.error.URLError("rate limit")

        said = []
        kept = {"apps": {"app": {"version": "0.9.0"}}}
        found, failed = releases.gather([APP], kept, get=get, say=said.append)
        self.assertEqual((found, failed), ({"app": {"version": "0.9.0"}}, ["app"]))
        self.assertIn("website/data/releases.json", said[0])
        # the file the live site was built from is newer than the file in the repository: it wins
        found, _ = releases.gather([APP], kept, {"apps": {"app": {"version": "1.0.0"}}}, get=get, say=said.append)
        self.assertEqual(found, {"app": {"version": "1.0.0"}})
        self.assertIn("live site", said[1])
        # nothing known anywhere: no release, never a guess
        found, _ = releases.gather([APP], {"apps": {}}, get=get, say=said.append)
        self.assertEqual(found, {"app": None})


class Command(unittest.TestCase):
    def test_out_and_changed_from(self):
        with tempfile.TemporaryDirectory() as folder:
            out, github_output = pathlib.Path(folder, "fresh.json"), pathlib.Path(folder, "output")
            real_get, real_apps, environ = releases.get_json, releases.read_apps, dict(releases.os.environ)
            live = {"apps": {"app": None}}
            releases.read_apps = lambda: [APP]
            releases.get_json = lambda url, token=None, timeout=20: live if url == "https://example.org/releases.json" else [release("v0.9.0")]
            releases.os.environ["GITHUB_OUTPUT"] = str(github_output)
            releases.os.environ.pop("GITHUB_ACTIONS", None)
            try:
                with redirect_stdout(io.StringIO()) as said:
                    releases.main(["--out", str(out), "--changed-from", "https://example.org/releases.json"])
                self.assertEqual(json.loads(out.read_text())["apps"]["app"]["version"], "0.9.0")
                self.assertEqual(github_output.read_text(), "changed=true\n")
                self.assertIn("The App: 0.9.0", said.getvalue())
                live = json.loads(out.read_text())
                with redirect_stdout(io.StringIO()):
                    releases.main(["--out", str(out), "--changed-from", "https://example.org/releases.json"])
                self.assertEqual(github_output.read_text(), "changed=true\nchanged=false\n")
            finally:
                releases.get_json, releases.read_apps = real_get, real_apps
                releases.os.environ.clear()
                releases.os.environ.update(environ)


class ThisRepository(unittest.TestCase):
    def test_the_data_files_agree(self):
        platforms = {platform["id"] for platform in releases.read_platforms()}
        kept = releases.read_kept()
        apps = releases.read_apps()
        self.assertEqual([app["slug"] for app in apps], ["script", "manuscript", "book"])
        for app in apps:
            self.assertEqual(set(app["state"]), {"none", "preview", "released"}, app["slug"])
            self.assertTrue(set(app["platforms"]) <= platforms, app["slug"])
            self.assertIn(app["slug"], kept["apps"])
            releases.state_words(app, kept["apps"][app["slug"]])  # every placeholder is one the tool fills


if __name__ == "__main__":
    unittest.main()
