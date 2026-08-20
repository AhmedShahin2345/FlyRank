"use client";

import { Play, Save, Upload, Plus, Zap, Loader2 } from "lucide-react";

interface ToolbarProps {
  onExecute: () => void;
  onSave: () => void;
  onLoad: (file: File) => void;
  isExecuting: boolean;
  selectedNodeId: string | null;
  nodeCount: number;
  edgeCount: number;
}

export function Toolbar({ onExecute, onSave, onLoad, isExecuting, selectedNodeId, nodeCount, edgeCount }: ToolbarProps) {
  const [fileInput, setFileInput] = useState<HTMLInputElement | null>(null);

  return (
    <div className="h-16 px-6 border-b border-gray-200 bg-white flex items-center justify-between shadow-sm">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-bold text-gray-900">AI Decision Flow</h1>
        <div className="hidden sm:flex items-center gap-4 text-sm text-gray-500">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-green-500" />
            <span>{nodeCount} nodes</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-blue-500" />
            <span>{edgeCount} edges</span>
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={onSave}
          className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          title="Save workflow (JSON)"
        >
          <Save className="w-4 h-4" />
          Save
        </button>

        <input
          type="file"
          accept=".json"
          ref={setFileInput}
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) onLoad(file);
            if (fileInput) fileInput.value = "";
          }}
        />
        <button
          onClick={() => fileInput?.click()}
          className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          title="Load workflow (JSON)"
        >
          <Upload className="w-4 h-4" />
          Load
        </button>

        <button
          onClick={onExecute}
          disabled={isExecuting || nodeCount === 0}
          className="flex items-center gap-2 px-6 py-2 text-sm font-semibold text-white bg-primary-600 border-none rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isExecuting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Executing...
            </>
          ) : (
            <>
              <Zap className="w-4 h-4" />
              Execute
            </>
          )}
        </button>
      </div>
    </div>
  );
}