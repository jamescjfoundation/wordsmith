# How a download is checked

## What the launcher checks for you

Every release of a Wordsmith app has a file named `SHA256SUMS.txt`. It lists one checksum for
each download: a long number worked out from the file's contents, which changes when a single
byte of the file changes.

Before the launcher opens a download, it:

1. reads `SHA256SUMS.txt` from the same release of the app, on GitHub;
2. works out the checksum of the file it downloaded;
3. compares the two. They must be the same, and when GitHub itself gives a checksum for the
   file, that one must be the same too.

If anything differs, or the list has no line for the file, the file is thrown away and nothing
is installed. The line under the app's name says so.

The downloads come from the app's own releases page on GitHub and from nowhere else. The
launcher does not take a download address from anything it reads.

A checksum shows that the file is the one the release holds. It does not show who built it.
The apps' builds are not signed with a publisher's certificate yet.

## Checking the launcher's own download

Nothing checks the launcher before you have it, so do it yourself once. Download
`SHA256SUMS.txt` beside the launcher's file, then:

```sh
sha256sum --check --ignore-missing SHA256SUMS.txt   # Linux
shasum -a 256 --check --ignore-missing SHA256SUMS.txt   # macOS
```

On Windows, `certutil -hashfile <the file> SHA256` prints the checksum; compare it with the
file's line in `SHA256SUMS.txt`.

Each release file also has a build provenance attestation on GitHub, a signed statement of where
and from which commit it was built. With GitHub's command line (`gh`):

```sh
gh attestation verify wordsmith-launcher-X.Y.Z-linux-x86_64.tar.gz --repo jamescjfoundation/wordsmith
```

For a download of an app, the files are built by a workflow the apps share, so its repository is
named as the signer:

```sh
gh attestation verify wordsmith-book-X.Y.Z-linux-x86_64.tar.gz --repo jamescjfoundation/wordsmith-book \
  --signer-repo jamescjfoundation/open-source-core
```
