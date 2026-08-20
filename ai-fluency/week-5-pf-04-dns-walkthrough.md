# Week 5 · PF-04 — DNS Walkthrough (in my own words)

Site: **https://ahmedshahin2345.github.io/** — a GitHub Pages site. This is
the whole walkthrough, written so a non-technical teammate can follow it.

## What DNS actually is

DNS (Domain Name System) is the phonebook of the internet. Computers
talk to each other using numbers called IP addresses — for example
`185.199.108.153` is one of GitHub Pages' servers. But nobody wants to
type a string of numbers, so we give websites names like
`ahmedshahin2345.github.io`. DNS is the system that maps the name to the
number, millions of times a second, all over the world.

## What happens when you type my URL

1. **Your browser asks a resolver.** The first thing your browser needs
   is "what IP address does `ahmedshahin2345.github.io` point to?" It
   sends that question to a **resolver** — a server run by your internet
   provider (or a service like 1.1.1.1) whose only job is to answer DNS
   questions. A resolver remembers recent answers (caching), so if
   someone nearby asked the same question a minute ago, it can answer
   instantly without going anywhere.

2. **The resolver asks the nameservers.** If the answer isn't cached, the
   resolver goes on a short trip:
   - It asks the **root nameservers** (the top of the phonebook): "who
     manages `.io`?" They point to the `.io` registry's nameservers.
   - It asks the `.io` nameservers: "who manages `github.io`?" They point
     to GitHub's nameservers.
   - It asks **GitHub's nameservers** — the actual "record holders" for
     this domain — "what is the address of
     `ahmedshahin2345.github.io`?" They answer with an **A record**: the
     IP address of GitHub's Pages server, plus a few alternates.

3. **The record comes back, the browser connects.** The resolver hands
   the IP to your browser. Your browser opens a direct connection to that
   server, sends "give me the page for `/`", the server responds with my
   `index.html`, and the page renders. HTTPS is automatic on GitHub
   Pages: the browser and server also agree on encryption before any
   content moves, which is why the URL is `https://` with the little padlock.

So: **resolver → root → registry → host's nameservers → record → browser
connects.** Most of that trip happens in a few milliseconds because every
step caches aggressively.

## What a CNAME record is

A CNAME record is an alias: "this name is actually another name." If I
one day buy `ahmedshahin.com` and want it to show my GitHub Pages site,
my domain provider would add:

```
ahmedshahin.com  CNAME  ahmedshahin2345.github.io
```

Anyone typing `ahmedshahin.com` would be told "go look up
`ahmedshahin2345.github.io` instead" — and the DNS phonebook then
resolves that name to the real IP. The site keeps living on GitHub Pages
(where hosting and HTTPS stay free) while my own name sits in front of it.
I did not buy a domain for this assignment; the `*.github.io` name is the
free URL that is already "clean enough for a CV" — it's my name, not
`spontaneous-kitten-3f21`.

## Why I can explain every file on the deployed site

The site is three files, all of which I wrote:

| File | What it does |
|---|---|
| `index.html` | The whole page — one file, inline CSS. Fonts come from Google Fonts, colors from my identity kit, structure from my through-line content map. |
| `hero-texture.svg` | Hand-built SVG noise tile in the kit's teal; gives the hero background texture without competing with the headline. |
| `as-monogram.svg` | The AS monogram from my identity kit — favicon and nav mark. |

GitHub Pages serves exactly this folder over HTTPS; there is no server
code, database, or build step to misunderstand.

## What the page contains

Who I am and my one-line claim ("I turn campus energy into sponsor-ready
ROI"), proof strip with real campaign numbers, two featured case cards
(SU Ticket Sales, AUC Welcome Party), the FlyRank internship build strip
with a GitHub link, my process (measure → translate → execute), a journal
slot for future posts and the capstone badge, and contact links (email,
LinkedIn, GitHub; CV and booking link land with the capstone update).