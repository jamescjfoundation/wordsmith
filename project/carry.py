#!/usr/bin/env python3
"""Write and check the blocks of text that Wordsmith repositories carry word for word.

Two kinds of block are handled here (Route N of the project map, project/README.md):

1. The Wordsmith project block. Its source is project/README.md in this repository; every
   repository in PROJECT_COPIES carries a copy.
2. Blocks owned by open-source-core. Their source is a file under the core's template/ folder;
   this repository carries the ones in CORE_BLOCKS. (The apps take theirs with `cargo xtask sync`.)

A block is everything from its BEGIN marker line to its END marker line, both included. A copy is
never edited: change the source, then run this tool.

    python3 project/carry.py            check every copy (the same as --check)
    python3 project/carry.py --write    write every stale copy that can be reached
    python3 project/carry.py --remote   read the other repositories from GitHub

Where the other repositories are read from: the sibling folders beside this checkout
(../wordsmith-script, ../open-source-core and so on) when they exist, and GitHub otherwise. With
--remote, GitHub always: each app's `main`, and the core's newest release tag. A sibling folder is
whatever is checked out there, which can be ahead of or behind `main`, so a check that passes
against sibling folders says nothing about what is published. --remote does.

--write changes files in sibling folders and in this repository only. It never commits: commit and
push each changed repository yourself. A file without the two marker lines is never guessed at.

Exit status: 0 every copy matches; 1 a copy is stale or missing; 2 a source could not be read.

Python 3, standard library only.
"""

import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ORG = "jamescjfoundation"

# 1. The project block: its source in this repository, and who carries a copy.
PROJECT_SOURCE = "project/README.md"
PROJECT_BLOCK = "wordsmith project block"
PROJECT_COPIES = [
    # (repository, file)
    ("wordsmith-script", "AGENTS.md"),
    ("wordsmith-manuscript", "AGENTS.md"),
    ("wordsmith-book", "AGENTS.md"),
]

# 2. Core blocks this repository carries.
CORE = "open-source-core"
CORE_BLOCKS = [
    # (file in the core, block name, file here)
    ("template/AGENTS.md", "public", "AGENTS.md"),
]

HERE = Path(__file__).resolve().parent.parent  # this checkout
TIMEOUT = 20  # seconds, for every network call


class CannotRead(Exception):
    """A source or a copy could not be read at all (offline, no such file, no git)."""

    def __init__(self, message, missing=False):
        super().__init__(message)
        self.missing = missing  # the file is not there, as opposed to out of reach


# ---- blocks ----------------------------------------------------------------------------------


def core_block(name):
    """The marker text of a core block."""
    return f"{CORE}: {name}"


def _span(text, marker):
    """(start, end) of the block `marker` in `text`, marker lines included, or None.

    A marker line is a whole line: `<!-- BEGIN marker -->`. Words may follow the marker inside the
    comment (`<!-- BEGIN marker. Copied by a tool. -->`), but not letters, digits or hyphens that
    would make it another block's name.
    """
    def line(word):
        return re.compile(
            rf"^[ \t]*<!-- {word} {re.escape(marker)}(?![\w-])[^\n]*?-->[ \t]*\r?$", re.MULTILINE
        )

    begin = line("BEGIN").search(text)
    if not begin:
        return None
    end = line("END").search(text, begin.end())
    if not end:
        return None
    stop = end.end()
    if text[stop - 1 : stop] == "\r":  # leave a CRLF line ending whole, outside the block
        stop -= 1
    return begin.start(), stop


def extract(text, marker):
    """The block `marker` from `text` with LF line endings, or None when a marker line is missing."""
    span = _span(text, marker)
    return None if span is None else text[span[0] : span[1]].replace("\r\n", "\n")


def replace(text, marker, block):
    """`text` with its block `marker` replaced by `block`; None when a marker line is missing.

    Everything outside the block is kept as it is, and the block takes the file's line endings.
    """
    span = _span(text, marker)
    if span is None:
        return None
    if "\r\n" in text:
        block = block.replace("\r\n", "\n").replace("\n", "\r\n")
    return text[: span[0]] + block + text[span[1] :]


# ---- reading the other repositories --------------------------------------------------------


def newest_tag(ls_remote_output):
    """The highest `vX.Y.Z` tag in `git ls-remote --tags` output, by number, or None."""
    best = None
    for found in re.finditer(r"refs/tags/(v(\d+)\.(\d+)\.(\d+))(?:\^\{\})?$", ls_remote_output, re.MULTILINE):
        key = tuple(int(n) for n in found.group(2, 3, 4))
        if best is None or key > best[0]:
            best = (key, found.group(1))
    return best[1] if best else None


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "wordsmith-carry"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as answer:
            return answer.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        raise CannotRead(f"{url}: HTTP {error.code}", missing=error.code == 404) from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise CannotRead(f"{url}: {getattr(error, 'reason', error)} (is this machine online?)") from error


def read_file(path):
    try:
        with open(path, encoding="utf-8", newline="") as handle:
            return handle.read()
    except OSError as error:
        raise CannotRead(f"{path}: {error.strerror or error}", missing=isinstance(error, FileNotFoundError)) from error


def write_file(path, text):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


