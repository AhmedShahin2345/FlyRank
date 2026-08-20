# W5 · Explain It Like You Built It

> A reflection on what I actually built, why it matters, and what I'd do differently.

---

## The Portfolio (PF-04)

**Live**: https://ahmedshahin2345.github.io/

**What I built**: A single-page portfolio that leads with my one-line claim — *"I turn campus energy into sponsor-ready ROI"* — then proves it with real campaign numbers (SU ticket sales: 20% → 58% follow-to-purchase), two featured cases (SU Ticket Sales, AUC Welcome Party), the FlyRank internship builds (API, scraper, LLM endpoint, n8n workflow), my process (measure → translate → execute), and contact links.

**Why this design**:
- The claim comes from Week 1's proof statement, sharpened in Week 3's through-line work. It's not a role description; it's a transformation with a business result.
- One page, no fluff. The identity kit (Fraunces/Inter, teal/charcoal/cream/terracotta, AS monogram) runs through everything — hero texture, stat cards, card borders, CTA buttons.
- Every link is a real destination: GitHub repo, email, LinkedIn placeholder. CV and booking link are honest placeholders ("lands here with capstone update") — no fake links.
- Built as plain HTML + inline CSS (one file) so I understand every byte deployed. Hosted on GitHub Pages (free, HTTPS automatic, custom domain ready).

**What I'd change**:
- Add the real portrait (phone photo, plain wall) — currently a text placeholder.
- Replace stat-card numbers with dashboard screenshots once exported.
- Add the AUC Welcome Party photos (select 2 from event set).
- The DNS walkthrough (in `ai-fluency/week-5-pf-04-dns-walkthrough.md`) explains the infrastructure in non-technical language — I'd add a diagram if I had more time.

---

## The Agent (FL-06/FL-07) — Brief Scout

**Spec**: `ai-fluency/fl-06-agent-spec.md`  
**Workflow**: `ai-fluency/fl-07-agent-workflow.json` (adapted from FL-04)  
**Build log**: `ai-fluency/fl-07-build-log.md`

**What I built**: An n8n workflow triggered by webhook that:
1. Takes a topic (+ optional RSS URL)
2. Fetches & parses the feed (Code tool = real HTTP + XML parse)
3. Summarizes each item with local LLM (`gemma3:1b` via `chainLlm`)
4. Writes the brief to `~/Documents/FlyRank/briefs/<topic>-<date>.md` (Code tool = real file write)
5. Returns the brief text

**Why n8n**: Already running locally with Ollama; visual debugging; webhook + Code tools = real external data + real file write without custom server code.

**The deviation**: FL-06 spec'd an AI Agent node with ToolCode sub-nodes. `gemma3:1b` doesn't support function calling (Ollama registry says so). The AI Agent node errors at runtime. Instead, I used `chainLlm` + two Code nodes — still two real tools, still end-to-end, still satisfies FL-07 criteria.

**9 real failures fixed** (documented in build log):
1. Node type prefix (`@n8n/`)
2. Ollama credential + inline baseUrl
3. Webhook body under `$json.body`
4. Sub-node connection direction (source=sub-node, target=root)
5. IPv6 `::1` → use `127.0.0.1`
6. `chainLlm` outputs `{text}` not `{response}`
7. RSS uses `contentSnippet`, not `description`
8. Limit node needs `$('Input').first().json.max_items`
9. Webhook `responseNode` returns first array item → wrap in single object

**Model quality**: `gemma3:1b` is mediocre — filler preambles, occasional TikTok hallucinations, one literal `{{ $json.topic }}` leak. Documented honestly in FL-04 doc and build log. With a tool-capable model (qwen2.5:7b, llama3.1:8b) the AI Agent node would work; time-constrained.

---

## What This Taught Me

1. **Infrastructure isn't magic** — DNS, webhooks, credentials, IPv4 vs IPv6, response modes. The portfolio DNS walkthrough forced me to explain it to a non-technical person; that's when I actually understood it.
2. **Local models have hard limits** — `gemma3:1b` is fast and tiny but can't call tools. You don't get agent behavior without a tool-capable model. The spec must match the model.
3. **Visual workflow debugging beats console logs** — n8n's canvas + execution log let me see exactly which node failed and why. The 9 fixes above were all visible in the UI.
4. **Honest documentation > perfect output** — The FL-04 doc lists model failures; the build log lists 9 real bugs. That's more useful than a sanitized success story.
5. **One file you understand > framework you don't** — The portfolio is 300 lines of HTML/CSS. No build step, no framework, no mystery. Same for the n8n workflow: every node is visible, every connection traceable.

---

## What's Next (W6)

- **Make It Do Something**: Extend Brief Scout with a scheduler (cron trigger) and a Slack/email webhook so the brief posts automatically every Tuesday.
- **Phone check**: Call a peer, walk them through the portfolio + agent, get feedback.
- **Survive the Crit**: Publish both URLs, invite real critique, iterate.
- **Final link list + user checklist**: All deliverables in one place for portal submission.

---

## Links (all pushed to https://github.com/AhmedShahin2345/FlyRank)

| Assignment | Repo Path | Live / Evidence |
|---|---|---|
| BE-03 Auth API | `backend/be-03/` | Tests pass, Swagger at `/docs` |
| BE-05 Book Scraper | `backend/be-05/` | 60 books, idempotent, cached |
| BE-07 LLM Enrich | `backend/be-07/` | Eval 7/8, AI-rematch quarantined |
| W3 Identity Kit | `ai-fluency/identity/` | Fonts, colors, monogram, texture |
| W3 Through-Line | `ai-fluency/week-3-through-line.md` | Claim + content map + CTAs |
| W4 Three Roads | `portfolio/` (branch) | Three single-page variants |
| W4 Empty but Live | `https://ahmedshahin2345.github.io/` (v1) | Near-blank + kit |
| W4 FL-05 MCP | `ai-fluency/fl-05-mcp.md` | Filesystem MCP registered |
| W4 FL-04 n8n | `ai-fluency/fl-04/` | 5 runs, doc, evidence |
| W5 PF-04 Portfolio | `https://ahmedshahin2345.github.io/` (v2) | Full portfolio |
| W5 DNS Walkthrough | `ai-fluency/week-5-pf-04-dns-walkthrough.md` | Half-page, own words |
| W5 FL-06 Spec | `ai-fluency/fl-06-agent-spec.md` | 1–2 pages, 5 eval cases |
| W5 FL-07 Agent | `ai-fluency/fl-07-agent-workflow.json` | Working n8n workflow |
| W5 FL-07 Build Log | `ai-fluency/fl-07-build-log.md` | 9 failures + deviation |