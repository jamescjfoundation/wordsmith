# Recorded releases

The first public release of each Wordsmith app, 0.9.0, as it was published on 2026-11-27. The
tests in `tests/releases.rs` read them through the same code the launcher reads GitHub with, so
they pass without a network.

| File | What it is |
| --- | --- |
| `<id>-releases.json` | GitHub's answer to `GET /repos/jamescjfoundation/<id>/releases`, kept to the members the launcher reads: the tag, whether it is a draft or a pre-release, the day, and each file's name, size and checksum |
| `<id>-SHA256SUMS.txt` | The release's `SHA256SUMS.txt`, byte for byte |

They are public data, and they are never edited. `cargo xtask live` reads the same releases
from GitHub itself, and installs one of them.
