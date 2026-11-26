#!/usr/bin/env python3
"""Each app's latest public release, for the website and the wiki.

The pages show a version, a date and download links. They come from each app's releases on
GitHub, never from a number typed into a page. This tool reads them and keeps the answer in one
file, which build.py and the wiki read:

    python3 website/tools/releases.py              read GitHub and print what each app has published
    python3 website/tools/releases.py --write      the same, and write it to website/data/releases.json
    python3 website/tools/releases.py --out FILE   write it to FILE instead (the deploy does this)
    python3 website/tools/releases.py --out FILE --changed-from URL
                                                   also say whether it differs from the file at URL
                                                   (the scheduled deploy: is the live site behind?)

What is asked: GET https://api.github.com/repos/<owner>/<repo>/releases for each app in
website/data/apps/. That is public data and needs no token. Requests without one share a small
hourly allowance with everything else at the same address, so when GITHUB_TOKEN is set (GitHub
gives every workflow run one; nobody has to create it) the tool sends it.

When an app cannot be read (no network, the allowance used up), the tool keeps the last known
answer for that app and says so: first from --last-known URL (the file the live site was built
from), then from website/data/releases.json. A page is never built from a guess.

Standard library only. build.py imports this file for the helpers at the top and never touches
the network: without --releases it reads website/data/releases.json.
"""
import argparse, datetime, json, os, pathlib, re, sys, urllib.error, urllib.request

WEBSITE = pathlib.Path(__file__).resolve().parent.parent
DATA = WEBSITE / "data"
KEPT = DATA / "releases.json"
NOTE = ("The last known public release of each app. Written by website/tools/releases.py --write; "
        "never edit it. The published site reads GitHub again at every deploy.")


# ---------------------------------------------------------------- what build.py and the tests use

def read_apps(folder=DATA / "apps"):
    """The apps, from website/data/apps/<slug>.json, in their order."""
    apps = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(folder.glob("*.json"))]
    return sorted(apps, key=lambda app: app["order"])


def read_platforms(file=DATA / "platforms.json"):
    return json.loads(file.read_text(encoding="utf-8"))


def read_kept(file=KEPT):
    """The releases file: {"apps": {slug: release or None}}. A missing file means no release is known."""
    if not pathlib.Path(file).exists():
        return {"apps": {}}
    return json.loads(pathlib.Path(file).read_text(encoding="utf-8"))


def version_key(version):
    """Orders versions: 1.0.0 after 0.9.0 and after 1.0.0-rc.1; text that is no version sorts first."""
    found = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+.*)?", version.strip())
    if not found:
        return (-1, 0, 0, 0, ())
    pre = tuple((0, int(part), "") if part.isdigit() else (1, 0, part) for part in found.group(4).split(".")) if found.group(4) else ()
    return (int(found.group(1)), int(found.group(2)), int(found.group(3)), 0 if pre else 1, pre)


def state_of(release):
    """Where an app stands: "none" (nothing published), "preview" (before 1.0.0, or marked a
    pre-release on GitHub) or "released"."""
    if not release:
        return "none"
    if release.get("prerelease") or version_key(release["version"])[0] < 1:
        return "preview"
    return "released"


def long_date(day):
    """2026-12-01 → 1 December 2026"""
    date = datetime.date.fromisoformat(day)
    return f"{date.day} {date.strftime('%B')} {date.year}"


def size_words(size):
    """Bytes as a reader says them: 48 MB, 1.2 GB, 310 KB."""
    half_up = lambda number: int(number + 0.5)  # the wiki's lib/releases.mjs rounds the same way
    if size >= 1024 ** 3:
        return f"{half_up(size * 10 / 1024 ** 3) / 10:.1f} GB"
    if size >= 1024 ** 2:
        return f"{half_up(size / 1024 ** 2)} MB"
    return f"{max(1, half_up(size / 1024))} KB"


def state_words(app, release):
    """The words an app's data file has for its state, with the release's version and date filled in."""
    words = app["state"][state_of(release)]
    fill = {"version": release["version"], "date": long_date(release["date"])} if release else {}
    return {key: text.format(**fill) for key, text in words.items()}


# Files that are about a download, not a download: checksum lists, signatures, update manifests.
BESIDE = re.compile(r"(sha256|sha512|checksums?|\.sig$|\.asc$|\.minisig$|\.sbom|\.json$|\.txt$|\.yml$|\.yaml$)", re.I)


def files_for(release, platform):
    """The release's files for one platform, by the platform's file-name pattern."""
    if not release:
        return []
    pattern = re.compile(platform["files"], re.I)
    return [file for file in release["files"] if pattern.search(file["name"]) and not BESIDE.search(file["name"])]


