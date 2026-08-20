import { Node, Edge } from "reactflow";

export const initialNodes: Node[] = [
  {
    id: "start",
    type: "decision",
    position: { x: 250, y: 50 },
    data: {
      label: "Is this a support request?",
      prompt: "The user is asking for help with a product or service issue. Is this a support request? Answer YES or NO only.",
    },
  },
  {
    id: "support",
    type: "decision",
    position: { x: 50, y: 250 },
    data: {
      label: "Is it urgent?",
      prompt: "The user has a support issue. Is this urgent (system down, data loss, security issue)? Answer YES or NO only.",
    },
  },
  {
    id: "sales",
    type: "decision",
    position: { x: 450, y: 250 },
    data: {
      label: "Is it a pricing inquiry?",
      prompt: "The user is asking about pricing, plans, or purchasing. Is this a pricing inquiry? Answer YES or NO only.",
    },
  },
  {
    id: "urgent-support",
    type: "decision",
    position: { x: 50, y: 450 },
    data: {
      label: "Escalate to team?",
      prompt: "This is an urgent support issue. Should it be escalated to the on-call team immediately? Answer YES or NO only.",
    },
  },
  {
    id: "pricing",
    type: "decision",
    position: { x: 450, y: 450 },
    data: {
      label: "Enterprise customer?",
      prompt: "The user is asking about pricing. Are they asking about enterprise/custom plans? Answer YES or NO only.",
    },
  },
];

export const initialEdges: Edge[] = [
  {
    id: "e1",
    source: "start",
    target: "support",
    sourceHandle: "yes",
    type: "yes",
    label: "YES",
  },
  {
    id: "e2",
    source: "start",
    target: "sales",
    sourceHandle: "no",
    type: "no",
    label: "NO",
  },
  {
    id: "e3",
    source: "support",
    target: "urgent-support",
    sourceHandle: "yes",
    type: "yes",
    label: "YES",
  },
  {
    id: "e4",
    source: "support",
    target: "sales",
    sourceHandle: "no",
    type: "no",
    label: "NO",
  },
  {
    id: "e5",
    source: "sales",
    target: "pricing",
    sourceHandle: "yes",
    type: "yes",
    label: "YES",
  },
  {
    id: "e6",
    source: "sales",
    target: "support",
    sourceHandle: "no",
    type: "no",
    label: "NO",
  },
];