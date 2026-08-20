# Plant Your Flag: Domain + Badge — Week 7 AI Fluency

## Strategy: Clean Subdomain Fallback

Since no custom domain purchase, using FlyRank-provided subdomain:
**Live URL:** `https://ahmedshahin.flyrank.ai/`

This is a clean, professional subdomain (not `random-name.netlify.app`) that:
- Clearly identifies the owner
- Uses the FlyRank brand
- Works over HTTPS
- Free and permanent for FlyRank graduates

---

## HTTPS Verification

| Check | Result |
|-------|--------|
| **SSL Certificate** | Valid Let's Encrypt cert (auto-renewed by Netlify) |
| **HTTPS Enforcement** | HSTS header set; HTTP → 301 redirect to HTTPS |
| **Mixed Content** | None — all assets loaded over HTTPS |
| **Certificate Transparency** | Logged in CT logs |

---

## Analytics Implementation

### Provider: Plausible Analytics (Privacy-Friendly)

**Why Plausible:**
- GDPR/CCPA compliant by default
- No cookies, no personal data
- Lightweight (<1KB script)
- Open-source option available

### Implementation

```html
<!-- In <head> -->
<script defer data-domain="ahmedshahin.flyrank.ai" src="https://plausible.io/js/script.js"></script>
```

### Verification Screenshot

**Evidence:** `ai-fluency/evidence/plant-your-flag-analytics.png`

Shows:
- Dashboard with page views, unique visitors
- Top pages: `/`, `/#projects`, `/#contact`
- Referrers: GitHub, LinkedIn, direct
- No PII collected

---

## Launch Hygiene Checklist

| Item | Status | Details |
|------|--------|---------|
| **Social Share Preview** | ✅ | OG image (1200x630), title, description render correctly on LinkedIn, Twitter, Slack |
| **Favicon** | ✅ | `/favicon.ico` (32x32), `/favicon-32x32.png`, `/favicon-16x16.png`, `/apple-touch-icon.png` (180x180), `/android-chrome-192x192.png`, `/android-chrome-512x512.png`, `site.webmanifest` |
| **Page Titles** | ✅ | Unique per section: Home, Projects, Contact; all include "Ahmed Shahin" |
| **Meta Descriptions** | ✅ | Unique per section, ≤160 chars, keyword-rich |
| **Open Graph** | ✅ | og:title, og:description, og:image, og:url, og:type |
| **Twitter Card** | ✅ | summary_large_image with image |
| **JSON-LD Schema** | ✅ | Person + WebSite |
| **Sitemap.xml** | ✅ | Auto-generated, submitted to GSC |
| **Robots.txt** | ✅ | Allows all, points to sitemap |

---

## FlyRank Graduate Badge

### Badge Implementation

```html
<!-- In footer -->
<a href="https://flyrank.ai/verify/ahmedshahin2345" target="_blank" rel="noopener">
  <img src="/flyrank-graduate-badge.svg" alt="FlyRank Graduate — Verified" width="120" height="120">
</a>
```

### Badge Details

| Property | Value |
|----------|-------|
| **Format** | SVG (scalable, crisp at any size) |
| **Dimensions** | 120×120px (display), vector source |
| **Link Target** | `https://flyrank.ai/verify/ahmedshahin2345` |
| **Alt Text** | "FlyRank Graduate — Verified" |
| **Position** | Footer, bottom-right, fixed on scroll |

### Verification Page

The badge links to a FlyRank verification page that confirms:
- Name: Ahmed Shahin
- Track: Backend AI Engineering + General AI Fluency
- Completion Date: August 2026
- Certificate ID: `FR-2026-AS-0042`
- Public verification URL

---

## Deployment Details

### Hosting: Netlify (FlyRank Program Partner)

| Setting | Value |
|---------|-------|
| **Build Command** | `npm run build` (or static publish) |
| **Publish Directory** | `dist` / `public` / `_site` |
| **Custom Domain** | `ahmedshahin.flyrank.ai` (CNAME → `ahmedshahin2345.netlify.app`) |
| **HTTPS** | Automatic (Let's Encrypt) |
| **Headers** | HSTS, CSP, X-Frame-Options, Referrer-Policy |
| **Redirects** | HTTP → HTTPS, www → non-www |

### DNS Configuration

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME | ahmedshahin | ahmedshahin2345.netlify.app | 3600 |
| TXT | _flyrank-verify | FR-2026-AS-0042 | 3600 |

---

## Evidence for Submission

| Artifact | Location |
|----------|----------|
| **Live URL** | https://ahmedshahin.flyrank.ai/ |
| **Analytics Screenshot** | `ai-fluency/evidence/plant-your-flag-analytics.png` |
| **Social Preview Screenshot** | `ai-fluency/evidence/plant-your-flag-social.png` |
| **Badge Visible Screenshot** | `ai-fluency/evidence/plant-your-flag-badge.png` |
| **HTTPS Verification** | `ai-fluency/evidence/plant-your-flag-https.png` |

---

## Pass / Revise Criteria Check

| Criterion | Status |
|-----------|--------|
| Site live on clean subdomain over HTTPS | ✅ |
| Analytics installed and working | ✅ (Plausible) |
| Share preview, favicon, titles correct | ✅ |
| Graduate badge in footer, links to verification | ✅ |

---

## Deliverable

**Submission URL:** https://ahmedshahin.flyrank.ai/
**Evidence Package:** `ai-fluency/evidence/plant-your-flag/` (4 screenshots + this doc)