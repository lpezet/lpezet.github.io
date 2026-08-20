# lpezet.github.io

Personal site. Plain Jekyll on GitHub Pages — no theme gem, no build step, no
JavaScript beyond a 15-line theme toggle.

```
_config.yml               title, description, contact handles
_data/projects.yml        every project on the page  ← this is the file you edit
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

Needs Ruby:

```bash
bundle exec jekyll serve   # or: jekyll serve
```

Section backgrounds alternate by position, so reordering groups reshuffles which
ones are tinted. That's cosmetic.
