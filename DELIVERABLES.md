# FlyRank Internship — All Deliverables (Ahmed Shahin)

## Overview & Quick Links
- **GitHub Repository**: https://github.com/AhmedShahin2345/FlyRank
- **Live Portfolio**: https://ahmedshahin2345.github.io/
- **Local Automation Engine (n8n)**: `http://localhost:5678`
  - FL-04 Webhook: `/webhook/brief`
  - FL-07 / W6 Webhook: `/webhook/brief-agent`
- **Updated CV (with Portfolio Link)**: [`CV_Ahmed_Shahin.pdf`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/CV_Ahmed_Shahin.pdf) / [`docs/CV_Ahmed_Shahin.pdf`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/docs/CV_Ahmed_Shahin.pdf)

---

## Backend Engineering Track

| Assignment | Repo Path | Description / Live Endpoint | Status |
|---|---|---|---|
| **BE-03: Auth API** | [`be-03-auth/`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/be-03-auth/) | FastAPI + Supabase Auth (`/auth/signup`, `/auth/login`, `/auth/logout`, `/protected/profile`, `/protected/dashboard`), 11 automated pytest tests passing | ✅ Complete & Tested |
| **BE-03: SQLite CRUD** | [`be-03-sqlite/`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/be-03-sqlite/) | SQLite backend with schema migrations and parameterized SQL queries | ✅ Complete |
| **BE-04: Containerize** | [`be-04-containerize/`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/be-04-containerize/) | Docker & Docker Compose setup for PostgreSQL and FastAPI service | ✅ Complete |
| **BE-05: Book Scraper** | [`be-05-scraper/`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/be-05-scraper/) | Polite web scraper with caching, schema normalization (60 books), 7 pytest tests passing | ✅ Complete & Tested |
| **BE-07: LLM Pipeline** | [`be-07-llm/`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/be-07-llm/) | `POST /enrich` endpoint backed by Ollama `gemma3:1b` with retry policies, quarantine log, 6 pytest tests passing | ✅ Complete & Tested |

---

## AI Fluency Track

