"use client";

import { useState } from "react";
import { Handle, Position, NodeProps } from "reactflow";
import { MessageSquare, Trash2, Minus, Plus } from "lucide-react";

interface DecisionNodeProps extends NodeProps {
  data: {
    label: string;
    prompt: string;
  };
}

export function DecisionNode({ data, id, selected, isConnectable }: DecisionNodeProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [prompt, setPrompt] = useState(data.prompt);
  const [label, setLabel] = useState(data.label);

  const handleSave = () => {
    // In a real app, this would update the node via onNodesChange
    setIsEditing(false);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    // Deletion would be handled by parent
  };

  return (
    <div
      className={`group relative min-w-[200px] max-w-[280px] bg-white rounded-xl shadow-lg border-2 transition-all ${
        selected ? "border-primary-500 shadow-primary-500/20" : "border-gray-200 hover:border-primary-300"
      }`}
      style={{ width: "220px" }}
    >
      {/* Node header */}
      <div className="flex items-center justify-between p-3 border-b border-gray-100 bg-gray-50 rounded-t-xl">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-primary-600" />
          <span className="font-semibold text-gray-900 text-sm">Decision</span>
        </div>
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={(e) => { e.stopPropagation(); setIsEditing(true); }}
            className="p-1 rounded hover:bg-gray-200 text-gray-500 hover:text-gray-700"
            title="Edit prompt"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            onClick={handleDelete}
            className="p-1 rounded hover:bg-gray-200 text-gray-500 hover:text-red-600"
            title="Delete node"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Node content */}
      <div className="p-3">
        {/* Label input */}
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-500 mb-1">Node Label</label>
          <input
            type="text"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            placeholder="e.g., Is this a support request?"
          />
        </div>

        {/* Prompt editor */}
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-500 mb-1">LLM Prompt</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={4}
            className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none font-mono text-xs"
            placeholder="Enter the question for the LLM..."
          />
        </div>

        {/* Connection handles */}
        <div className="flex justify-between">
          <Handle
            id="yes"
            type="source"
            position={Position.Left}
            className="w-3 h-3 bg-green-500 border-2 border-white"
            style={{ top: "60%" }}
          />
          <Handle
            id="no"
            type="source"
            position={Position.Right}
            className="w-3 h-3 bg-red-500 border-2 border-white"
            style={{ top: "60%" }}
          />
        </div>
      </div>

      {/* Edge labels */}
      <div className="flex justify-between px-3 pb-2 text-xs">
        <span className="text-green-600 font-medium">YES</span>
        <span className="text-red-600 font-medium">NO</span>
      </div>
    </div>
  );
}