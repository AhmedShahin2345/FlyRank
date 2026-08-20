# 🧠 AI Fluency Track · FlyRank Internship

Welcome to the **AI Fluency** track of the FlyRank software engineering internship. This repository documents a comprehensive 8-week progression through prompt engineering, autonomous workflow automation (n8n), local LLM orchestration (Ollama), Model Context Protocol (MCP) integrations, personal branding, and final capstone delivery.

---

> [!IMPORTANT]
> # 🌟 Final Capstone Project — Standalone Repository
> **The FlyRank Capstone Widget Platform is officially hosted and maintained as its own dedicated GitHub repository:**  
> 👉 **[https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)**  
> *(The complete capstone codebase is also mirrored locally inside [`fl-10-capstone/flyrank-capstone-widget-platform/`](fl-10-capstone/flyrank-capstone-widget-platform/))*

---

## 🗺️ 8-Week Curriculum & Deliverables Index

| Week | Focus Area | Deliverables & Documentation | Key Artifacts |
|---|---|---|---|
| **Week 1** | **Workflow Audit & Sitemap** | [`FL-01-AI-Workflow-Audit.md`](FL-01-AI-Workflow-Audit.md)<br>[`FL-01-Portfolio-Sitemap.md`](FL-01-Portfolio-Sitemap.md)<br>[`FL-01-Proof-Statement.md`](FL-01-Proof-Statement.md) | `evidence/sitemap_sketch.png` |
| **Week 2** | **Prompt Engineering & Ladders** | [`FL-02-Framed-Cases.md`](FL-02-Framed-Cases.md)<br>[`FL-02-Prompt-Ladder.md`](FL-02-Prompt-Ladder.md)<br>[`FL-02-Prompt-Iteration-Log.md`](FL-02-Prompt-Iteration-Log.md) | `evidence/claude_1.png` - `claude_3.png` |
| **Week 3** | **Identity Kit & Strategy** | [`week-3-identity-kit.md`](week-3-identity-kit.md)<br>[`week-3-through-line.md`](week-3-through-line.md)<br>[`week-3-curate-images.md`](week-3-curate-images.md) | [`identity/`](identity/) (monogram, fonts, palette) |
| **Week 4** | **Systems, MCP & Workflows** | [`week-4-three-roads.md`](week-4-three-roads.md)<br>[`week-4-empty-but-live.md`](week-4-empty-but-live.md)<br>[`week-4-fl-05-mcp.md`](week-4-fl-05-mcp.md)<br>[`week-4-fl-04-workflow.md`](week-4-fl-04-workflow.md) | [`fl-04/`](fl-04/) (5 real RSS runs)<br>[`mcp-setup/`](mcp-setup/) (filesystem MCP) |
| **Week 5** | **Agent Architecture & Deployment** | [`week-5-pf-04-dns-walkthrough.md`](week-5-pf-04-dns-walkthrough.md)<br>[`week-5-explain-it-like-you-built-it.md`](week-5-explain-it-like-you-built-it.md)<br>[`fl-06-agent-spec.md`](fl-06-agent-spec.md)<br>[`fl-07-build-log.md`](fl-07-build-log.md) | [`fl-07-agent-workflow.json`](fl-07-agent-workflow.json)<br>[`evidence/fl-07-agent-run.mov`](evidence/fl-07-agent-run.mov) |
| **Week 6** | **Proactive Automation & Feedback** | [`w6-make-it-do-something-explainer.md`](w6-make-it-do-something-explainer.md)<br>[`w6-mobile-fix-log.md`](w6-mobile-fix-log.md)<br>[`w6-phone-check-notes.md`](w6-phone-check-notes.md)<br>[`w6-survive-the-crit.md`](w6-survive-the-crit.md) | Scheduled cron trigger (`0 9 * * 2`) & outbound Slack dispatch |
| **Week 7** | **Quality & Domain Flag Planting** | [`break-your-own-site.md`](break-your-own-site.md)<br>[`plant-your-flag.md`](plant-your-flag.md) | 8 bugs audited, Plausible analytics, FlyRank badge |
| **Week 8** | **Capstone & Future Roadmap** | [`fl-09-docs-demo/`](fl-09-docs-demo/) (Docs & Demo)<br>[`fl-10-capstone/`](fl-10-capstone/) (Capstone Package & Codebase)<br>[`future-plan.md`](future-plan.md) (Roadmap) | **[flyrank-capstone-widget-platform](https://github.com/AhmedShahin2345/flyrank-capstone-widget-platform)** |

---

## 🤖 Running the Local Autonomous Agent (n8n + Ollama)

The FL-07 / Week 6 autonomous briefing workflow runs locally on your machine with zero external API costs:

### Prerequisites
1. **Ollama**: Running locally with `gemma3:1b` model:
   ```bash
   ollama run gemma3:1b
   ```
2. **n8n**: Running locally on port `5678`:
   ```bash
   n8n start
   ```

### Executing the Brief Scout Agent
Trigger the agent via webhook:
```bash
curl -X POST http://localhost:5678/webhook/brief-agent \
  -H "Content-Type: application/json" \
  -d '{"topic": "retail", "url": "https://www.retaildive.com/feeds/news/", "max_items": 3}'
```

---

## 📸 Visual Evidence Directory

All visual evidence and recordings are organized in [`evidence/`](evidence/):
- `empty-but-live.png`: Initial GitHub Pages deployment.
- `pf-04-live.png`: Final personal portfolio live screenshot.
- `mcp-evidence.png` & `mcp-tasks.png`: Model Context Protocol tool executions.
- `fl-04-canvas.png`, `fl-04-executions.png`, `fl-04-runs.png`: n8n pipeline visual proof.
- `fl-07-agent-run.mov`: 2-minute unedited screen recording of agent execution.
- `break-your-own-site.png` & `plant-your-flag-*.png`: Week 7 quality and analytics verifications.
