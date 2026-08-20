# FL-10 Retrospective

## Written for Week-1 Me

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
Every slow operation follows this: client gets 202 + job_id, worker processes with retries/backoff/DLQ, client polls GET /jobs/{id}. This applies to payments, report generation, ML training, video encoding, notifications. You now see it everywhere.

**2. Design for Failure, Not Success**
Happy paths are easy. Production is about: what happens when the DB is down? When the LLM returns garbage? When the user double-clicks? When the feed returns 404? You now write the error handling first, then the happy path.

**3. Ship the Thing, Then Polish**
Perfectionism is procrastination in disguise. The BE-06 tests had bugs; the Decision Flow used chainLlm instead of AI Agent; the portfolio had 8 bugs on launch. You shipped anyway, documented the gaps, fixed them in public. That's how you learn — and how you build trust.

---

**Final thought:** You didn't just build APIs and a portfolio. You built the mental models that let you walk into any backend/AI role and say "I've seen this failure mode before. Here's how we handle it."

That's the real certificate.

---

**Word count:** ~680 words