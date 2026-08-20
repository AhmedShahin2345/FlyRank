# FL-10 Build-in-Public Post

## Platform: LinkedIn
## Date: August 20, 2026
## Status: Draft — To be published after final review

---

### Post Content

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

### Supporting Assets

| Asset | Status |
|-------|--------|
| Portfolio screenshot | `ai-fluency/evidence/plant-your-flag-social.png` |
| Analytics screenshot | `ai-fluency/evidence/plant-your-flag-analytics.png` |
| Badge visible | `ai-fluency/evidence/plant-your-flag-badge.png` |
| Demo video | Unlisted YouTube (link in repo) |

---

### Engagement Strategy

1. **Tag:** @FlyRank, @n8n_io, @OllamaAI
2. **Hashtags:** #FlyRank #BackendEngineering #AIFluency #BuildInPublic #ShipIt
3. **Comment seed:** Reply to own post with link to GitHub repo and demo video
4. **Engage:** Respond to every comment within 24 hours

---

### One Real Decision (Explained)

**Decision:** Used `chainLlm` + Code nodes instead of AI Agent node in n8n workflow.

**Why:** `gemma3:1b` (815MB) is the only model that fits in local RAM. It doesn't support function calling in Ollama's registry. The AI Agent node validates this at startup and errors.

**Trade-off:** Lost the clean agent architecture (model decides which tool to call). Gained a working system with real HTTP + real file I/O via Code nodes.

**Lesson:** Constraints force creativity. The workaround is uglier but ships.

---

### One Real Limitation (Honest)

**Limitation:** `gemma3:1b` output quality is mediocre.

**Evidence:** 
- Filler preambles ("Here is your brief based on the feed...")
- Occasional hallucinated references (TikTok, Instagram in retail briefs)
- One run leaked template syntax (`{{ $json.topic }}`)

**Mitigation:** Documented in build log, eval results, and demo video. Next step: Llama 3.1 8B (4.7GB) or cloud API.

---

### Why This Post Matters

Build-in-public isn't performative — it's accountability. Saying "here's what I built, here's what's broken" forces you to be honest with yourself. And it lets others learn from your actual scars, not your highlight reel.

The portfolio isn't perfect. The APIs have known limitations. The demo video shows the warts. That's the point.

**Here's the link to the thing I built:** https://ahmedshahin.flyrank.ai/

---

**Built with n8n + Ollama + React Flow + Inngest + ReportLab + FastAPI + Claude.**  
I designed, debugged, documented, and deployed every piece.  
Claude assisted with: prompt phrasing, JSON-LD schemas, docker-compose files, README structure.

#FlyRank #BackendEngineering #AIFluency #BuildInPublic #ShipIt