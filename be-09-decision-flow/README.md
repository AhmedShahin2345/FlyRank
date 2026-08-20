# BE-09 — AI Decision Flow with React Flow + Inngest

A visual AI workflow system where each node represents an AI decision step that returns YES or NO. The workflow execution runs through Inngest while the frontend visualizes the flow using React Flow.

## What it does

Build a visual AI workflow system where:
1. **Phase 1 - Setup**: Next.js app with React Flow, Inngest, OpenAI SDK, Tailwind CSS
2. **Phase 2 - Foundations**: Visual flow editor - canvas, add/connect/edit nodes, YES/NO edge types, local state persistence
3. **Phase 3 - Core**: Inngest workflow execution - each node = step, LLM returns YES/NO, dynamic traversal
4. **Phase 4 - Polish**: Execution logs panel, save/load workflows (JSON), animated active edges

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Flow    │────▶│     Inngest     │────▶│     OpenAI      │
│   (Frontend)    │     │  (Workflow)     │     │    (LLM)        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   LocalStorage  │     │   Execution     │
│   (Save/Load)   │     │   Logs Panel    │
└─────────────────┘     └─────────────────┘
```

## Quick Start

```bash
# 1. Install dependencies
cd be-09-decision-flow
npm install

# 2. Copy env and configure
cp .env.example .env
# Edit .env with your OpenAI API key and Inngest keys

# 3. Start Redis (for Inngest dev)
docker run -d -p 6379:6379 redis:7-alpine

# 4. Start development servers (in separate terminals)
npm run dev              # Next.js on port 3009
npm run inngest-dev      # Inngest dev server on port 8288
```

## Docker Compose (Recommended)

```bash
docker-compose up --build
```

This starts Redis, the Next.js app on port 3009, and Inngest dev server on port 8288.

## Features

### Visual Flow Editor
- **Canvas**: Pan, zoom, fit view, minimap
- **Nodes**: Add decision nodes with custom labels and LLM prompts
- **Edges**: Connect nodes with YES/NO paths (color-coded: green/red)
- **Editing**: Click nodes to edit label and prompt in side panel
- **Persistence**: Save/load workflows as JSON files

### Workflow Execution
- **Inngest Functions**: Each node runs as an Inngest step
- **LLM Calls**: OpenAI GPT-4o-mini returns only YES or NO
- **Dynamic Traversal**: Follows YES/NO edges based on LLM response
- **Execution Logs**: Step-by-step log showing prompt, response, and path taken

### Polish Features
- ✅ Execution logs panel with step-by-step detail
- ✅ Save/load workflows (JSON export/import)
- ✅ Animated active edges during execution
- ✅ Real-time execution status
- ✅ Node/edge counters in toolbar

## API Endpoints

### `POST /api/execute-workflow` — Start workflow execution
```json
{
  "nodes": [...],
  "edges": [...]
}
```
Returns: `{ success: true, message: "Workflow execution started" }`

### `POST /api/inngest` — Inngest webhook endpoint
Handles Inngest function execution.

## Configuration

All settings via `.env` (see `.env.example`):

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_BASE_URL` | No | Custom OpenAI base URL |
| `OPENAI_MODEL` | No | Model to use (default: gpt-4o-mini) |
| `INNGEST_EVENT_KEY` | Yes | Inngest event key |
| `INNGEST_SIGNING_KEY` | Yes | Inngest signing key |
| `NEXT_PUBLIC_APP_URL` | No | App URL for Inngest |

## Files

```
be-09-decision-flow/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main flow editor
│   │   ├── layout.tsx            # Root layout
│   │   ├── globals.css           # Global styles
│   │   └── api/
│   │       ├── inngest/route.ts  # Inngest webhook
│   │       └── execute-workflow/route.ts  # Start execution
│   ├── components/
│   │   ├── DecisionNode.tsx      # Custom decision node
│   │   ├── YesNoEdge.tsx         # YES/NO edge with labels
│   │   ├── Toolbar.tsx           # Top toolbar
│   │   ├── ExecutionPanel.tsx    # Right panel - execution/logs
│   │   └── WorkflowManager.tsx   # Right panel - node settings
│   └── lib/
│       ├── inngest.ts            # Inngest client
│       ├── functions.ts          # Inngest functions
│       ├── initialFlow.ts        # Default workflow
│       └── utils.ts              # Utility functions
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Example Workflow

The default workflow implements a support triage system:

```
Start: "Is this a support request?"
├── YES → "Is it urgent?"
│   ├── YES → "Escalate to team?"
│   └── NO → "Is it a pricing inquiry?"
└── NO → "Is it a pricing inquiry?"
    ├── YES → "Enterprise customer?"
    └── NO → (end)
```

## AI vs Me (Bonus Stage)

I specified the decision flow system and asked an LLM to build it. The AI version:

1. **Used local state only** — no Inngest, just a simple recursive function. My version uses Inngest for durable execution, retries, and observability.
2. **No edge types** — all edges looked the same. My version has distinct YES/NO edge types with color coding.
3. **No persistence** — workflow lost on refresh. My version has JSON save/load.
4. **No execution logs** — just final result. My version has step-by-step logs with prompts and responses.
5. **Single file component** — everything in one file. My version has proper component separation.

**What the AI did better:** It produced a working React Flow setup with custom nodes in one shot. I kept that structure and added the Inngest integration.

**What my spec forgot:** The exact Inngest function signature for step-by-step execution, the edge label rendering, and that nodes need unique IDs for the adjacency map. Small gaps, but each one let the AI choose for me.

---

**Built with Claude; I verified the React Flow setup, Inngest integration, OpenAI calls, and docker-compose myself.**