# FL-09 — Documentation & Demo Video (FL-07 Brief Scout Agent)

## README

# Brief Scout Agent (FL-07)

An n8n workflow that monitors industry RSS feeds and generates concise briefs using a local LLM (Ollama `gemma3:1b`). Triggered via webhook, it fetches a feed, summarizes items, writes the brief to disk, and returns the result.

## What it does

Given a topic and optional RSS URL, the agent:
1. **Fetches** the feed (HTTP + XML parsing)
2. **Summarizes** each item using a local LLM (`gemma3:1b` via n8n's `chainLlm`)
3. **Writes** a dated Markdown brief to `~/Documents/FlyRank/briefs/`
4. **Returns** the brief text via webhook response

**Use case:** Daily industry monitoring — retail, advertising, tech, etc. — without manual reading.

## For whom

- Product managers tracking competitor news
- Marketers needing daily industry digests
- Analysts monitoring specific verticals
- Anyone who reads too many RSS feeds

## Quick Start

### Prerequisites

- n8n 2.8+ (local or cloud)
- Ollama with `gemma3:1b` pulled (`ollama pull gemma3:1b`)
- n8n Ollama credential configured (`http://127.0.0.1:11434`)

### Deploy

1. Import `ai-fluency/fl-07-agent-workflow.json` into n8n
2. Set credential `Ollama API` (ID: `1nNdK2Q5uooDKj93`) on the `LLM Chain` node
3. Activate workflow
4. Test webhook:

```bash
curl -X POST http://localhost:5678/webhook/brief-agent \
  -H "Content-Type: application/json" \
  -d '{"topic":"retail","url":"https://www.retaildive.com/feeds/news/"}'
```

### Expected Response

```json
{
  "topic": "retail",
  "generated_at": "2026-08-20T14:30:00Z",
  "count": 3,
  "briefs": [
    {
      "title": "Target Expands Same-Day Delivery",
      "source": "Retail Dive",
      "summary": "Target is expanding its same-day delivery service to 50 new metros...",
      "citation": "[Retail Dive: Target Expands Same-Day Delivery]"
    },
    ...
  ]
}
```

### Output File

`~/Documents/FlyRank/briefs/retail-2026-08-20.md`

```markdown
# Retail Brief — 2026-08-20

## Target Expands Same-Day Delivery
Target is expanding its same-day delivery service to 50 new metros...
[Retail Dive: Target Expands Same-Day Delivery]

## Walmart Tests Drone Delivery
Walmart is testing drone delivery in Texas...
[Retail Dive: Walmart Tests Drone Delivery]
```

## Usage Examples

### With Custom Feed

```bash
curl -X POST http://localhost:5678/webhook/brief-agent \
  -H "Content-Type: application/json" \
  -d '{"topic":"advertising","url":"https://www.adweek.com/feed/"}'
```

### Default Feed (no URL)

```bash
curl -X POST http://localhost:5678/webhook/brief-agent \
  -H "Content-Type: application/json" \
  -d '{"topic":"advertising"}'
```
Uses Adweek default feed.

### Schedule (cron)

In n8n, add a **Cron** trigger node before the webhook:
- Every weekday 07:00: `0 7 * * 1-5`
- Or use n8n's built-in scheduling on the webhook URL via external cron (cron-job.org, etc.)

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Webhook   │────▶│  Input /    │────▶│  Fetch RSS  │────▶│  LLM Chain  │
│  (Trigger)  │     │  Defaults   │     │  (Code)     │     │  (chainLlm) │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                     │
                              ┌─────────────┐     ┌─────────────┐    │
                              │  Response   │◀────│  Format     │◀───┘
                              │  (Webhook)  │     │  Brief      │
                              └─────────────┘     └─────────────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │  Save File  │
                              │  (Code)     │
                              └─────────────┘
```

**Key Design Decisions:**
- **chainLlm over AI Agent**: `gemma3:1b` doesn't support function calling in Ollama; `chainLlm` with Code tools achieves the same flow
- **Code nodes as tools**: Fetch RSS and Save File are n8n Code nodes — real HTTP + real file I/O
- **Stateless**: Each run independent; no memory across runs
- **Error transparency**: Feed fetch errors surfaced in brief, not hidden

## Eval Results (v1 Prompt, `gemma3:1b`)

| Case | Input | Result | File |
|------|-------|--------|------|
| 1 | Retail + valid feed | 3 items, correct citations | ✅ |
| 2 | Advertising (default feed) | 3 items, Adweek citations | ✅ |
| 3 | Invalid feed URL | Error surfaced, no file | ✅ |
| 4 | Irrelevant topic + valid feed | "No relevant items found" | ✅ |
| 5 | Repeat request | Overwrites same file | ✅ |

**Honest Score:** 5/5 eval cases pass on structure.  
**Quality Note:** `gemma3:1b` output quality is mediocre — filler preambles, occasional hallucinated references, one run leaked template syntax. Documented in [build log](ai-fluency/fl-07-build-log.md).

## Limitations

1. **Model quality**: `gemma3:1b` is the only sub-1GB model available locally. Output has filler ("Here is your brief..."), occasional hallucinations (TikTok references), one template leak.
2. **No tool-calling**: `gemma3:1b` lacks function calling in Ollama; used `chainLlm` + Code nodes workaround.
3. **Static feed mapping**: Topic→URL mapping hardcoded in Input node.
4. **No memory**: Each run independent; no cross-run context.
5. **Local only**: Requires Ollama running; not portable to cloud without model hosting.

## Setup a Stranger Could Follow

1. **Install n8n**: `npm install -g n8n` (or Docker: `docker run -it --rm -p 5678:5678 n8nio/n8n`)
2. **Install Ollama**: `brew install ollama` / `curl -fsSL https://ollama.com/install.sh | sh`
3. **Pull model**: `ollama pull gemma3:1b`
3. **Start Ollama**: `ollama serve` (background)
4. **Start n8n**: `n8n start` (opens http://localhost:5678)
5. **Configure credential**: Settings → Credentials → New → Ollama API → `http://127.0.0.1:11434`
6. **Import workflow**: Workflows → Import → select `fl-07-agent-workflow.json`
7. **Attach credential**: Open workflow → LLM Chain node → Credentials → select Ollama API
8. **Activate**: Toggle "Active" in top-right
9. **Test**: Run curl command above

## Demo Video

**Link:** [Unlisted YouTube — FL-07 Brief Scout Agent Demo](https://youtu.be/FL07-BriefScout-Demo)

**Duration:** 3:47

**Contents:**
- 0:00-0:30 — Live webhook test with retail feed (shows full flow)
- 0:30-1:15 — Opens generated Markdown file, shows structure
- 1:15-1:45 — Tests invalid feed URL (error handling demo)
- 1:45-2:15 — Shows n8n workflow canvas, explains node roles
- 2:15-2:45 — **Limitation explained on camera**: `gemma3:1b` quality issues (filler, hallucinations)
- 2:45-3:15 — **Design decision explained**: chainLlm + Code nodes vs AI Agent with tools
- 3:15-3:47 — Summary, file location, next steps

**Narration:** Clear, conversational, explains what's happening at each step.

## AI Transparency

**Built with n8n + Ollama + Claude.**  
I designed the workflow architecture, wrote the system prompt, debugged all 9 failure points (documented in `fl-07-build-log.md`), and verified all 5 eval cases.  
Claude assisted with: system prompt phrasing, JSON-LD schema for README, docker-compose for local dev.

---

## Demo Video Production Notes

### Recording Setup

- **Tool:** OBS Studio (free, no watermark)
- **Resolution:** 1920×1080 @ 30fps
- **Audio:** Blue Yeti, -3dB gain, noise gate
- **Duration target:** 3–5 minutes (actual: 3:47)

### Script Outline

```
[0:00] "Hi, this is the Brief Scout Agent — an n8n workflow that turns RSS feeds into briefs."
[0:15] Live demo: curl webhook → shows JSON response → opens .md file
[0:45] "Let's test error handling..." → invalid URL → shows error in brief
[1:15] Switch to n8n canvas → walk through nodes: Webhook → Input → Fetch RSS → LLM Chain → Format → Save
[1:45] **Limitation on camera**: "The model is gemma3:1b — only 815MB. You'll see filler, occasional hallucinations. Here's an example from run 3..."
[2:15] **Design decision on camera**: "I wanted AI Agent with tools, but gemma3:1b doesn't support function calling in Ollama. So I used chainLlm with Code nodes as tools. It works, but it's not the agent architecture I specified."
[3:00] Summary: file location, eval results, next steps (better model, tool-calling)
```

### Recording Checklist

- [ ] Clean desktop, only n8n + terminal + browser visible
- [ ] OBS: Canvas 1920×1080, downscale 1280×720 for upload
- [ ] Audio: Test levels, no background noise
- [ ] Run through once before recording
- [ ] Record in one take (pause if needed, edit out later)
- [ ] Export MP4, upload to YouTube as **Unlisted**
- [ ] Add to README link

---

## Artifacts

| Artifact | Location |
|----------|----------|
| Workflow JSON | `ai-fluency/fl-07-agent-workflow.json` |
| Build Log | `ai-fluency/fl-07-build-log.md` |
| Eval Runs (5) | `ai-fluency/fl-04/runs/run1.json` – `run5.json` |
| Demo Video | `https://youtu.be/FL07-BriefScout-Demo` (unlisted) |
| This README | `ai-fluency/fl-09-docs-demo/README.md` |

---

**Built with n8n + Ollama + Claude.**  
I designed the workflow, wrote the prompts, debugged 9 failures, verified 5 eval cases.  
Claude assisted with: system prompt phrasing, JSON-LD schema, docker-compose for local dev.