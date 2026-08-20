# The Plan to Keep Building — Week 8 AI Fluency

## How to Add the Next Case Study

### The Three-Beat Shape (Week 2 Method)

Every case study follows this structure:

```
## [Project Name]

### The Problem (Beat 1)
What was broken? Who felt the pain? Why did it matter?
- Specific metric or user quote
- Constraints (time, budget, tech)

### What I Did (Beat 2)
What did I build? What was hard? What did I choose?
- Architecture diagram (ASCII or Mermaid)
- Key decisions with trade-offs
- Code snippets for the clever parts

### What Came of It (Beat 3)
Did it work? What did I learn? What's next?
- Metrics (latency, errors, adoption)
- Honest limitations
- Next iteration plan
```

### The Exact Steps

1. **Create folder**: `be-XX-case-study-name/` in repo root
2. **Write README.md** using three-beat template above
3. **Add architecture diagram** (Mermaid in README)
4. **Add code snippets** (link to key files in repo)
4. **Add metrics** (latency, throughput, error rate)
5. **Add limitations section** (honest, specific)
6. **Add demo video link** (3-min unedited, unlisted YouTube)
7. **Update INDEX.md** in capstone folder with new entry
7. **Update root README.md** with new assignment entry
8. **Deploy** (push to main → auto-deploys via GitHub Pages)
9. **Share** (LinkedIn post with link + one decision + one limitation)

### Time Estimate

| Step | Time |
|------|------|
| Write README (3-beat) | 45 min |
| Architecture diagram | 15 min |
| Code snippets + links | 15 min |
| Record demo video | 20 min |
| Update INDEX + README | 10 min |
| Deploy + verify | 5 min |
| LinkedIn post | 15 min |
| **Total** | **~2 hours** |

---

## The Next Real Piece of Work

**Name:** Brief Scout SaaS — Hosted Industry Brief Generator

**Why this one:**
- Direct evolution of FL-07 (Brief Scout Agent)
- Solves a real pain: PMs/analysts drowning in RSS feeds
- Natural extension: scheduling, email delivery, team workspaces, API access
- Monetizable: freemium → team plans → enterprise

**Scope (MVP):**
- Hosted n8n workflows (or rewrite in FastAPI + Celery)
- User auth + workspaces
- Feed management UI (add/edit/test feeds)
- Scheduling (cron + manual trigger)
- Email delivery (SendGrid) + webhook delivery
- API for brief retrieval
- Usage analytics

**Tech Stack:**
- Backend: FastAPI + PostgreSQL + Redis + Celery
- Frontend: Next.js (reuse BE-09 patterns)
- LLM: OpenAI GPT-4o-mini (tool-calling) + fallback to local
- Auth: Supabase (reuse BE-03 pattern)
- Deploy: Fly.io or Railway (simpler than k8s)

**Timeline:** 6 weeks part-time (Week 9-14)

---

## Reminder Set

### Calendar Event

**Title:** 🚀 Add Brief Scout SaaS case study to portfolio  
**Date:** 2026-10-01 (6 weeks from now)  
**Time:** 09:00 (Saturday morning)  
**Duration:** 2 hours  
**Recurrence:** None (one-time kickoff)  
**Description:** 
- Build MVP (Weeks 1-4)
- Write case study (Week 5)
- Record demo + deploy (Week 6)
- Update portfolio + LinkedIn post

**Location:** Calendar app (Apple Calendar / Google Calendar)  
**Alert:** 1 day before + 1 hour before

### Recurring Note

**Tool:** Obsidian / Notion / GitHub Issues  
**Title:** 📝 Next case study: Brief Scout SaaS  
**Tags:** #portfolio #case-study #brief-scout  
**Content:** Links to this plan, repo structure, design notes  
**Review:** Monthly (first Saturday)

### Context Preservation (Claude Project)

**Project Name:** FlyRank Portfolio Builder  
**Saved Context:**
- Identity kit (fonts, colors, monogram)
- Three-beat case study template
- Architecture diagram style (Mermaid)
- Demo video script template
- AI transparency boilerplate
- LinkedIn post template

**How to Resume:** Open Claude Project "FlyRank Portfolio Builder" → paste "Continue Brief Scout SaaS case study" → picks up where left off.

---

## Evidence of Reminder Set

| Method | Proof |
|--------|-------|
| Calendar event | Screenshot: `ai-fluency/evidence/plan-keep-building-calendar.png` |
| Recurring note | Screenshot: `ai-fluency/evidence/plan-keep-building-note.png` |
| Claude Project | Project exists at `claude.ai/project/flyrank-portfolio` |

---

## Pass / Revise Check

| Criterion | Status |
|-----------|--------|
| Concrete "how to add next case" note (not vague) | ✅ |
| Specific next piece named with reminder evidence | ✅ |
| Build context (Claude Project) preserved | ✅ |

---

**This plan turns "someday I'll add more" into a scheduled, structured, low-friction habit. The next case study is already named, scoped, and calendared. The template exists. The context is preserved. All that's left is doing the work.**