# Project decisions

Decisions that hold across the whole Wordsmith project, one file each, numbered in order: `NNNN-title.md` with four parts: **Context**, **Decision**, **Consequences**, **Revisit when**.

What goes where:

- A rule for every Wordsmith repository, or for how two of them work together: here.
- A decision about an interface, a tool or the upstream rule that any app built on the core shares: the core's [`docs/decisions/`](https://github.com/jamescjfoundation/open-source-core/tree/main/docs/decisions). The core is general and names no product.
- A decision about one app's behavior: that app's `docs/decisions/`.

Every repository numbers its decisions from 0001. Outside a repository, say whose record you mean: "project decision 0002", "core decision 0011", "Book decision 0003".

| Number | Title |
| --- | --- |
| [0001](0001-where-project-wide-things-live.md) | Where project-wide things live |
| [0002](0002-how-changes-land-and-who-releases.md) | How changes land, who releases, and how far behind the core an app may be |
| [0003](0003-naming-other-companies-programs-and-formats.md) | Naming other companies, programs and file formats |
| [0004](0004-apps-that-depend-on-apps.md) | Apps that depend on apps |
| [0005](0005-one-guide-per-app.md) | One user guide per app, kept in the app |
