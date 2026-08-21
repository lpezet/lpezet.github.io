#!/usr/bin/env python3
"""A tiny Jekyll stand-in, so the site can be reviewed without Ruby.

Renders every .html page with front matter into ./_site (same directory
Jekyll uses, already gitignored) and optionally serves it.

    python3 preview.py             # build once
    python3 preview.py --serve     # build, then serve on :8765 and rebuild
                                   # on every page request

It implements only the handful of Liquid filters this site actually uses.
It is a review aid, not a build step — GitHub Pages still builds the real
thing with Jekyll, and that remains the authority.

Needs: pip install pyyaml python-liquid
"""
import argparse
import functools
import http.server
import os
import re
import shutil

import yaml
from liquid import Environment

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, "_site")

FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)

env = Environment()
env.filters["relative_url"] = lambda v: str(v)
env.filters["absolute_url"] = lambda v: "https://lpezet.github.io" + str(v)
env.filters["slugify"] = lambda v: re.sub(r"[^a-z0-9]+", "-", str(v).lower()).strip("-")
env.filters["strip_newlines"] = lambda v: str(v).replace("\n", "")


def split_front_matter(text):
    """Return (front matter dict, body). A None dict means there was none."""
    m = FM.match(text)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def out_path(rel, permalink):
    if permalink:
        p = permalink.strip("/")
        return os.path.join(OUT, p, "index.html") if p else os.path.join(OUT, "index.html")
    return os.path.join(OUT, rel)


def url_for(rel, permalink):
    if permalink:
        return permalink
    return "/" if rel == "index.html" else "/" + rel


def build(quiet=False):
    site = yaml.safe_load(open(os.path.join(SRC, "_config.yml")))
    site["data"] = {}
    ddir = os.path.join(SRC, "_data")
    for f in sorted(os.listdir(ddir)):
        if f.endswith((".yml", ".yaml")):
            site["data"][os.path.splitext(f)[0]] = yaml.safe_load(open(os.path.join(ddir, f)))

    layouts = {}
    for f in os.listdir(os.path.join(SRC, "_layouts")):
        _, body = split_front_matter(open(os.path.join(SRC, "_layouts", f)).read())
        layouts[os.path.splitext(f)[0]] = env.from_string(body)

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))

    pages = []
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if not d.startswith(("_", ".")) and d != "assets"]
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, SRC)
            fm, body = split_front_matter(open(full).read())
            if fm is None:
                # No front matter: Jekyll copies it through untouched.
                dest = os.path.join(OUT, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy(full, dest)
                continue
            page = dict(fm)
            page.setdefault("url", url_for(rel, fm.get("permalink")))
            html = env.from_string(body).render(site=site, page=page)
            if fm.get("layout"):
                html = layouts[fm["layout"]].render(site=site, page=page, content=html)
            dest = out_path(rel, fm.get("permalink"))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "w").write(html)
            pages.append((page["url"], os.path.relpath(dest, OUT), len(html)))

    if not quiet:
        for url, dest, n in sorted(pages):
            print(f"  {url:<12} {n:>7} bytes  {dest}")
    return pages


class Handler(http.server.SimpleHTTPRequestHandler):
    """Rebuilds before serving a page, so a browser reload is enough."""

    def do_GET(self):
        if not os.path.splitext(self.path.split("?")[0])[1] or self.path.endswith(".html"):
            try:
                build(quiet=True)
            except Exception as e:      # keep serving the last good build
                print(f"  build failed: {e}")
        super().do_GET()

    def log_message(self, fmt, *args):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--serve", action="store_true", help="serve _site after building")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    print(f"building -> {OUT}")
    build()
    if not args.serve:
        return
    handler = functools.partial(Handler, directory=OUT)
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as httpd:
        print(f"serving  -> http://127.0.0.1:{args.port}/   (ctrl-c to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
