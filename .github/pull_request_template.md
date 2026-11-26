<!-- A pull request is optional here (project decision 0002). A change pushed straight to `main` follows the same list. Delete the lines that do not apply. -->

## What changed, and why


## Where

- [ ] `project/` (the map, the decisions, the carried text)
- [ ] `brand/`
- [ ] `website/`
- [ ] `website/wiki/`
- [ ] `launcher/`, or something else:

## Checked

- [ ] The "Check before pushing" lines in `AGENTS.md` for each folder above were run and pass.
- [ ] `python3 project/check_links.py` passes, if a Markdown file changed.

## Other repositories

- [ ] This follows a change in another repository, and links it in full (`jamescjfoundation/<repository>#<number>` or the commit's address): an app's commit or release for a wiki or website change (Routes C, D, E and J of `project/README.md`).
- [ ] Brand files were changed in the kit (`brand/source/`), never in a copy, and the copies here were updated. Each app's copies follow in that app's repository (Route F).
- [ ] The project block or a carried block changed: `python3 project/carry.py --write` was run, and each app's `AGENTS.md` follows (Route N).
- [ ] No other repository needs to change.

## Public

- [ ] Nothing here holds a person's name or email, an account name, details of a machine, anything said in a conversation, an open security problem or a secret ("What is public" in `AGENTS.md`).
- [ ] The website and the wiki say only what the apps do today.
