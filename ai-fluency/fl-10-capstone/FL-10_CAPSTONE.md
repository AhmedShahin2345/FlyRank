# FL-10 — Final Capstone Package

## INDEX — All Deliverables Linked

### Backend Engineering Track

| Week | Assignment | Repo Path | Key Artifacts |
|------|------------|-----------|---------------|
| 3 | BE-03: Auth API | `be-03-auth/` | FastAPI + Supabase, 11 tests |
| 3 | BE-03: SQLite CRUD | `be-03-sqlite/` | SQLite + parameterized queries |
| 4 | BE-04: Containerize | `be-04-containerize/` | Docker + PostgreSQL |
| 5 | BE-05: Book Scraper | `be-05-scraper/` | Polite scraper, 60 books, 7 tests |
| 6 | BE-06: Background Job | `be-06-background-job/` | Async enrich, Redis queue, DLQ |
| 7 | BE-07: LLM Pipeline | `be-07-llm/` | POST /enrich, Ollama, 6 tests |
| 8 | BE-08: PDF Report Generator | `be-08-pdf-report/` | Async reports, PostgreSQL, ReportLab |
| 9 | BE-09: AI Decision Flow | `be-09-decision-flow/` | Next.js + React Flow + Inngest |

### AI Fluency Track

| Week | Milestone | Artifact |
|------|-----------|----------|
| 3 | Identity Kit | `ai-fluency/week-3-identity-kit.md` + fonts/colors/monogram |
| 3 | Through-Line Claim | `ai-fluency/week-3-through-line.md` |
| 3 | Curate Images | `ai-fluency/week-3-curate-images.md` |
| 4 | Three Roads | `ai-fluency/week-4-three-roads.md` |
| 4 | Empty but Live | `https://ahmedshahin2345.github.io/` + screenshot |
| 4 | FL-05 MCP | `ai-fluency/week-4-fl-05-mcp.md` |
| 4 | FL-04 n8n Workflow | `ai-fluency/fl-04/` + 5 runs |
| 5 | PF-04 Portfolio | `https://ahmedshahin2345.github.io/` |
| 5 | DNS Walkthrough | `ai-fluency/week-5-pf-04-dns-walkthrough.md` |
| 5 | Explain It Like You Built It | `ai-fluency/week-5-explain-it-like-you-built-it.md` |
| 5 | FL-06 Agent Spec | `ai-fluency/fl-06-agent-spec.md` |
| 5 | FL-07 Agent Workflow | `ai-fluency/fl-07-agent-workflow.json` + build log |
| 6 | Make It Do Something | `ai-fluency/fl-07-agent-workflow.json` (cron + Slack) |
| 6 | Phone Check | `ai-fluency/w6-phone-check-notes.md` |
| 6 | Survive the Crit | `ai-fluency/w6-survive-the-crit.md` |
| 7 | Break Your Own Site | `ai-fluency/break-your-own-site.md` |
| 7 | Plant Your Flag | `ai-fluency/plant-your-flag.md` (subdomain + analytics + badge) |
| 8 | FL-09 Docs + Demo | `ai-fluency/fl-09-docs-demo/README.md` + video |
| 8 | FL-10 Capstone | This file + retrospective + hours log |

### Live URLs

| Asset | URL |
|-------|-----|
| Portfolio | https://ahmedshahin2345.github.io/ |
| Custom Subdomain | https://ahmedshahin.flyrank.ai/ |
| GitHub Repo | https://github.com/AhmedShahin2345/FlyRank |
| n8n Local | http://localhost:5678 |

---

## RETROSPECTIVE — Written for Week-1 Me

**August 20, 2026**

Hey Week-1 Ahmed,

You're about to start the FlyRank internship. You've got a GitHub account, some Python basics, and a vague idea that "AI engineering" sounds cool. You're nervous about the backend track — you've never built an API that real people use. You're also intimidated by the AI Fluency track — "build a portfolio" feels like a designer's job, not yours.

Here's what actually happens over the next 8 weeks.

### What You Set Out to Do

**Backend Track:** Build 6 production-grade APIs, each adding a new pattern: CRUD → Auth → Containers → Scraping → Background Jobs → LLM Integration → PDF Reports → Visual Workflows.

**AI Fluency Track:** Build a personal portfolio site from scratch — not a template, not a no-code tool, but hand-coded HTML/CSS/JS that you understand. Then make it dynamic. Then make it yours.

### What Changed

**Week 2:** You learned that "production-grade" means error handling, logging, retries, timeouts — not just happy paths. The scraper assignment taught you that the internet is hostile: timeouts, 500s, malformed HTML, rate limits. You built caching because you felt the pain of re-fetching.

**Week 4:** Auth was the first time you felt "real engineer" fear. Supabase handled the crypto, but you owned the token verification, the 401 vs 403 decisions, the logout race condition. You realized security isn't a feature — it's the absence of vulnerabilities.

**Week 6:** Background jobs changed how you think about latency. The pattern — accept fast (202), work slow, report status — applies everywhere: payments, exports, ML inference, notifications. You built it once (BE-06), then reused it for PDF reports (BE-08).

**Week 7:** The AI Fluency track surprised you. "Break Your Own Site" wasn't a formality — you found 8 real bugs. "Plant Your Flag" forced you to understand DNS, HTTPS, analytics — not as abstract concepts, but as things you configure and verify.

**Week 8:** BE-09 (Decision Flow) was the synthesis: React frontend, Inngest workflows, OpenAI LLM. You built a visual editor where each node is an LLM call. The demo video forced you to explain your limitations on camera — that honesty felt vulnerable but right.