def has_checksums(release):
    """Whether the release carries a list of checksums, or GitHub gave a checksum for its files."""
    return any(re.search(r"sha256|sha512|checksum", file["name"], re.I) or "sha256" in file for file in release["files"])


# ---------------------------------------------------------------- reading GitHub

def normalize(listing):
    """GitHub's list of releases → the one the pages show, or None when nothing is published.

    The newest full release wins; a pre-release is shown only while no full release exists.
    Drafts are never shown.
    """
    public = [one for one in listing if not one.get("draft") and one.get("published_at")]
    if not public:
        return None
    full = [one for one in public if not one.get("prerelease")]
    newest = max(full or public, key=lambda one: (version_key(one["tag_name"]), one["published_at"]))
    files = []
    for asset in newest.get("assets", []):
        if asset.get("state", "uploaded") != "uploaded":
            continue
        file = {"name": asset["name"], "url": asset["browser_download_url"], "size": asset["size"]}
        digest = asset.get("digest") or ""
        if digest.startswith("sha256:"):
            file["sha256"] = digest.removeprefix("sha256:")
        files.append(file)
    return {
        "version": newest["tag_name"].removeprefix("v"),
        "tag": newest["tag_name"],
        "date": newest["published_at"][:10],
        "url": newest["html_url"],
        "prerelease": bool(newest.get("prerelease")),
        "files": sorted(files, key=lambda file: file["name"]),
    }


def get_json(url, token=None, timeout=20):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "wordsmith-website-build", "X-GitHub-Api-Version": "2022-11-28"}
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as answer:
        return json.loads(answer.read().decode("utf-8"))


def gather(apps, kept, last_known=None, get=None, token=None, say=print):
    """Each app's release, read from GitHub; where that fails, the last known one.

    Returns ({slug: release or None}, [slugs that could not be read]).
    """
    get = get or get_json
    found, failed = {}, []
    for app in apps:
        slug = app["slug"]
        try:
            found[slug] = normalize(get(f"https://api.github.com/repos/{app['repository']}/releases?per_page=30", token))
        except (urllib.error.URLError, OSError, ValueError, KeyError) as error:
            failed.append(slug)
            if last_known is not None and slug in last_known.get("apps", {}):
                found[slug], source = last_known["apps"][slug], "the file the live site was built from"
            else:
                found[slug], source = kept.get("apps", {}).get(slug), "website/data/releases.json"
            say(f"{app['name']}: GitHub could not be read ({error}). Kept the last known answer, from {source}.")
    return found, failed


def describe(app, release):
    if not release:
        return f"{app['name']}: no public release."
    kind = " (marked a pre-release)" if release["prerelease"] else ""
    return f"{app['name']}: {release['version']}{kind}, published {release['date']}, {len(release['files'])} file(s)."


def as_text(found):
    return json.dumps({"note": NOTE, "apps": found}, indent=2, ensure_ascii=False) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read each app's latest public release from GitHub.")
    parser.add_argument("--write", action="store_true", help="write website/data/releases.json")
    parser.add_argument("--out", help="write the answer to this file")
    parser.add_argument("--last-known", help="the address of the releases file the live site was built from, to fall back on")
    parser.add_argument("--changed-from", help="compare with the releases file at this address; with GITHUB_OUTPUT set, write changed=true or false")
    args = parser.parse_args(argv)

    apps = read_apps()
    kept = read_kept()
    live = None
    for address in dict.fromkeys(filter(None, [args.last_known, args.changed_from])):
        try:
            live = get_json(address)
        except (urllib.error.URLError, OSError, ValueError) as error:
            print(f"The live site's releases file could not be read ({error}).")
    found, failed = gather(apps, kept, live, token=os.environ.get("GITHUB_TOKEN") or None)
    for app in apps:
        print(describe(app, found[app["slug"]]))
    if failed and os.environ.get("GITHUB_ACTIONS"):
        print(f"::warning::The latest release could not be read from GitHub for: {', '.join(failed)}. The pages keep the last known release.")

    text = as_text(found)
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
    if args.write:
        if failed:
            sys.exit(f"Not written: {', '.join(failed)} could not be read, and website/data/releases.json holds only what GitHub answered.")
        changed = text != (KEPT.read_text(encoding="utf-8") if KEPT.exists() else "")
        KEPT.write_text(text, encoding="utf-8")
        print("Wrote website/data/releases.json. Run `python3 website/tools/build.py` and commit the pages with it."
              if changed else "website/data/releases.json already says this.")
    if args.changed_from:
        changed = live is None or live.get("apps") != found
        print("The live site is behind: it was built from other release data." if changed
              else "The live site was built from the same release data.")
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
                out.write(f"changed={'true' if changed else 'false'}\n")


if __name__ == "__main__":
    main()
