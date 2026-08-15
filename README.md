# lpezet.github.io

Personal site. Plain Jekyll on GitHub Pages — no theme gem, no build step, no
JavaScript beyond a 15-line theme toggle.

```
_config.yml               title, description, contact handles
_data/projects.yml        every project on the page  ← this is the file you edit
_layouts/default.html     the whole page chrome
index.html                hero + the loop over _data/projects.yml
assets/css/style.css      hand-written CSS, light/dark via custom properties
assets/images/            screenshots
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

`goal` and `challenge` are rendered as HTML, not escaped, so `<code>` and
`<strong>` work inline. Keep it to those two — anything more belongs in the
layout.

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
