#!/usr/bin/env python3
"""Check that this public repository holds nothing personal and no secret.

    python3 project/privacy.py              every tracked text file, and the commits
    python3 project/privacy.py --head REV   read the commits that lead to REV, not to HEAD

It is this repository's form of `cargo xtask privacy`, which the Rust repositories have from
open-source-core (template/xtask/src/privacy.rs there). The rules are the same where both have
them; two are added here, private network addresses and private host names.

In every tracked text file, a line fails when it holds:

- an email address that is not a no-reply, example or published project address;
- a home folder (`/home/<name>`, `/Users/<name>`, `C:\\Users\\<name>`);
- a private network address (10.x.x.x, 172.16 to 172.31, 192.168.x.x, 169.254.x.x, 100.64 to
  100.127), or a host name that only one network knows (`.test`, `.local`, `.lan`, `.internal`,
  `.localdomain`, `.home.arpa`);
- something shaped like a key or a token.

In the history, a commit fails when its author or committer address is not a no-reply one. The
commits read are those that lead to HEAD, from the default branch's first no-reply commit on:
what came before that commit is not read.

A line that must keep a match on purpose carries the marker named in ALLOW_MARKER. Files with a
NUL byte (pictures, PDFs, fonts) and files over 4 MB are not read. A pattern cannot find a
person's name, a quoted conversation or an open security problem: read your own diff for those.

Exit status: 0 nothing found; 1 something found; 2 Git could not be read.

Python 3, standard library only.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # this checkout

MAX_SCAN_BYTES = 4 * 1024 * 1024
ALLOW_MARKER = "privacy" + ":allow"

# Addresses that are fine to publish, matched at the end of the address. A project address goes
# here once it is published on the website.
ALLOWED_EMAIL_SUFFIXES = (
    "@users.noreply.github.com",
    "@noreply.github.com",
    "noreply@github.com",
    "noreply@anthropic.com",
    "@example.com",
    "@example.org",
    "@example.net",
    "@example.invalid",
)

# Home folders that are not a person's: CI runners and placeholders in documentation.
ALLOWED_HOMES = {"runner", "user", "you", "me", "example", "USER", "username"}

# Host names reserved for examples.
ALLOWED_HOSTS = ("example.test", "example.local")

# Starts of well-known secret formats, written split so this file does not match itself.
SECRET_PREFIXES = (
    "gh" + "p_",
    "gh" + "o_",
    "gh" + "s_",
    "gh" + "u_",
    "github" + "_pat_",
    "sk" + "-ant-",
    "sk" + "_live_",
    "xo" + "xb-",
    "xo" + "xp-",
)
PRIVATE_KEY = re.compile("-----BEGIN " + r"(?:[A-Z]+ )?PRIVATE KEY")
CLOUD_KEY = re.compile("AK" + r"IA[A-Z0-9]{16}")

EMAIL = re.compile(r"([A-Za-z0-9._%+-]+)@([A-Za-z0-9._%+-]+)")
HOME = re.compile(r"(/home/|/Users/|\\Users\\)([A-Za-z0-9_.<>-]*)")
ADDRESS = re.compile(r"(?<![\w.])(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?![\w]|\.\d)")
# One or more labels, then an ending only a private network resolves. Not a method call
# (`pattern.test(x)`), not a file name with a further ending (`page.test.ts`).
HOST = re.compile(
    r"(?<![\w.-])((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:test|local|lan|internal|localdomain|home\.arpa))"
    r"(?![\w(-]|\.[a-z0-9])"
)


def emails_in(line):
    out = []
    for local, domain in EMAIL.findall(line):
        domain = domain.rstrip(".")
        ending = domain.rpartition(".")[2]
        # `name@1.2.3` is a version, `git@host:path` a remote: neither is an email address.
        if "." not in domain or len(ending) < 2 or not ending.isalpha() or local == "git":
            continue
        out.append(f"{local}@{domain}")
    return out


def home_paths_in(line):
    out = []
    for prefix, name in HOME.findall(line):
        if name and not name.startswith("<") and name not in ALLOWED_HOMES:
            out.append(prefix + name)
    return out


def private_addresses_in(line):
    out = []
    for found in ADDRESS.finditer(line):
        a, b, c, d = (int(n) for n in found.groups())
        if max(a, b, c, d) > 255:
            continue
        if a == 10 or (a == 172 and 16 <= b <= 31) or (a, b) in ((192, 168), (169, 254)) or (a == 100 and 64 <= b <= 127):
            out.append(found.group(0))
    return out


def private_hosts_in(line):
    out = []
    for found in HOST.finditer(line):
        name = found.group(1)
        before = line[max(0, found.start() - 2) : found.start()]
        if before.endswith("/") and before != "//":
            continue  # the last part of a path (`tools/run.test`), not a host
        if any(name == ok or name.endswith("." + ok) for ok in ALLOWED_HOSTS):
            continue
        out.append(name)
    return out


def secrets_in(line):
    out = []
    for prefix in SECRET_PREFIXES:
        at = line.find(prefix)
        if at < 0:
            continue
        # A prefix with a long token after it; the prefix named in a sentence is fine.
        tail = re.match(r"[A-Za-z0-9_-]*", line[at + len(prefix) :]).group(0)
        if len(tail) >= 16:
            out.append(f"something that looks like a secret (`{prefix}...`)")
    if PRIVATE_KEY.search(line):
        out.append("something that looks like a private key")
    if CLOUD_KEY.search(line):
        out.append("something that looks like a cloud access key")
    return out


def line_problems(line, addresses=True):
    """What is wrong with one line of text, as a list of sentences.

    `addresses` is False for a file whose numbers are not addresses (the path data of an SVG).
    """
    if ALLOW_MARKER in line:
        return []
    out = []
    for email in emails_in(line):
        if not email.endswith(ALLOWED_EMAIL_SUFFIXES):
            out.append(f"email address `{email}`")
    out += [f"home folder `{path}`" for path in home_paths_in(line)]
    if addresses:
        out += [f"private network address `{address}`" for address in private_addresses_in(line)]
    out += [f"private host name `{name}`" for name in private_hosts_in(line)]
    out += secrets_in(line)
    return out


def is_text(data):
    return b"\0" not in data[:8192]


def git(root, *args):
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, timeout=120, check=False)
    if done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {done.stderr.decode('utf-8', 'replace').strip() or 'failed'}")
    return done.stdout.decode("utf-8", "replace")


def scan_tree(root=HERE):
    """(problems, number of files read) for every tracked text file under `root`."""
    problems = []
    scanned = 0
    for name in git(root, "ls-files", "-z").split("\0"):
        path = root / name
        if not name or not path.is_file() or path.stat().st_size > MAX_SCAN_BYTES:
            continue
        data = path.read_bytes()
        if not is_text(data):
            continue
        scanned += 1
        addresses = path.suffix.lower() != ".svg"
        for number, line in enumerate(data.decode("utf-8", "replace").splitlines(), start=1):
            problems += [f"{name}:{number}: {problem}" for problem in line_problems(line, addresses)]
    return problems, scanned


def no_reply(address):
    return address.endswith(ALLOWED_EMAIL_SUFFIXES)


def default_branch(root):
    """The default branch as a ref this clone has, or None."""
    try:
        return git(root, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").strip()
    except RuntimeError:
        pass
    for ref in ("refs/remotes/origin/main", "refs/heads/main"):
        try:
            git(root, "rev-parse", "--verify", "--quiet", ref)
            return ref
        except RuntimeError:
            continue
    return None


def identity_problems(log):
    """Problems in `git log --format='%H %ae %ce'` output: one per address that is not no-reply."""
    out = []
    for line in log.splitlines():
        commit, _, addresses = line.partition(" ")
        author, _, committer = addresses.partition(" ")
        for who, address in (("author", author), ("committer", committer)):
            if not no_reply(address):
                out.append(f"commit {commit[:10]}: the {who} address is not a no-reply address")
    return out


def first_no_reply(log):
    """The first commit of an oldest-first log whose two addresses are both no-reply, or None."""
    for line in log.splitlines():
        commit, author, committer = (line.split(" ") + ["", ""])[:3]
        if no_reply(author) and no_reply(committer):
            return commit
    return None


def scan_identities(root=HERE, head="HEAD"):
    """(problems, number of commits read) for the commits that lead to `head`."""
    try:
        git(root, "rev-parse", "--verify", "--quiet", f"{head}^{{commit}}")
    except RuntimeError:
        if head == "HEAD":
            return [], 0  # no commit yet
        raise
    fmt = "--format=%H %ae %ce"
    base = default_branch(root) or head
    start = first_no_reply(git(root, "log", "--reverse", fmt, base))
    if start is None:
        # The default branch has no no-reply commit: read only what `head` adds to it.
        log = git(root, "log", fmt, head, "--not", base)
    else:
        log = git(root, "log", fmt, head, "--not", f"{start}^@")
    return identity_problems(log), len(log.splitlines())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--head",
        default="HEAD",
        metavar="REV",
        help="read the commits that lead to REV (a pull request's own head, where HEAD is GitHub's merge commit)",
    )
    args = parser.parse_args(argv)
    try:
        problems, files = scan_tree()
        in_commits, commits = scan_identities(head=args.head)
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(f"privacy: {error}", file=sys.stderr)
        return 2
    for problem in problems + in_commits:
        print(f"FOUND    {problem}")
    if problems or in_commits:
        print(
            f"{len(problems) + len(in_commits)} found in {files} tracked text file(s) and {commits} commit(s). "
            f"Remove each one, or end a line that must keep it with `{ALLOW_MARKER}`."
        )
        return 1
    print(f"Nothing personal and no secret found in {files} tracked text file(s) and {commits} commit(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
