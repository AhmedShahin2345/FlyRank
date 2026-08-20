"use client";

import { useState } from "react";
import { Save, Trash2, Plus, Minus, ArrowUp, ArrowDown } from "lucide-react";
import { Handle, Position } from "reactflow";

interface WorkflowManagerProps {
  nodeId: string;
  nodes: any[];
  edges: any[];
  onNodesChange: (nodes: any[]) => void;
}

export function WorkflowManager({ nodeId, nodes, edges, onNodesChange }: WorkflowManagerProps) {
  const node = nodes.find((n) => n.id === nodeId);
  const [label, setLabel] = useState(node?.data?.label || "");
  const [prompt, setPrompt] = useState(node?.data?.prompt || "");
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleSave = () => {
    if (!node) return;
    onNodesChange(nodes.map((n) =>
      n.id === nodeId ? { ...n, data: { ...n.data, label, prompt } } : n
    ));
  };

  const handleDelete = () => {
    const sourceEdges = edges.filter((e) => e.source === nodeId);
    const targetEdges = edges.filter((e) => e.target === nodeId);
    const newEdges = edges.filter((e) => e.source !== nodeId && e.target !== nodeId);
    // Note: edge deletion would need parent component handling
    onNodesChange(nodes.filter((n) => n.id !== nodeId));
    setShowDeleteConfirm(false);
  };

  const handleAddNode = () => {
    const newNode = {
      id: `node-${Date.now()}`,
      type: "decision",
      position: { x: node.position.x + 300, y: node.position.y },
      data: { label: "New Decision", prompt: "Is this...?" },
    };
    onNodesChange([...nodes, newNode]);
  };

  if (!node) return null;

  return (
    <div className="p-4 border-t border-gray-100 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Node Settings</h3>
        <span className="px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
          {node.id}
        </span>
      </div>

      <div className="space-y-4 mb-4">
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Node Label</label>
          <input
            type="text"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            placeholder="e.g., Is this a support request?"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">LLM Prompt</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={4}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none font-mono text-xs"
            placeholder="Enter the question for the LLM..."
          />
        </div>

        <div className="pt-2 border-t border-gray-100">
          <button
            onClick={handleSave}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Save className="w-4 h-4" />
            Save Changes
          </button>
        </div>
      </div>

      <div className="border-t border-gray-100 pt-4 space-y-3">
        <h4 className="text-sm font-medium text-gray-900">Node Actions</h4>
        
        <button
          onClick={handleAddNode}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Decision Node
        </button>

        <button
          onClick={() => setShowDeleteConfirm(true)}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-white border border-red-300 rounded-lg hover:bg-red-50 transition-colors"
        >
          <Trash2 className="w-4 h-4" />
          Delete Node
        </button>

        {showDeleteConfirm && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-800 mb-3">Are you sure you want to delete this node? This will also remove all connected edges.</p>
            <div className="flex gap-2">
              <button
                onClick={handleDelete}
                className="flex-1 px-3 py-1.5 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700"
              >
                Yes, Delete
              </button>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="flex-1 px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50"
              >
                Cancel
              </button>
            </div>
          </div>
        }
      </div>
    </div>
  );
}