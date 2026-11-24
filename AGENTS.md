# AGENTS.md

Guidance for anyone, human or agent, changing this repository.

## What this repository is

A monorepo for the shared, project-wide pieces of Wordsmith. The apps (Script, Manuscript, Book) and their shared base (`open-source-core`) live in their own repositories under `jamescjfoundation`; don't copy their code here. Each top-level folder is an independent project with its own tooling:

| Folder | Stack | Owns |
| --- | --- | --- |
| `website/` | Plain HTML/CSS/JS, a Python 3 page generator, no dependencies | The public site |
| `wiki/` | Not chosen yet | Suite-wide user and contributor docs |
| `launcher/` | Rust (planned) | Wordsmith Launcher desktop app |
| `.github/workflows/` | GitHub Actions | CI and deploys, one workflow per folder |

Keep changes inside one folder where you can. A change that spans folders (for example, launcher status on the website) should say so in the commit message.

## Project-wide rules

These come from the project's public promises on the website. Don't break them.

- **Privacy:** no telemetry, analytics, accounts, trackers or third-party requests. The website self-hosts its fonts for this reason; no CDNs, Google Fonts or embeds. The only network request any app makes on its own is the update check with GitHub, and it can be turned off.
- **Licensing:** code is MIT OR Apache-2.0. Only add dependencies with compatible licenses, and credit them (README/NOTICE).
- **Names:** "Wordsmith", "Wordsmith & Ink", "Wordsmith Script", "Wordsmith Manuscript", "Wordsmith Book" are trademarks. Use them exactly as written. The launcher is "Wordsmith Launcher".
- **Brand assets** in `website/assets/brand/` are copied unchanged from the brand kit. Don't edit them; replace them from the kit.
- **Writing style:** plain, short, friendly sentences for writers, not developers. No marketing superlatives. Don't claim a feature exists before it does; mark planned things as planned.

## website/

- Pages are generated. The shared header, footer and all page text are in `website/tools/build.py`. Edit that, then run `python3 website/tools/build.py` from the repo root and commit the regenerated `.html` files with it. Don't hand-edit the `.html` pages; the next build overwrites them.
- Styles: `website/assets/css/site.css` (brand color tokens, dark theme follows the system). JS: `website/assets/js/site.js`; the site must work with JS off.
- Links between pages stay relative, so the site also works from a local preview or a subpath. It is served at `https://wordsmithand.ink/`; the only absolute URLs are the canonical, `og:url` and `og:image` tags, built from `SITE` in `build.py`. The 404 page is the exception: `build.py` makes its local links start at `/`, because Pages shows it at any missing address, including ones inside folders.
- Preview: `python3 -m http.server -d website` then http://localhost:8000.
- Deploy: `.github/workflows/pages.yml` publishes `website/` on every push to `main` that touches it. Pages is set to the "GitHub Actions" source, with the custom domain `wordsmithand.ink` set in the repository's Pages settings.
- Check before committing: every page builds, no broken relative links or missing assets, images have `alt` text, and the page reads well at phone width and in dark mode.

## wiki/

Not built yet. The tool hasn't been picked. When it is:

- Record the choice and the build/preview commands in `wiki/README.md` and here.
- A repository has one GitHub Pages site. To publish the wiki on Pages, build it into the website's Pages artifact (for example under `/wiki/`) in `pages.yml` rather than adding a second Pages deploy.
- Write for writers first; contributor docs go in their own section.

## launcher/

Not started. When it is:

- A Rust crate (or Cargo workspace) rooted at `launcher/`, so `cargo` commands run from there: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`.
- Match the apps' choices where it makes sense (egui for UI, `open-source-core` if it fits) so the suite looks and behaves as one.
- Downloads come only from the project's official GitHub releases and are verified before anything runs. Update checks can be turned off. No accounts, no telemetry.
- Targets macOS, Windows and Linux.
- Add a `launcher.yml` workflow scoped to `paths: ["launcher/**"]` when there is code to check.
- Keep `website/launcher.html` (via `build.py`) in step with what the launcher actually does.

## Git

- `main` is the default branch and deploys the website. Work on a branch and open a pull request for anything beyond a typo.
- Keep commits focused, with a short imperative subject.
- Don't commit build output other than the generated website pages, or `target/`, `node_modules/` or editor files.