class Repository:
    """One of the other repositories: a sibling folder, or GitHub."""

    def __init__(self, name, remote):
        self.name = name
        folder = HERE.parent / name
        self.folder = folder if not remote and folder.is_dir() else None
        self._ref = None

    def ref(self):
        """What a remote read reads: the core's newest release tag, an app's `main`."""
        if self._ref is None:
            self._ref = self._core_tag() if self.name == CORE else "main"
        return self._ref

    def _core_tag(self):
        url = f"https://github.com/{ORG}/{CORE}"
        try:
            listed = subprocess.run(
                ["git", "ls-remote", "--tags", url], capture_output=True, text=True, timeout=TIMEOUT * 3, check=False
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise CannotRead(f"git ls-remote --tags {url}: {error}") from error
        if listed.returncode != 0:
            raise CannotRead(f"git ls-remote --tags {url}: {listed.stderr.strip() or 'failed'} (is this machine online?)")
        tag = newest_tag(listed.stdout)
        if tag is None:
            raise CannotRead(f"{url} has no vX.Y.Z release tag")
        return tag

    def where(self):
        if self.folder:
            return f"sibling folder ../{self.name}"
        return f"GitHub, {self.ref()}"

    def at(self):
        """Short form for a sentence: `the core at <this>`."""
        return f"../{self.name}" if self.folder else self.ref()

    def read(self, file):
        if self.folder:
            return read_file(self.folder / file)
        return fetch(f"https://raw.githubusercontent.com/{ORG}/{self.name}/{self.ref()}/{file}")

    def write(self, file, text):
        write_file(self.folder / file, text)


# ---- the two jobs --------------------------------------------------------------------------


class Report:
    def __init__(self):
        self.stale = 0
        self.unread = 0
        self.written = 0

    def ok(self, what):
        print(f"  ok       {what}")

    def wrote(self, what):
        self.written += 1
        print(f"  written  {what}")

    def bad(self, what, why):
        self.stale += 1
        print(f"  STALE    {what}: {why}")

    def cannot(self, what, why):
        self.unread += 1
        print(f"  UNREAD   {what}: {why}")


def carry_one(report, write, block, marker, what, read, save, add_markers):
    """Compare one copy with `block`; with `write`, replace it when `save` can."""
    try:
        text = read()
    except CannotRead as error:
        report.cannot(what, str(error))
        return
    have = extract(text, marker)
    if have == block:
        report.ok(what)
    elif have is None:
        report.bad(what, f"the file has no `{marker}` marker lines. {add_markers}")
    elif write and save:
        save(replace(text, marker, block))
        report.wrote(what)
    else:
        report.bad(what, "the copy differs from its source")


def project_block(report, write, remote):
    """The project block, from this repository out to the repositories that carry it."""
    print(f"The project block, from {PROJECT_SOURCE} here:")
    block = extract(read_file(HERE / PROJECT_SOURCE), PROJECT_BLOCK)
    if block is None:
        raise CannotRead(f"{PROJECT_SOURCE} has no `{PROJECT_BLOCK}` marker lines")
    lines = block.split("\n")
    stale_remote = []
    for name, file in PROJECT_COPIES:
        repository = Repository(name, remote)
        try:
            what = f"{name}, {file}, project block ({repository.where()})"
        except CannotRead as error:
            report.cannot(f"{name}, {file}, project block", str(error))
            continue
        before = report.stale
        carry_one(
            report,
            write,
            block,
            PROJECT_BLOCK,
            what,
            lambda r=repository, f=file: r.read(f),
            (lambda text, r=repository, f=file: r.write(f, text)) if repository.folder else None,
            f"Add the lines `{lines[0]}` and `{lines[-1]}` where the block belongs in {name}'s {file}, then run --write.",
        )
        if report.stale > before and not repository.folder:
            stale_remote.append(name)
    if stale_remote:
        print(
            "  To fix a copy read from GitHub: clone the repository beside this one and run\n"
            "  `python3 project/carry.py --write`, then commit and push it there."
        )


def core_blocks(report, write, remote):
    """Core-owned blocks, from the core into this repository."""
    core = Repository(CORE, remote)
    print(f"Core blocks, from {CORE} ({core.where()}):")
    for core_file, name, file in CORE_BLOCKS:
        marker = core_block(name)
        what = f"wordsmith, {file}, {name}"
        try:
            block = extract(core.read(core_file), marker)
        except CannotRead as error:
            if error.missing:
                report.bad(what, f"the core at {core.at()} has no {core_file}, so no `{name}` block yet")
            else:
                report.cannot(what, str(error))
            continue
        if block is None:
            report.bad(what, f"the core at {core.at()} has no `{name}` block yet (in {core_file})")
            continue
        lines = block.split("\n")
        carry_one(
            report,
            write,
            block,
            marker,
            what,
            lambda f=file: read_file(HERE / f),
            lambda text, f=file: write_file(HERE / f, text),
            f"Add the lines `{lines[0]}` and `{lines[-1]}` where the block belongs in {file}, then run --write.",
        )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, usage="carry.py [--check | --write] [--remote]"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="compare every copy with its source (the default)")
    mode.add_argument("--write", action="store_true", help="write every stale copy in a sibling folder or in this repository")
    parser.add_argument("--remote", action="store_true", help="read the other repositories from GitHub, never from sibling folders")
    args = parser.parse_args(argv)
    if args.write and args.remote:
        parser.error("--write changes sibling folders, so it cannot be used with --remote")

    report = Report()
    try:
        project_block(report, args.write, args.remote)
        core_blocks(report, args.write, args.remote)
    except CannotRead as error:
        print(f"carry: {error}", file=sys.stderr)
        return 2

    if report.written:
        print(f"{report.written} file(s) written. Nothing was committed: commit and push each changed repository.")
    if report.unread:
        print(f"{report.unread} could not be read, so nothing is known about them.")
        return 2
    if report.stale:
        fix = "see the lines above" if args.write else "run `python3 project/carry.py --write`, or see the lines above"
        print(f"{report.stale} stale or missing: {fix}.")
        return 1
    print("Every carried block matches its source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
