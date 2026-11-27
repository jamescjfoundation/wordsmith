<!-- Every change lands through a pull request whose checks pass; its author merges it (project decision 0002). Delete the lines that do not apply. -->

## What changed, and why


## Where

- [ ] `project/` (the map, the decisions, the carried text)
- [ ] `brand/`
- [ ] `website/`
- [ ] `website/wiki/`
- [ ] `launcher/`, or something else:

## Checked

- [ ] The "Check before pushing" lines in `AGENTS.md` for each folder above were run and pass.
- [ ] The "Checks" run on this pull request is green. It is not required, so a red run does not stop the merge: look.

## Other repositories

- [ ] This follows a change in another repository, and links it in full (`jamescjfoundation/<repository>#<number>` or the commit's address): an app's commit or release for a wiki or website change (Routes C, D, E and J of `project/README.md`).
- [ ] Brand files were changed in the kit (`brand/source/`), never in a copy, and the copies here were updated with `npm run brand`. Each app's copies follow in that app's repository (Route F).
- [ ] The project block or a carried block changed: `python3 project/carry.py --write` was run, and each app's `AGENTS.md` follows (Route N).
- [ ] No other repository needs to change.

## Public

- [ ] Nothing here holds a person's name or email, an account name, details of a machine, anything said in a conversation, an open security problem or a secret ("What is public" in `AGENTS.md`). `python3 project/privacy.py` finds what a pattern can; the rest is read by eye.
- [ ] The website and the wiki say only what the apps do today.
