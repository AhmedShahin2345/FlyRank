import { inngest } from "@/lib/inngest";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_BASE_URL,
});

interface WorkflowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: {
    label: string;
    prompt: string;
  };
}

interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle: string | null;
  targetHandle: string | null;
  type: "yes" | "no";
  label: string;
}

interface ExecuteWorkflowEvent {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
}

export const executeWorkflow = inngest.createFunction(
  { id: "execute-decision-workflow" },
  { event: "workflow/execute" },
  async ({ event, step }) => {
    const { nodes, edges } = event.data as ExecuteWorkflowEvent;
    
    // Build adjacency map for traversal
    const adjacencyMap = new Map<string, { yes: string | null; no: string | null }>();
    edges.forEach((edge) => {
      const source = edge.source;
      if (!adjacencyMap.has(source)) {
        adjacencyMap.set(source, { yes: null, no: null });
      }
      const handles = adjacencyMap.get(source)!;
      if (edge.sourceHandle?.includes("yes") || edge.type === "yes") {
        handles.yes = edge.target;
      } else if (edge.sourceHandle?.includes("no") || edge.type === "no") {
        handles.no = edge.target;
      }
    });

    // Find start node (node with no incoming edges)
    const targetIds = new Set(edges.map((e) => e.target));
    const startNode = nodes.find((n) => !targetIds.has(n.id));
    
    if (!startNode) {
      throw new Error("No start node found in workflow");
    }

    const executionPath: string[] = [];
    const logs: Array<{ nodeId: string; prompt: string; response: string; timestamp: number }> = [];
    
    let currentNodeId = startNode.id;
    let maxSteps = 50; // Prevent infinite loops

    while (currentNodeId && maxSteps > 0) {
      maxSteps--;
      executionPath.push(currentNodeId);
      
      const currentNode = nodes.find((n) => n.id === currentNodeId);
      if (!currentNode) break;

      // Call LLM for decision
      const prompt = currentNode.data.prompt || `Based on the context, answer YES or NO: ${currentNode.data.label}`;
      
      const response = await step.run(`llm-call-${currentNodeId}`, async () => {
        const completion = await openai.chat.completions.create({
          model: process.env.OPENAI_MODEL || "gpt-4o-mini",
          messages: [
            {
              role: "system",
              content: "You are a decision-making assistant. Respond with ONLY 'YES' or 'NO'. No explanations, no extra text."
            },
            {
              role: "user",
              content: prompt
            },
            temperature: 0.1,
            max_tokens: 10,
          });
        return completion.choices[0].message.content?.trim().toUpperCase() || "NO";
      });

      const decision = response === "YES" ? "YES" : "NO";
      
      logs.push({
        nodeId: currentNodeId,
        prompt,
        response: decision,
        timestamp: Date.now(),
      });

      // Determine next node based on decision
      const handles = adjacencyMap.get(currentNodeId);
      if (handles) {
        currentNodeId = decision === "YES" ? handles.yes : handles.no;
      } else {
        break; // No outgoing edges, end of workflow
      }
    }

    return {
      success: true,
      path: executionPath,
      logs,
    };
  }
);