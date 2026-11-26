#!/usr/bin/env python3
"""Check that the links between this repository's Markdown files resolve.

    python3 project/check_links.py            every tracked .md file
    python3 project/check_links.py FILE ...   only these files

What is checked: every link and picture in a Markdown file that points inside this repository.
The file or folder it names must exist, and when the link ends in `#anchor` and names a Markdown
file (or this file), the anchor must be there: a heading, as GitHub turns it into an anchor, or an
`id` or `name` written in the file's own HTML (`<a id="route-a"></a>`).

What is not checked: addresses with a scheme (`https:`, `mailto:`), since this tool makes no
network request; anything inside a code block or code span; and the wiki's `.mdx` pages, whose
links are routes of the built site, not files.

A link to a page of the website leaves off `.html` (the site's own rule), so a link whose target
is missing is accepted when the same path with `.html` exists.

Exit status: 0 every link resolves; 1 a link is broken; 2 a file could not be read.

Python 3, standard library only.
"""

import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # this checkout
SKIP_PARTS = {"node_modules", ".next", "out", "target", ".private"}

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CODE_SPAN = re.compile(r"(`+)(?:(?!\1).)+?\1")
# [text](target) and ![alt](target); the target is <in angle brackets> or runs to the first space
# or the closing bracket, and one level of brackets inside it is allowed.
INLINE = re.compile(r"!?\[(?:[^\]\[]|\[[^\]]*\])*\]\(\s*(<[^>]*>|(?:[^()\s]|\([^()]*\))*)(?:\s+[\"'(][^)]*)?\)")
REFERENCE = re.compile(r"^ {0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HTML_ID = re.compile(r"<[a-zA-Z][^>]*?\s(?:id|name)\s*=\s*[\"']([^\"']+)[\"']")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def prose_lines(text):
    """The lines of `text` as (number, line), with fenced code blocks left out."""
    fence = None
    for number, line in enumerate(text.replace("\r\n", "\n").split("\n"), start=1):
        mark = FENCE.match(line)
        if fence is None and mark:
            fence = mark.group(1)[0]
            continue
        if fence is not None:
            if mark and mark.group(1)[0] == fence:
                fence = None
            continue
        yield number, line


def without_code_spans(line):
    return CODE_SPAN.sub("", line)


def links(text):
    """Every link target in `text`, as (line number, target), code left out."""
    found = []
    for number, line in prose_lines(text):
        line = without_code_spans(line)
        reference = REFERENCE.match(line)
        if reference:
            found.append((number, reference.group(1).strip("<>")))
            continue
        for match in INLINE.finditer(line):
            found.append((number, match.group(1).strip("<>")))
    return found


def slug(heading):
    """The anchor GitHub gives a heading: its text in lower case, punctuation dropped, spaces as hyphens."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)  # a link keeps its text
    text = re.sub(r"<[^>]+>", "", text)  # HTML tags go
    text = text.replace("`", "").replace("*", "")
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(text):
    """Every anchor a link may name in `text`."""
    found = set()
    seen = {}
    for _, line in prose_lines(text):
        heading = HEADING.match(line)
        if heading:
            base = slug(heading.group(2))
            count = seen.get(base, 0)
            seen[base] = count + 1
            found.add(base if count == 0 else f"{base}-{count}")
        for match in HTML_ID.finditer(without_code_spans(line)):
            found.add(match.group(1))
    return found


def problems(file, root=HERE, read=None):
    """What is wrong with the links of `file` (a path under `root`): a list of (line, message)."""
    read = read or (lambda path: path.read_text(encoding="utf-8"))
    out = []
    cache = {}

    def anchors_of(path):
        if path not in cache:
            cache[path] = anchors(read(path))
        return cache[path]

    for number, target in links(read(file)):
        if not target or SCHEME.match(target) or target.startswith("//"):
            continue
        path_part, _, fragment = target.partition("#")
        path_part = urllib.parse.unquote(path_part.split("?", 1)[0])
        fragment = urllib.parse.unquote(fragment)
        if not path_part:
            dest = file
        elif path_part.startswith("/"):
            dest = root / path_part.lstrip("/")
        else:
            dest = file.parent / path_part
        if not dest.exists():
            page = dest.with_name(dest.name + ".html")
            if path_part and not path_part.endswith("/") and page.is_file():
                continue  # a website page, linked without .html
            out.append((number, f"{target}: no such file or folder"))
            continue
        if fragment and dest.is_file() and dest.suffix.lower() == ".md":
            if fragment not in anchors_of(dest) and fragment.lower() not in anchors_of(dest):
                where = "this file" if dest == file else path_part
                out.append((number, f"{target}: no anchor `{fragment}` in {where}"))
    return out


def tracked_markdown(root=HERE):
    """The tracked .md files under `root`; every .md file when Git cannot say."""
    try:
        listed = subprocess.run(
            ["git", "ls-files", "-z", "--", "*.md"], cwd=root, capture_output=True, check=True, timeout=30
        ).stdout.decode("utf-8")
        files = [root / name for name in listed.split("\0") if name]
    except (OSError, subprocess.SubprocessError):
        files = list(root.rglob("*.md"))
    return sorted(f for f in files if f.is_file() and not SKIP_PARTS & set(f.relative_to(root).parts))


def main(argv):
    if any(arg in ("-h", "--help") for arg in argv):
        print(__doc__)
        return 0
    files = [Path(arg).resolve() for arg in argv] or tracked_markdown()
    broken = 0
    unread = 0
    for file in files:
        try:
            found = problems(file)
        except (OSError, UnicodeDecodeError) as error:
            print(f"UNREAD   {file}: {error}")
            unread += 1
            continue
        try:
            name = file.relative_to(HERE)
        except ValueError:
            name = file
        for number, message in found:
            print(f"BROKEN   {name}:{number}: {message}")
            broken += 1
    if unread:
        return 2
    if broken:
        print(f"{broken} broken link(s) in {len(files)} file(s).")
        return 1
    print(f"Every link in {len(files)} Markdown file(s) resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
