# 0004: Apps that depend on apps

Date: 2026-11-26. Status: accepted.

## Context

The shared rules said an app depends only on the core. Two dependencies between Wordsmith apps exist all the same, and both are right for what they do:

- Wordsmith Book builds on Wordsmith Manuscript's `manuscript-model` and `manuscript-format` crates, at a tag of Manuscript's repository, because it opens Manuscript projects. A second reader in Book would drift from the format.
- Wordsmith Manuscript reads Wordsmith Script's `.wss` files with a reader of its own, so that a screenplay kept in a novel's project can be shown.

Neither had a rule. What Book needed from Manuscript sat in a file in Book's repository that nothing in Manuscript pointed to. Nothing on Manuscript's side built Book, so a rename there could break Book unseen. Script's format rule did not know Manuscript read the format.

The general rule for any project on the core is core decision [0015](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0015-apps-that-depend-on-apps.md). This record says how it applies to Wordsmith.

## Decision

A Wordsmith app may depend on another, under a contract the providing app owns.

| Consumer | Provider | What crosses | The contract |
| --- | --- | --- | --- |
| Wordsmith Book | Wordsmith Manuscript | The model and format crates; `.wsm` and `.wsmz` projects, read; an offers file, written | Manuscript's [`docs/book-handoff.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/docs/book-handoff.md) |
| Wordsmith Manuscript | Wordsmith Script | `.wss` files, read | Script's [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/docs/format.md) |

- The contract lists what the consumer may use and the format versions it reads. The provider tags the commits a consumer may pin and never moves such a tag.
- A need goes in as an issue in the provider's repository. Anyone working in the consumer, an agent included, may open it. The consumer keeps at most a list of links.
- A change to the provider is its own change in the provider's repository, landed and tagged first. A consumer's change never edits the provider.
- The provider checks its consumers before a change to the contract lands, and opens an issue in the consumer for anything it must follow.
- Both apps of a pair build on the same core release, so a consumer holds one core.
- The same rule covers any later pair, in any direction. Something a third app would also need is general: it goes to the core.

The steps are Route B in the [project map](../README.md#route-b).

## Consequences

- Manuscript's model and format stay Manuscript's. They do not move into the core, which would put manuscript concepts into a base meant for any project.
- Book's existing requests become issues in Manuscript's repository, and the contract is rewritten around what Book really uses, including the project schema.
- Manuscript needs a check that builds Book, and a written scheme for book-view tags. Until both exist, a break is found only when Book moves to a new tag.
- Script's format rule names Manuscript as a reader, and Manuscript refuses a `.wss` version newer than the one it was written for.

## Revisit when

A third app needs Manuscript's crates (the shared part may then deserve a repository of its own), or a contract grows to most of its provider's public interface.
