# lpezet.github.io

Personal site. Plain Jekyll on GitHub Pages — no theme gem, no build step, no
JavaScript beyond a 15-line theme toggle.

```
_config.yml               title, description, contact handles
_data/projects.yml        every project on the page  ← this is the file you edit
_data/breads.yml          every recipe on /breads/
_layouts/default.html     the whole page chrome
index.html                hero + the loop over _data/projects.yml
breads/index.html         standalone hobby page, own CSS, no layout
assets/css/style.css      hand-written CSS, light/dark via custom properties
assets/images/            screenshots
```

## The breads page

`breads/index.html` is deliberately not part of the layout — it keeps its own
serif/paper styling and a self-contained `<style>` block, and only borrows two
things from the site: the `~/Luke Pezet` bar back to the home page and the
`localStorage['theme']` key, so the light/dark choice carries across. It's
linked once from the low-key "Off the clock" section at the bottom of
`index.html` and is intentionally absent from the nav.

The recipes come from `_data/breads.yml`; everything else on that page — the
conversion table, the "where to start" cards, the closing lists — is plain HTML
in the template, because only the recipes repeat. Recipe numbers are generated
from position, so inserting one renumbers the rest.

Each recipe has a `historical` and a `kitchen` block, and each block is an
ordered list of single-key nodes — `p`, `warn`, `steps`, `text`, `note`,
`subhead`, `form` — so a recipe can mix prose, a formula and a caveat box in
whatever order it needs. The header comment in the file has the details.

```yaml
- name: Ötzi's cracker
  date: c. 3300 BC · South Tyrol
  prov: Reconstructed from the Iceman's gut contents.
  historical:
    - p: Einkorn bran dominates the cereal residue.
  kitchen:
    - form:
        rows:
          - { item: Einkorn wholemeal, amount: 200 g · 100% }
        total: { item: Six crackers, amount: 312 g }
    - steps: [Mix and knead 60 seconds., Roll to 2–3 mm.]
    - note: No salt and no leaven — neither is evidenced.
  swap: <b>Einkorn</b> <span class="arrow">→</span> <b>einkorn.</b>
```

## Adding a project

Add an entry under the right group in `_data/projects.yml`. Nothing else needs
to change — `index.html` renders whatever is in there, and the nav is built from
the group titles.

```yaml
- name: Thing
  tagline: One line, shown under the name.
  goal: What it's for and why it exists.
  challenge: The interesting hard part. Optional, but it's the best field here.
  tech: [TypeScript, Docker]
  status: live            # optional — also "in progress"
  image: /assets/images/thing.png   # optional
  links:
    - label: thing
      url: https://github.com/lpezet/thing
```

For private work, set `private: true` and **omit `links` entirely** — the card
renders a "private project" badge and a no-link note instead.

`goal` and `challenge` are rendered as HTML, not escaped, so `<code>`,
`<strong>` and `<em>` work inline. Keep it to those three — anything more
belongs in the layout.

## Adding a group

Append to `groups:` in the same file with an `id`, a `title`, and optionally a
`period` and `blurb`. The `id` becomes the anchor and the nav entry.

## Previewing locally

With Ruby, the real thing:

```bash
bundle exec jekyll serve   # or: jekyll serve
```

Without Ruby, `preview.py` is a ~150-line stand-in that renders the site into
`_site/` and serves it, rebuilding on every page request so a browser reload is
all you need:

```bash
pip install pyyaml python-liquid
python3 preview.py --serve          # http://127.0.0.1:8765
python3 preview.py                  # build only
```

It implements just the Liquid filters this site uses (`relative_url`,
`absolute_url`, `slugify`, `strip_newlines`) and it is a review aid, not a build
step — GitHub Pages still builds the published site with Jekyll, and where the
two disagree, Jekyll is right.

Section backgrounds alternate by position, so reordering groups reshuffles which
ones are tinted. That's cosmetic.
