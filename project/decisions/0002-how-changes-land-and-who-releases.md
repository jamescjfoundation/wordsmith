# 0002: How changes land, who releases, and how far behind the core an app may be

Date: 2026-11-26. Status: accepted.

## Context

The written rules asked for a pull request with a person's approval for every change, a person's approval for every core release, and apps never more than one core release behind. Practice was different in all three. Almost every change was pushed straight to `main`. The core was released many times in two days, most releases cut during one app's build, because a core change reaches an app only through a release. Two apps fell more than ten releases behind while the third kept up. A rule that the history contradicts teaches nothing: a reader cannot tell whether to follow the text or the practice.

Nothing is in users' hands yet. No app has a published release, so a broken `main` blocks no one but the people and agents working on it, and CI is free on public repositories.

## Decision

- **Landing.** While no app has a published release, a change may be pushed straight to `main` in any Wordsmith repository. The repository's gate is run first: `cargo xtask ci` in the Rust repositories, the checks in `AGENTS.md` in wordsmith. A pull request is optional; its author merges it once its checks pass, without waiting for a review. Whoever turns `main` red fixes it at once.
- **Releases.** A person or an agent may release the core or an app, once the release's gate has passed on the commit. This covers patch and minor releases of the core and every app release. No release is cut on a commit whose gate has not passed. The core's side of this is core decision [0011](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0011-releases-and-versioning.md).
- **Upstream pins.** Moving the core to a newer upstream release follows the train in the core's `docs/UPSTREAM.md`, and may also be done by a person or an agent once the contract tests and the gate pass (core decision [0004](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0004-follow-hold-own.md)).
- **Core pins.** An app moves to the newest core release before new work starts on it and before its own release. Between those it may fall behind. An app more than three core releases behind gets an issue in its repository saying so.
- **What still needs a person.** Rewriting public history, changing a repository's settings on GitHub, and anything that cannot be undone.

## Consequences

- The text now matches what happens, so it can be followed.
- A core fix an app needs does not wait on one person: build it, pass the gate, release, move the pin.
- `main` can be red for a short time. That is accepted until the first app release.
- The release rule puts all the weight on the gate. A gate that reports green for something it did not test is now a release risk, so gaps in the gate are fixed before they are worked around.
- "One release behind" is gone. An app that nobody is working on may sit several releases back; the cost is paid when work on it starts, as one move.

## Revisit when

The first app publishes a release. From then on a broken `main` or a bad release reaches writers, and the landing and release rules are looked at again: required checks before `main` changes, and who may publish an app release.
