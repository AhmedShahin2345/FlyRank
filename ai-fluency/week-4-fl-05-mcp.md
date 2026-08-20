# Week 4 · FL-05 — Agent Concepts and MCP Basics

## The explainer

"Agent" is the most abused word in AI right now, so let me be precise about
what I actually built and what I didn't.

### Workflow vs agent

A **workflow** is a fixed sequence of steps: step A always runs, then step B,
then step C. The order is decided in advance by the person who designed it,
and each step has a defined handoff — one step's output is the next step's
input. Nothing in the chain decides *which* step to run next; the chain is
the decision.

An **agent**, as Anthropic's *Building Effective Agents* frames it, is a
system where a model makes the routing decisions itself: it decides what to
do next, picks which tool to call, observes the result, and loops until the
job is done. The workflow has the path pre-drawn; the agent reads the map as
it walks. The practical difference: a workflow that hits an unexpected input
does what its designer told it to do anyway; an agent improvises a path
around it.

My FL-04 pipeline is unambiguously a **workflow**. Its steps — gather, then
synthesize, then draft, then format — run in a fixed order with defined
handoffs, and the model never chooses which step comes next. That is not a
flaw; it is the right design for a research pipeline, because a weekly brief
should be reproducible, and a reproducible chain beats improvisation when
the deliverable is the same every week.

### What MCP is

**MCP (Model Context Protocol)** is a standard way to let an AI connect to
tools and data sources — a "USB-C port for AI applications". Before MCP,
every integration was bespoke: a filesystem plugin here, a database plugin
there, each with its own shape. MCP defines one protocol with three
primitives:

- **Tools** — actions the AI can invoke (read a file, query an API, run a
  search). The model decides to call one, the server executes it, the result
  comes back into the conversation.
- **Resources** — data the AI can read (a file, a config, a document), like
  a read-only file cabinet.
- **Prompts** — reusable instruction templates the server exposes, so the
  same workflow start isn't rewritten every time.

The crucial point: with MCP, a chat alone becomes a chat *plus* a
machine that can touch the outside world — which is exactly what separates
an agent (or tool-using assistant) from a chatbot.

### What I connected, and the three tasks

I connected the official **filesystem MCP server** to a client through the
MCP protocol (the server exposes 14 tools; setup in `mcp-setup/`). Three
tasks that chat alone could not have done:

1. **`list_directory`** — listed the project folder and returned the real
   file names (chat alone cannot see a file system).
2. **`read_text_file`** — read `budget-notes.txt` and returned its actual
   content (chat alone does not have my files).
3. **`search_files` + `get_file_info`** — found every `.txt` note in the
   project and returned metadata (size, modified time, permissions) for one
   of them.

Evidence: `evidence/mcp-evidence.png` and `evidence/mcp-tasks.png` show the
client connecting, listing the 14 tools, and the three tool calls with their
real outputs — outputs that came from the file system, not from the model's
memory.

### What FL-04 would need to become an agent

My FL-04 workflow (gather → synthesize → draft → format) becomes an agent
when the model starts deciding the path. Concretely:

1. **A research tool.** The "gather" step is currently a fixed source list.
   Add an MCP `web_search` tool and the model can choose which sources to
   hit, follow up on what it finds, and go deeper where the topic needs it.
2. **A feedback loop.** After drafting, the model checks its own output
   against the brief's criteria and decides whether to revise — a loop, not
   a fixed pass. A critique tool (or rubric resource) gives it something
   concrete to check against.
3. **A decision point.** The pipeline stops being "always do all four steps"
   and becomes "synthesize first, then *decide* whether this brief needs a
   deep draft or a quick summary" — the routing choice moves from the
   designer to the model.

The cheapest single upgrade: add MCP **tools** (research + file read/write)
so the model can act on what it finds. That one change is what turns my
workflow into a tool-using loop — and it is the honest definition of the
"agent" word: not marketing, just a model that decides what to do next,
with tools to do it.

---

*Explainer word count: ~700. Written in my own words after reading Building
Effective Agents and the MCP introduction, and after running the three tool
calls above.*

## Evidence

- `evidence/mcp-evidence.png` — MCP client connected to the filesystem
  server; 14 tools listed over the protocol.
- `evidence/mcp-tasks.png` — Task 3 outputs: real file paths and metadata
  returned by tool calls.
- Full transcript: `mcp-setup/mcp-evidence.txt`
- Client + setup: `mcp-setup/mcp-client.py`, server registered via
  `claude mcp add --scope local fs -- npx -y @modelcontextprotocol/server-filesystem /tmp/mcp-test`