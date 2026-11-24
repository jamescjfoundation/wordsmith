#!/usr/bin/env python3
"""Rebuilds the Wordsmith brand kit: logos, app icons, lockups, palettes, the production sets,
and (with --pdf) the two guideline PDFs.

    python3 brand/source/fetch_fonts.py          # once
    python3 brand/source/build.py                # build into brand/build/ and compare with brand/
    python3 brand/source/build.py --write        # also update the changed files in brand/
    python3 brand/source/build.py --pdf          # also render the PDFs (needs Node and Playwright)

Nothing in brand/ changes without --write, and then only files whose content changed. SVGs are
compared without the C2PA metadata the kit's exporter added, and PNGs by their pixels. Hand-written
files (READMEs, the brand guide, the apps' tokens.json, the introduction PDF) are never touched.
Python needs fonttools, cairosvg, numpy and pillow (see requirements.txt).
"""
import argparse, hashlib, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HERE)
APPS = {"script": "Wordsmith Script", "manuscript": "Wordsmith Manuscript", "book": "Wordsmith Book"}
MARK = {"script": "wordsmith-mark", "manuscript": "wordsmith-manuscript-mark", "book": "wordsmith-book-mark"}
PDFS = {"brand": "Wordsmith & Ink - Brand Guidelines.pdf", "products": "Wordsmith Apps - Product Assets.pdf"}


def run(*cmd, **kw):
    subprocess.run([*cmd], check=True, **kw)


def build(out):
    py = sys.executable
    os.makedirs(out, exist_ok=True)
    run(py, os.path.join(HERE, "buildink.py"), os.path.join(out, "wordsmith-and-ink"))
    for app in ("manuscript", "book"):
        run(py, os.path.join(HERE, "buildp.py"), app, os.path.join(out, f"wordsmith-{app}"))
    run(py, os.path.join(HERE, "buildc.py"), os.path.join(out, "wordsmith-script"))
    sys.path.insert(0, HERE)
    import buildp, palettes
    os.makedirs(os.path.join(out, "wordsmith-script", "palette"), exist_ok=True)
    buildp.write_palette(APPS["script"], "wordsmith-script", palettes.SCRIPT, os.path.join(out, "wordsmith-script", "palette") + "/")

    ink = os.path.join(out, "wordsmith-and-ink")
    for app in APPS:
        slug = f"wordsmith-{app}"; d = os.path.join(out, slug)
        # each app's logo folder also holds its endorsed lockup
        for v in ("ink", "paper"):
            shutil.copy(os.path.join(ink, "lockups", f"{slug}-endorsed-{v}.svg"), os.path.join(d, "logo"))
        # the ready-to-use production set (its README is hand-written and kept as it is)
        prod = os.path.join(d, "production"); os.makedirs(prod, exist_ok=True)
        files = [("app-icon", "favicon.svg"), ("app-icon", "icon-1024.png"), ("palette", f"{slug}-palette.svg")]
        files += [("logo", f"{slug}-{k}-{v}.svg") for k in ("wordmark", "stacked") for v in ("ink", "paper")]
        files += [("logo", f"{MARK[app]}-{v}.svg") for v in ("ink", "paper")]
        for src, name in files:
            shutil.copy(os.path.join(d, src, name), prod)
        for src, name in [("app-icon", "wordsmith-and-ink-icon.svg")] + [
                (folder, f"wordsmith-and-ink-{k}-{v}.svg") for folder, k in (("lockups", "family"), ("logo", "imprint"), ("logo", "mark")) for v in ("ink", "paper")]:
            shutil.copy(os.path.join(ink, src, name), prod)


def pdf(out):
    """Renders the two PDFs from the files in brand/ (so run it after --write to show new logos)."""
    pdf_out = os.path.join(out, "pdfs"); os.makedirs(pdf_out, exist_ok=True)
    env = dict(os.environ, WORDSMITH_BRAND=BRAND, WORDSMITH_PDF_OUT=pdf_out)
    for n in PDFS:
        run(sys.executable, os.path.join(HERE, "pdf", f"{n}.py"), env=env, cwd=os.path.join(HERE, "pdf"))
    if not os.path.isdir(os.path.join(HERE, "node_modules", "playwright")):
        sys.exit("Rendering the PDFs needs Playwright: cd brand/source && npm install && npx playwright install chromium")
    run("node", os.path.join(HERE, "pdf", "render.js"), *PDFS, env=env, cwd=HERE)
    for n, name in PDFS.items():
        os.replace(os.path.join(pdf_out, f"{n}.pdf"), os.path.join(pdf_out, name))


def norm(path):
    """Content to compare: SVGs without C2PA metadata, PNGs as pixels, everything else as bytes."""
    if path.endswith(".svg"):
        s = open(path, "rb").read()
        s = re.sub(rb' xmlns:c2pa="[^"]*"', b"", s)
        return re.sub(rb"<metadata><c2pa:manifest>.*?</c2pa:manifest></metadata>", b"", s, flags=re.S)
    if path.endswith(".png"):
        from PIL import Image
        im = Image.open(path).convert("RGBA"); return repr(im.size).encode() + im.tobytes()
    if path.endswith(".ico"):
        from PIL import Image
        im = Image.open(path); return b"".join(repr(s).encode() + im.ico.getimage(s).convert("RGBA").tobytes() for s in sorted(im.info["sizes"]))
    return open(path, "rb").read()


def compare(out, write, only=None):
    changed, new, same = [], [], 0
    for root, _, files in os.walk(out):
        for f in files:
            src = os.path.join(root, f); rel = os.path.relpath(src, out)
            if rel.endswith(".html") or (only and not rel.startswith(only)):
                continue
            dest = os.path.join(BRAND, rel)
            if not os.path.exists(dest):
                new.append(rel)
            elif rel.endswith(".pdf") or norm(src) != norm(dest):
                changed.append(rel)
            else:
                same += 1; continue
            if write:
                os.makedirs(os.path.dirname(dest), exist_ok=True); shutil.copy(src, dest)
    print(f"\n{same} unchanged, {len(changed)} changed, {len(new)} new" + (" (written to brand/)" if write and (changed or new) else ""))
    for rel in sorted(changed): print("  changed", rel)
    for rel in sorted(new): print("  new    ", rel)


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--out", default=os.path.join(BRAND, "build"), help="build folder (default brand/build, not committed)")
    a.add_argument("--write", action="store_true", help="copy changed and new files into brand/")
    a.add_argument("--pdf", action="store_true", help="also render the two guideline PDFs")
    args = a.parse_args()
    out = os.path.realpath(args.out)
    # the build folder is emptied first, so it must not be brand/ itself, a folder holding it, or a kit folder in it
    if os.path.commonpath([out, BRAND]) == out or (out.startswith(BRAND + os.sep) and out != os.path.join(BRAND, "build")):
        sys.exit("--out must be brand/build or a folder outside brand/")
    shutil.rmtree(out, ignore_errors=True)
    build(out)
    compare(out, args.write)
    if args.pdf:
        pdf(out)  # after the logos are written, so the PDFs show them
        compare(out, args.write, only="pdfs" + os.sep)


if __name__ == "__main__":
    main()
