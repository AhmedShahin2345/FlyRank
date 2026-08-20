"use client";

import { CheckCircle, XCircle, Clock, Zap, ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface ExecutionPanelProps {
  isExecuting: boolean;
  result: {
    path: string[];
    logs: Array<{ nodeId: string; prompt: string; response: string; timestamp: number }>;
  } | null;
  nodeCount: number;
  edgeCount: number;
}

export function ExecutionPanel({ isExecuting, result, nodeCount, edgeCount }: ExecutionPanelProps) {
  const [expandedLogs, setExpandedLogs] = useState(false);

  if (nodeCount === 0) {
    return (
      <div className="p-6 text-center text-gray-500">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2h10" />
          </svg>
        </div>
        <p className="text-lg font-medium text-gray-900 mb-2">No workflow yet</p>
        <p className="text-sm text-gray-500 max-w-xs mx-auto">
          Add decision nodes to the canvas and connect them to create a workflow.
        </p>
      </div>
    );
  }

  if (isExecuting) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Execution in Progress</h2>
          <div className="flex items-center gap-2 text-primary-600">
            <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <span className="text-sm font-medium">Running...</span>
          </div>
        </div>
        <div className="space-y-3">
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600">The workflow is being executed via Inngest.</p>
            <p className="text-xs text-gray-500 mt-1">Each decision node calls an LLM which returns YES or NO, determining the next path.</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-primary-600" />
          Execution Results
        </h2>
        <div className="p-4 bg-gray-50 rounded-lg text-center text-gray-500">
          <p className="mb-2">Click <span className="font-medium text-primary-600">Execute</span> to run the workflow.</p>
          <p className="text-xs">Each decision node will call an LLM with its prompt.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Execution Complete</h2>
        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
          Completed
        </span>
      </div>

      <div className="mb-4 p-3 bg-green-50 rounded-lg border border-green-200">
        <div className="flex items-center gap-2 text-sm text-green-800 mb-2">
          <CheckCircle className="w-4 h-4" />
          <span className="font-medium">Execution path: {result.path.join(" → ")}</span>
        </div>
        <div className="text-xs text-green-700">
          {result.logs.length} decision(s) made
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-900">Decision Log</h3>
          <button
            onClick={() => setExpandedLogs(!expandedLogs)}
            className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700"
          >
            {expandedLogs ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            <span>{expandedLogs ? "Collapse" : "Expand"}</span>
          </button>
        </div>

        <div className={`${expandedLogs ? "block" : "hidden"} space-y-3`}>
          {result.logs.map((log, index) => (
            <div key={index} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex items-center gap-2 text-xs mb-2">
                <span className="px-2 py-0.5 bg-primary-100 text-primary-700 rounded text-xs font-medium">
                  Step {index + 1}
                </span>
                <span className="text-gray-500">{new Date(log.timestamp).toLocaleTimeString()}</span>
              </div>
              <div className="mb-2">
                <span className="text-xs font-medium text-gray-500">Prompt:</span>
                <p className="text-sm text-gray-900 font-mono bg-white p-2 rounded border">{log.prompt}</p>
              </div>
              <div>
                <span className="text-xs font-medium text-gray-500">Response:</span>
                <p className="text-sm text-gray-900">
                  <span className={`px-2 py-0.5 rounded text-sm font-semibold ${
                    log.response === "YES" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                  }`}>
                    {log.response}
                  </span>
                </p>
              </div>
            </div>
          ))}
        </div>

        {!expandedLogs && result.logs.length > 0 && (
          <div className="mt-3 p-3 bg-gray-50 rounded-lg text-center text-sm text-gray-500">
            Click "Expand" to see {result.logs.length} decision step(s)
          </div>
        )}
      </div>
    </div>
  );
}