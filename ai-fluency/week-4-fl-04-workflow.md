# Week 4 · FL-04: Build a Workflow with n8n

**Deliverable:** an n8n workflow that takes a feed URL, pulls the latest industry news, and returns an AI-written weekly brief — executed 5 times against 5 different real RSS feeds, all documented below.

---

## The workflow: "Weekly Industry Brief (FL-04)"

`ai-fluency/fl-04/workflow.json` (importable into any n8n instance).

**Pipeline:**

```
POST /webhook/brief  (webhook, respond with last node)
  → Input         (set node: url, topic, max_items from the request body)
  → Gather        (RSS Feed Read node, reads any URL)
  → Limit         (first N items, max_items from the request)
  → Synthesize    (Basic LLM Chain)
       └─ Ollama Chat Model (gemma3:1b via local Ollama on 127.0.0.1:11434)
  → Format        (Code node: pairs each article with its brief, adds topic + timestamp)
```

One webhook call:

```
POST http://localhost:5678/webhook/brief
{
  "url": "https://www.marketingdive.com/feeds/news/",
  "topic": "student marketing & sponsorships",
  "max_items": 3
}
```

returns one JSON object with `topic`, `generated_at`, `count`, and `briefs[]` — each brief is `{title, link, ai}` where `ai` is the model's three-line INSIGHT / TAG / RELEVANCE output.

---

## Five real runs

Run on 20 Aug 2026 against five working feeds. Every run returned HTTP 200 with 3 AI briefs.

| # | Feed | Topic | Items | Time |
|---|------|-------|-------|------|
| 1 | Marketing Dive (news) | student marketing & sponsorships | 3 | ~5 s |
| 2 | Adweek (all) | advertising industry news | 3 | ~4 s |
| 3 | HubSpot Marketing Blog | marketing strategy | 3 | ~7 s |
| 4 | Retail Dive (news) | retail & ecommerce | 3 | ~4 s |
| 5 | TechCrunch (all) | startups & tech | 3 | ~5 s |

All five request/response pairs are saved verbatim in `ai-fluency/fl-04/runs/run1.json … run5.json`.

Example (run 1, first brief):

```json
{
  "title": "Estée Lauder’s Jo Malone turns to ‘Fortnite’ for first gaming activation",
  "link": "https://www.marketingdive.com/news/estee-lauders-jo-malone-turns-to-fortnite-for-first-gaming-activation/828061/",
  "ai": "INSIGHT: …TAG: social … RELEVANCE: …"
}
```

The LLM ran locally (Ollama, `gemma3:1b`, pulled to the machine; ~815 MB model) — no cloud cost, no external API key.

---

## What actually went wrong during the build (and how each was fixed)

These were the real failure points; each one was found by running, not reading.

1. **Wrong node-type prefix for n8n 2.x.** `n8n-nodes-langchain.lmChatOllama` → activation error "Unrecognized node type". In n8n 2.8 the package is `@n8n/n8n-nodes-langchain`, so the type is `@n8n/n8n-nodes-langchain.lmChatOllama` (and `…chainLlm`).
2. **Ollama node requires the `ollamaApi` credential** — activation refused with "Missing required credential: ollamaApi". Created one via `POST /rest/credentials` (baseUrl `http://127.0.0.1:11434`) and attached it to the node.
3. **Webhook body is nested in n8n 2.x.** `$json.url` was `null`; the body lives at `$json.body.url`. Fixed the Input node expressions.
4. **Sub-node connections point the other way.** The model connection must be keyed by the *sub-node* (source) with the *chain* as the destination: `"Ollama": {"ai_languageModel": [[{"node": "LLM Chain", ...}]]}`. My first attempt had it reversed, which produced "A Model sub-node must be connected and enabled" at runtime.
5. **`localhost` → IPv6.** The Ollama node resolved `localhost` to `::1`, but Ollama only listens on `127.0.0.1` → `ECONNREFUSED ::1:11434` ("fetch failed"). Fix: use `http://127.0.0.1:11434` explicitly.
6. **The chain drops the input item.** `chainLlm` outputs only `{text: ...}` — article title/link don't pass through. The Format node reads `$('Limit')` (the articles) and `$('Synthesize · LLM Chain')` (the briefs) directly.
7. **RSS items have no `description`.** Keys are `title`, `link`, `content`, `contentSnippet`. The prompt now uses `contentSnippet`.
8. **The Limit node evaluates `$json.max_items` per RSS item** (undefined → unlimited). Use `$('Input').first().json.max_items` instead.
9. **Webhook returns the last node's *first* item.** Wrapped all briefs in one item `{topic, generated_at, count, briefs[]}` so the full output is returned.

---

## Honest assessment

- **The automation is real and repeatable**: any RSS URL → 3 fresh AI briefs in seconds, all local, zero API cost.
- **The model is small and it shows**: `gemma3:1b` pads output with preamble ("Okay, here's a three-line response…") despite a strict system message, and it sometimes drafts generic TikTok/Gen-Z briefs that don't match the article (e.g. run 5's Alation cyberattack story). A larger model (e.g. gemma3:12b or a cloud API) would fix most of that.
- **Weakest step is the synthesis step**, not the plumbing: fetch, limit, format, and response handling are deterministic; the model is the only "creative" part and the only part that hallucinates. That's the right place to invest next (better model, or retrieval of the full article text instead of the snippet).

## Links
- Workflow JSON: `ai-fluency/fl-04/workflow.json`
- Five runs (verbatim): `ai-fluency/fl-04/runs/run1.json` … `run5.json`
- Evidence screenshots: `ai-fluency/evidence/fl-04-*.png`