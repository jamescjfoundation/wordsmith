#!/usr/bin/env python3
"""Local preview of the website (python3 website/tools/serve.py [port], then http://localhost:8000).

Like `python3 -m http.server -d website`, but it serves /about from about.html and shows 404.html for
missing pages, the way GitHub Pages does. The site's links leave off ".html", so plain http.server
can't follow them. The wiki at /wiki/ isn't served here; it's a separate project (see wiki/README.md).
"""
import http.server, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def translate_path(self, path):
        local = pathlib.Path(super().translate_path(path))
        html = local.with_name(local.name + ".html")
        if not local.exists() and html.is_file():
            return str(html)
        return str(local)

    def list_directory(self, path):
        # Pages doesn't list folders; a folder without index.html is a missing page.
        self.send_error(404)
        return None

    def send_error(self, code, message=None, explain=None):
        page = ROOT / "404.html"
        if code != 404 or not page.is_file():
            return super().send_error(code, message, explain)
        body = page.read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Serving {ROOT} at http://localhost:{port}")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