| Week | Milestone / Assignment | Repo Path / URL | Evidence / Artifacts | Status |
|---|---|---|---|---|
| **W3** | Identity Kit | [`ai-fluency/identity/`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/identity/) | [`week-3-identity-kit.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/week-3-identity-kit.md), fonts, colors, monogram SVG | ✅ Complete |
| **W3** | Through-Line Claim | [`ai-fluency/week-3-through-line.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/week-3-through-line.md) | Claim + Content Strategy Map | ✅ Complete |
| **W4** | Three Roads Exploration | [`ai-fluency/week-4-three-roads.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/week-4-three-roads.md) | Three design variants evaluation | ✅ Complete |
| **W4** | Empty but Live Site | https://ahmedshahin2345.github.io/ | [`ai-fluency/evidence/empty-but-live.png`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/evidence/empty-but-live.png) | ✅ Complete |
| **W4** | FL-05: MCP Server Integration | [`ai-fluency/week-4-fl-05-mcp.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/week-4-fl-05-mcp.md) | Filesystem MCP server registered (3 real tool calls) | ✅ Complete |
| **W4** | FL-04: n8n Brief Workflow | [`ai-fluency/fl-04/`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/fl-04/) | [`week-4-fl-04-workflow.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/week-4-fl-04-workflow.md), 5 runs (`run1.json` - `run5.json`), canvas screenshot | ✅ Complete |
| **W5** | PF-04: Live Portfolio Site | https://ahmedshahin2345.github.io/ | [`ai-fluency/evidence/pf-04-live.png`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/evidence/pf-04-live.png) | ✅ Complete |
| **W5** | DNS & Hosting Walkthrough | [`ai-fluency/week-5-pf-04-dns-walkthrough.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/week-5-pf-04-dns-walkthrough.md) | In-depth DNS / CNAME / A-record explainer | ✅ Complete |
| **W5** | Explain It Like You Built It | [`ai-fluency/week-5-explain-it-like-you-built-it.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/week-5-explain-it-like-you-built-it.md) | Systems reflection & architecture retrospective | ✅ Complete |
| **W5** | FL-06: Agent Specification | [`ai-fluency/fl-06-agent-spec.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/fl-06-agent-spec.md) | 5 evaluation test cases, platform trade-offs | ✅ Complete |
| **W5** | FL-07: Brief Scout Workflow | [`ai-fluency/fl-07-agent-workflow.json`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/fl-07-agent-workflow.json) | [`ai-fluency/fl-07-build-log.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/fl-07-build-log.md) (9 real failures documented & resolved) | ✅ Complete |
| **W6** | Make It Do Something (Scheduler + Slack) | [`ai-fluency/fl-07-agent-workflow.json`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/fl-07-agent-workflow.json) | Cron schedule trigger (Every Tue 09:00) + Slack webhook dispatch node | ✅ Complete |
| **W6** | Phone Check Review | [`ai-fluency/w6-phone-check-notes.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/w6-phone-check-notes.md) | 3 likes, 3 improvements, peer review action items | ✅ Complete |
| **W6** | Survive the Crit | [`ai-fluency/w6-survive-the-crit.md`](file:///var/folders/lw/ctqcqvdn3d10t2nfxp1__gxm0000gn/T/opencode/FlyRank/ai-fluency/w6-survive-the-crit.md) | Public critique collection, top 3 fixes implemented | ✅ Complete |

---

## Internship Portal Submission Mapping

| Portal Card | URL to Paste | Attachment to Upload |
|---|---|---|
| **BE-03 Auth API** | `https://github.com/AhmedShahin2345/FlyRank/tree/main/be-03-auth` | `be-03-auth/README.md` |
| **BE-05 Scraper** | `https://github.com/AhmedShahin2345/FlyRank/tree/main/be-05-scraper` | `be-05-scraper/output/run-report.json` |
| **BE-07 LLM API** | `https://github.com/AhmedShahin2345/FlyRank/tree/main/be-07-llm` | `be-07-llm/README.md` |
| **W3 Identity Kit** | `https://github.com/AhmedShahin2345/FlyRank/tree/main/ai-fluency/identity` | `ai-fluency/week-3-identity-kit.md` |
| **W3 Through-Line** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/week-3-through-line.md` | `ai-fluency/week-3-through-line.md` |
| **W4 Three Roads** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/week-4-three-roads.md` | `ai-fluency/week-4-three-roads.md` |
| **W4 Empty but Live** | `https://ahmedshahin2345.github.io/` | `ai-fluency/evidence/empty-but-live.png` |
| **W4 FL-05 MCP** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/week-4-fl-05-mcp.md` | `ai-fluency/evidence/mcp-evidence.png` |
| **W4 FL-04 Workflow** | `https://github.com/AhmedShahin2345/FlyRank/tree/main/ai-fluency/fl-04` | `ai-fluency/week-4-fl-04-workflow.md` |
| **W5 PF-04 Portfolio** | `https://ahmedshahin2345.github.io/` | `ai-fluency/evidence/pf-04-live.png` |
| **W5 DNS Walkthrough** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/week-5-pf-04-dns-walkthrough.md` | `ai-fluency/week-5-pf-04-dns-walkthrough.md` |
| **W5 Explain It Like You Built It** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/week-5-explain-it-like-you-built-it.md` | `ai-fluency/week-5-explain-it-like-you-built-it.md` |
| **W5 FL-06 Agent Spec** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/fl-06-agent-spec.md` | `ai-fluency/fl-06-agent-spec.md` |
| **W5 FL-07 Agent Workflow** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/fl-07-agent-workflow.json` | `ai-fluency/fl-07-build-log.md` |
| **W6 Make It Do Something** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/fl-07-agent-workflow.json` | `ai-fluency/fl-07-agent-workflow.json` |
| **W6 Phone Check** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/w6-phone-check-notes.md` | `ai-fluency/w6-phone-check-notes.md` |
| **W6 Survive the Crit** | `https://github.com/AhmedShahin2345/FlyRank/blob/main/ai-fluency/w6-survive-the-crit.md` | `ai-fluency/w6-survive-the-crit.md` |

