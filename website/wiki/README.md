# Wordsmith Wiki

User guides for Wordsmith Script, Manuscript and Book, published at https://wordsmithand.ink/wiki/.

Built with [Fumadocs](https://fumadocs.dev) on Next.js and exported as static files. It's its own project, separate from the main site's plain HTML, and shares only the domain, the fonts and the logos.

## Writing pages

Pages are MDX (Markdown with a few components) in `content/docs/`:

| Folder | Sidebar tab |
| --- | --- |
| `index.mdx` | The wiki's home page |
| `start/` | Getting started: the suite, installing, files, privacy, help |
| `script/`, `manuscript/`, `book/` | One tab per app |

- Each page starts with frontmatter: `title`, a one-line `description`, and optionally `icon` (a [Lucide](https://lucide.dev/icons) icon name).
- Each folder's `meta.json` sets the page order (`pages`) and, for the tabs, `"root": true`.
- Link to other pages by their file: `[Views](./views.mdx)` or `<Card title="Views" href="./views.mdx" />`.
- Put pictures next to the pages (`script/images/…`) and link them relatively: `![The page view](./images/page-view.webp)`.
- Components you can use without an import: `Callout`, `Cards`/`Card`, `Steps`/`Step`, `Tabs`/`Tab`, `Accordions`/`Accordion`, `Files`/`Folder`/`File`, `Kbd` (`<Kbd>Ctrl</Kbd>+<Kbd>S</Kbd>`) and `Status` (`<Status value="available|in-progress|planned" />`). They're registered in `components/mdx.tsx`.
- Don't put `<Status>` or other components inside a heading: the page fails with "Status is not defined". Put it on the line under the heading.
- Write for writers, in plain, short sentences. Only describe what an app does today, and mark the rest as planned. The rules are in the repository's `AGENTS.md`.

## Running it

Needs Node.js 22 or later.

```sh
cd website/wiki
npm install
npm run dev        # http://localhost:3000/wiki/ (the fonts and logos come from the main site, so they're missing here)
npm run build      # static export into out/, the same as the deploy
```

The deploy (`.github/workflows/pages.yml`) runs `npm ci && npm run build` and publishes `out/` at `/wiki/` next to the main site.

### Local preview with the main site: wordwiki.test

On the development machine, https://wordwiki.test serves the main site from `website/` and passes `/wiki/` to the wiki's dev server, so it looks exactly like the deployed site and updates as you save. It's temporary and not part of the deploy:

- the nginx site `/etc/nginx/sites-available/wordwiki` (enabled in `sites-enabled`), with the certificate `/etc/nginx/certs/wordwiki.test{,-key}.pem`;
- the supervisor program `wordwiki` (`/etc/supervisor/conf.d/wordwiki.conf`), which runs `next dev` on 127.0.0.1:3020. Logs: `/var/log/supervisor/wordwiki.log`. Restart it with `sudo supervisorctl restart wordwiki`.

To remove it:

```sh
sudo supervisorctl stop wordwiki
sudo rm /etc/supervisor/conf.d/wordwiki.conf /etc/nginx/sites-enabled/wordwiki /etc/nginx/sites-available/wordwiki /etc/nginx/certs/wordwiki.test.pem /etc/nginx/certs/wordwiki.test-key.pem
sudo supervisorctl update && sudo nginx -t && sudo systemctl reload nginx
```
