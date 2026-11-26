# 0003: Naming other companies, programs and file formats

Date: 2026-11-26. Status: accepted. Replaces the older rule in the three apps.

## Context

The apps began under a rule that no code, document, commit or fixture ever names another company, product or program. Each app wrote it down in its own words, and one app had a check that read a private list of names.

The rule cost more than it protected. An app has to say which programs' files it opens and which formats it writes. A book tool has to say what an ebook store or a print service expects of a file. "A print-on-demand service's file guide" tells a reader less than the name does, and a source that cannot be named cannot be checked. The wiki and the website already named other programs, because writers moving to Wordsmith need to know what comes across. The private list is gone, so the check passed on anything.

The change was raised in each app separately, as the same issue three times: [wordsmith-script#3](https://github.com/jamescjfoundation/wordsmith-script/issues/3), [wordsmith-manuscript#6](https://github.com/jamescjfoundation/wordsmith-manuscript/issues/6), [wordsmith-book#1](https://github.com/jamescjfoundation/wordsmith-book/issues/1). It is one rule for the whole project, so it is recorded once, here.

## Decision

- Code, documents, commit messages and fixtures may name another company, program, service or file format where that is a fact a reader needs: what an app opens or writes, what a store or printer requires, where a rule comes from. A source is cited by name and address.
- **Interface names, designs and help text stay our own.** A menu label, a feature name, a built-in design or a template is never another product's name or its distinctive feature name. Naming a program to say we open its files is not the same as using its words in our menus.
- An app is never described as replacing, following or being inspired by another product.
- **Apps never name WordCraft or craft-libs crates or types.** That is an architecture rule of the core (core decision [0002](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0002-layers.md)), and it does not change.
- **People are never named** in any repository.
- A check that only read the private list of names is removed, not kept as a check that cannot fail.

## Consequences

- Each app's `AGENTS.md`, `CONTRIBUTING.md` and plan are corrected to this rule, and the three issues are closed against those changes.
- Sources that were kept private only because of the old rule can be cited in the open.
- Trademarks are still other people's: a name is used to state a fact, never as our own label, and never with another company's logo.

## Revisit when

A name used as a fact draws a complaint from its owner, or interface text starts to borrow another product's names.
