# The files in this folder do not run

GitHub reads workflows, the pull request template and Dependabot's settings only at the root of
a repository. The launcher is a folder of the wordsmith repository, so nothing here is read by
GitHub.

The files are the ones every app built on open-source-core carries. `cargo xtask sync` writes
them and `cargo xtask sync --check`, a task of the launcher's gate, fails when one is missing or
differs from the pinned core release. They are kept for that, and so that the workflows that do
run can be compared with them.

| Here | What runs instead, at the repository's root |
| --- | --- |
| `workflows/ci.yml` | `.github/workflows/launcher.yml` |
| `workflows/release.yml` | `.github/workflows/release.yml` |
| `workflows/core-pin.yml` | `.github/workflows/launcher-core-pin.yml` |
| `pull_request_template.md` | `.github/pull_request_template.md`, the repository's own |
| `dependabot.yml` | Nothing: the repository has no Dependabot settings |

[Decision 0001](../docs/decisions/0001-an-app-in-a-folder-of-the-wordsmith-repository.md) says
why, and what is asked of the core so that the root files can become short callers of its
shared workflows.
