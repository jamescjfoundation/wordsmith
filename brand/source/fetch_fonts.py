#!/usr/bin/env python3
"""Downloads the fonts the brand kit is drawn with into brand/source/fonts/ (not committed).

    python3 brand/source/fetch_fonts.py

Courier Prime (logos, palette cards) and Inter 4.0 (endorsement and Foundation lines, labels),
both under the SIL Open Font License 1.1. These exact files reproduce the committed logos and
icons; another version of either font changes the letter outlines slightly. Each file is checked
against its SHA-256 before it is used. Uses only the Python standard library.
"""
import hashlib, io, os, sys, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("WORDSMITH_FONT_DIR", os.path.join(HERE, "fonts"))

COURIER = "https://raw.githubusercontent.com/google/fonts/cc9ce5318f8f50a32695e38ef0be8b0e453c7304/ofl/courierprime/"
INTER_ZIP = "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip"
INTER_ZIP_SHA = "ff970a5d4561a04f102a7cb781adbd6ac4e9b6c460914c7a101f15acb7f7d1a4"

# saved name: (source, path in source, sha256)
FONTS = {
    "CourierPrime-700.ttf": (COURIER + "CourierPrime-Bold.ttf", None, "ff1f38786c849d1c41fa8e447960abdb2bd75fdfb0cfcdeb524fad65a5af3638"),
    "CourierPrime-400.ttf": (COURIER + "CourierPrime-Regular.ttf", None, "72f793376f8e2841656bf21d77a5de010f2929bd6956a22ee848ad0c7eb978af"),
    "Inter-400.otf": (INTER_ZIP, "extras/otf/Inter-Regular.otf", "be6d709dcb730ddaf050cbdae6fe89bd56d5d14dc66885639bbf6f06bd03521b"),
    "Inter-500.otf": (INTER_ZIP, "extras/otf/Inter-Medium.otf", "1e65171fccd6f445b7742728454620ec2867356c849af78e71bf2c4f0e3d97ba"),
    "Inter-600.otf": (INTER_ZIP, "extras/otf/Inter-SemiBold.otf", "bd68706b7bf8b3c580ae57685a2116bb1704b3a9998309ccfec7cd486f8a593e"),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def get(url):
    print("downloading", url)
    with urllib.request.urlopen(url) as r:
        return r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    for name, (url, member, want) in FONTS.items():
        dest = os.path.join(OUT, name)
        if os.path.exists(dest) and sha(open(dest, "rb").read()) == want:
            print("ok", name)
            continue
        if url not in cache:
            data = get(url)
            if url == INTER_ZIP and sha(data) != INTER_ZIP_SHA:
                sys.exit(f"Checksum mismatch for {url}")
            cache[url] = data
        data = zipfile.ZipFile(io.BytesIO(cache[url])).read(member) if member else cache[url]
        if sha(data) != want:
            sys.exit(f"Checksum mismatch for {name}")
        open(dest, "wb").write(data)
        print("saved", name)
    print("Fonts are in", OUT)


if __name__ == "__main__":
    main()
