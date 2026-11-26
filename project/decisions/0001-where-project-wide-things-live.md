# 0001: Where project-wide things live

Date: 2026-11-26. Status: accepted.

## Context

Wordsmith is five repositories and two forks. Each was built with its own rules, and the only description of how they fit together sat outside all of them. An agent with one repository could not learn that the others exist: nothing in an app pointed to the wiki, the website or the brand kit, and nothing said how a change crosses from one repository to another.

Two repositories could hold a map and the rules that span the project: open-source-core, which every app already takes shared files from, and wordsmith, which holds the project's shared pieces. The core is a general base. Projects other than Wordsmith can build on it, so its code and rules must not depend on one product family.

## Decision

- The wordsmith repository owns the project map and the project-wide rules, in `project/`: `project/README.md` (the repositories, how they depend on each other, the routes, where to look and write, the rules) and `project/decisions/` (these records).
- open-source-core holds only what is general to any app built on it: the rules for building between an app and the core, its own releases, the upstream rule, and the shared settings and tooling. It names no Wordsmith product in its code or its rules.
- A decision about one app stays in that app's `docs/decisions/`.
- Every Wordsmith repository carries, in its `AGENTS.md`, the block marked in `project/README.md`: the repository table, the dependencies and the route table, with links back to the map. The block is changed here and copied out, never edited in a copy.
- Records that cross repositories are written as full links, never as bare paths, and a decision named outside its own repository says whose it is ("core decision 0011").

## Consequences

- One place answers "where does this go". A route is changed in one file.
- The core stays usable by other projects. A rule that is true of any app on the core is written there once; a rule that is about Wordsmith is written here.
- The carried block is a copy, so it can go stale. Until a tool checks the copies, whoever changes the block updates every repository's copy in the same piece of work.
  - 2026-11-26: a tool now does both. `project/carry.py` writes the block into each app's `AGENTS.md`, and the `carried.yml` workflow in the wordsmith repository fails while a published copy differs ([Route N](../README.md#route-n)). The copies are in the three apps; open-source-core carries none, since it names no product, and the wordsmith repository reads the map itself.
- Rules that were written into the core or an app but are really project-wide (naming other products, how changes land) move here, and the older text is corrected to point here.

## Revisit when

A second project builds on the core and needs some of the same rules (the general part then moves to the core), or the copies of the block drift more than once (the check becomes urgent).