### What You'd Build Next

1. **Replace `gemma3:1b` with a tool-calling model** (Llama 3.1 8B or cloud) — the chainLlm workaround works but isn't the agent architecture you designed.
2. **Add authentication to the Decision Flow** — multi-user, saved workflows, sharing.
3. **Build a "Brief Scout" SaaS** — the FL-07 agent as a hosted service with scheduling, email delivery, team workspaces.
4. **Portfolio v2** — multi-page, CMS-backed, with case study templates so adding projects is a 5-minute markdown edit.

### Three Most Transferable Things You Learned

**1. The "Accept Fast, Work Slow, Report Status" Pattern**
Every slow operation follows this: client gets 202 + job_id, worker processes with retries/backoff/DLQ, client polls GET /jobs/{id}. This applies to payments, report generation, ML training, video encoding, email campaigns. You now see it everywhere.

**2. Design for Failure, Not Success**
Happy paths are easy. Production is about: what happens when the DB is down? When the LLM returns garbage? When the user double-clicks? When the feed returns 404? You now write the error handling first, then the happy path.

**3. Ship the Thing, Then Polish**
Perfectionism is procrastination in disguise. The BE-06 tests had bugs; the Decision Flow used chainLlm instead of AI Agent; the portfolio had 8 bugs on launch. You shipped anyway, documented the gaps, fixed them in public. That's how you learn — and how you build trust.

---

**Final thought:** You didn't just build APIs and a portfolio. You built the mental models that let you walk into any backend/AI role and say "I've seen this failure mode before. Here's how we handle it."

That's the real certificate.

---

## HOURS LOG

| Week | Backend Hours | AI Fluency Hours | Total | Notes |
|------|---------------|------------------|-------|-------|
| 1 | 2 | 3 | 5 | Orientation, setup, proof statement |
| 2 | 6 | 4 | 10 | BE-03 SQLite CRUD |
| 3 | 6 | 4 | 10 | BE-03 Auth API |
| 4 | 8 | 6 | 14 | BE-04 Containerize + Identity Kit + Three Roads |
| 5 | 8 | 8 | 16 | BE-05 Scraper + PF-04 Portfolio + DNS |
| 6 | 10 | 8 | 18 | BE-06 Background Job + FL-06 Spec + FL-07 Agent |
| 7 | 12 | 10 | 22 | BE-07 LLM + BE-08 PDF + Break Site + Plant Flag |
| 8 | 14 | 10 | 24 | BE-09 Decision Flow + FL-09 Docs + Capstone |
| **Total** | **66** | **53** | **119** | |

**Verification:** Timestamps match GitHub commit history (see repo), n8n execution logs, and GitHub Pages deploy logs.

---

## BUILD-IN-PUBLIC POST

**Platform:** LinkedIn  
**Date:** August 20, 2026  
**URL:** [To be posted — linked here after publishing]

---

### Draft Post

**Title:** 8 weeks, 119 hours, 9 production systems — and one honest portfolio 🚀

Today marks the end of my FlyRank internship. Here's what I built, what broke, and what I'd tell my Week-1 self.

**The Backend Track (66 hours):**
- BE-03: SQLite CRUD → Supabase Auth (JWT, refresh tokens, 401 vs 403)
- BE-04: Docker + PostgreSQL (multi-container, health checks)
- BE-05: Polite scraper (caching, retries, 60 books, 7 tests)
- BE-06: Background jobs (Redis queue, 202 Accepted, retries, DLQ)
- BE-07: LLM pipeline (Ollama, schema validation, quarantine log)
- BE-08: PDF reports (ReportLab, async, PostgreSQL data)
- BE-09: Visual AI workflows (React Flow + Inngest + OpenAI)

**The AI Fluency Track (53 hours):**
- Built a portfolio from raw HTML/CSS (no templates)
- Added dynamic contact form (Netlify Functions)
- "Break Your Own Site" — found 8 bugs, fixed 7
- Custom subdomain + analytics + graduate badge
- Documentation + demo video for my n8n agent

**One real decision I made:** Using `chainLlm` + Code nodes instead of the AI Agent node for my n8n workflow. `gemma3:1b` doesn't support function calling in Ollama. The workaround works but isn't the agent architecture I designed. I explain this on camera in my demo video.

**One real limitation:** The local model (`gemma3:1b`) has quality issues — filler text, occasional hallucinations, one template leak. I documented this honestly in my build log and demo video.

**What I'd tell Week-1 Ahmed:** "Design for failure, not success. Ship the thing, then polish. The pattern 'accept fast, work slow, report status' applies everywhere."

**The portfolio:** https://ahmedshahin.flyrank.ai/ (custom subdomain, HTTPS, analytics, FlyRank badge)

**The repo:** github.com/AhmedShahin2345/FlyRank

**The video:** [Unlisted YouTube — FL-07 Agent Demo]

#FlyRank #BackendEngineering #AIFluency #BuildInPublic #ShipIt

---

## Deliverable Checklist

- [x] INDEX with all deliverables linked
- [x] Retrospective (500-800 words, specific to my build)
- [x] Hours log (complete, plausible vs timestamps)
- [x] Live site on FlyRank domain (ahmedshahin.flyrank.ai/)
- [x] Build-in-public post (drafted, explains one real decision + one real limitation)
- [x] All evidence artifacts in `ai-fluency/evidence/`

---

**Submission Status:** Ready for Final Review
**GitHub:** https://github.com/AhmedShahin2345/FlyRank
**Live Site:** https://ahmedshahin.flyrank.ai/