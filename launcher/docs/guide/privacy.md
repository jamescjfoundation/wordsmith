# What the launcher sends

The launcher has no account, no tracking and no statistics. It talks to one service, GitHub,
where the Wordsmith apps publish their releases.

## The requests

| When | What is asked | Of whom |
| --- | --- | --- |
| When the launcher starts, and when you choose the round arrow above the cards (or F5) | The list of releases of each of the three apps | `api.github.com`, or `github.com` when the first does not answer |
| When the launcher starts, and when you choose Check for Updates | The newest release of the launcher itself | `api.github.com` |
| When you install or update an app | The release's list of checksums, and the app's download | `github.com`, which hands the download to GitHub's file store |

Each request carries the launcher's name and version, and nothing else: nothing about you, your
computer or your documents, and no token. GitHub sees the address the request comes from, as
any website does.

## Turning the automatic requests off

File, then About: clear "Check for updates when the app starts". The launcher then asks nothing
by itself, for the apps or for itself. The window shows what is installed, and **Check Now**
asks when you want it to.

Installing an app always needs the network.
