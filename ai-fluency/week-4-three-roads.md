# Week 4 · Three Roads — Choose Your Stack with AI

## The constraints I gave the AI

```
- Free only: no hosting, domain, or tool that asks for a card.
- My honest skill level: beginner-to-intermediate; I can edit HTML/CSS and
  follow a template, I cannot maintain a server.
- What the portfolio must do (sitemap + content map pasted): 4 pages —
  landing with a proof strip, case studies with image galleries and
  before/after screenshots, about, contact form that emails me.
- How the work must be displayed: large image galleries, side-by-side
  before/after pairs, stat cards with numbers, one long-form case write-up.
  Nothing needs to be dynamic yet — no logins, no database, no comments.
```

## The three options the AI laid out (simplest → most powerful)

1. **Plain HTML/CSS on GitHub Pages** — hand-written or template-based static
   site, free hosting, no build step, no backend. Trade-off: everything is
   manual (edit a file, commit, it deploys); galleries are static markup.
2. **Static site generator (Eleventy or Astro) + GitHub Pages** — components
   and layouts so I write content, not duplicated HTML; still no backend.
   Trade-off: a build step and a toolchain to learn and maintain.
3. **Next.js / Vercel** — full framework, server functions, forms that post
   to an API. Trade-off: a backend exists (even if small), more to learn,
   more to maintain, and free-tier limits to mind.

## Pressure test on the front-runner

- *What breaks if I pick the simplest?* The contact form can't store to a
  database — but a `mailto:` fallback covers it, and the one action is an
  email anyway. Galleries are static but the content is fixed. Nothing breaks.
- *What do I maintain if I pick the most powerful?* A Node toolchain, a
  framework that changes yearly, Vercel free-tier limits, and a server I'd
  have to think about at 2 a.m. For four static pages.
- *Can I finish in two weeks?* Simplest: yes — the build week is mostly
  writing content and arranging images.
- *Does it show my work the way it needs?* Image galleries and side-by-side
  before/after pairs are plain HTML/CSS; the stat cards are the kit's colors.
  Yes.

## The decision — in my own words

**Chosen: plain HTML/CSS on GitHub Pages.**

The two I didn't choose, and why: **Eleventy/Astro** — real power, but a
toolchain I'd have to keep alive for four pages; the value shows up when a
site has dozens of pages, and mine has four. **Next.js/Vercel** — a backend
I don't need yet; the honest answer to "does anything have to be dynamic?" is
*no*, so a server is pure maintenance cost.

The decisive question was **"can I maintain this?"** — GitHub Pages deploys
itself on every push, there is nothing to run, nothing to update, and it
cannot break overnight. And **"does it show my work well?"** — image
galleries, before/after pairs, and stat cards are exactly what static HTML
does best. When (if) the portfolio needs a real form backend or a CMS, the
next road is one repo migration away — and by then I'll have earned the
toolchain.

The backend question, answered honestly: **not yet.**