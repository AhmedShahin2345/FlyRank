"use client";

import { useState, useCallback } from "react";
import { ReactFlow, Background, Controls, MiniMap, NodeTypes, EdgeTypes, useReactFlow, addEdge, Connection } from "reactflow";
import "reactflow/dist/style.css";
import { DecisionNode } from "@/components/DecisionNode";
import { YesNoEdge } from "@/components/YesNoEdge";
import { ExecutionPanel } from "@/components/ExecutionPanel";
import { Toolbar } from "@/components/Toolbar";
import { WorkflowManager } from "@/components/WorkflowManager";
import { initialNodes, initialEdges } from "@/lib/initialFlow";

const nodeTypes: NodeTypes = {
  decision: DecisionNode,
};

const edgeTypes: EdgeTypes = {
  yes: YesNoEdge,
  no: YesNoEdge,
};

export default function DecisionFlowPage() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<{
    path: string[];
    logs: Array<{ nodeId: string; prompt: string; response: string; timestamp: number }>;
  } | null>(null);

  const { getNodes, getEdges } = useReactFlow();

  const onNodesChange = useCallback((changes: any) => {
    setNodes((nds) => nds.map((node) => {
      const change = changes.find((c: any) => c.id === node.id);
      if (change && change.type === "select") {
        setSelectedNodeId(change.selected ? node.id : null);
      }
      return node;
    }));
  }, []);

  const onEdgesChange = useCallback((changes: any) => {
    setEdges((eds) => eds.map((edge) => {
      const change = changes.find((c: any) => c.id === edge.id);
      if (change && change.type === "select") {
        // Edge selection handling if needed
      }
      return edge;
    }));
  }, []);

  const onConnect = useCallback((connection: Connection) => {
    const sourceNode = nodes.find((n) => n.id === connection.source);
    if (!sourceNode) return;

    const edgeType = connection.sourceHandle?.includes("yes") ? "yes" : "no";
    const label = edgeType === "yes" ? "YES" : "NO";

    setEdges((eds) => addEdge(
      {
        ...connection,
        type: edgeType,
        label,
        style: { stroke: edgeType === "yes" ? "#22c55e" : "#ef4444" },
        animated: true,
      },
      eds
    ));
  }, [nodes]);

  const handleExecute = async () => {
    setIsExecuting(true);
    setExecutionResult({ path: [], logs: [] });

    try {
      const response = await fetch("/api/execute-workflow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nodes, edges }),
      });

      const data = await response.json();
      
      if (data.success) {
        setExecutionResult({
          path: data.path,
          logs: data.logs,
        });
      } else {
        console.error("Execution failed:", data.error);
      }
    } catch (error) {
      console.error("Execution error:", error);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleSaveWorkflow = async () => {
    const workflow = { nodes, edges };
    const blob = new Blob([JSON.stringify(workflow, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `workflow-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleLoadWorkflow = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const workflow = JSON.parse(e.target?.result as string);
        if (workflow.nodes && workflow.edges) {
          setNodes(workflow.nodes);
          setEdges(workflow.edges);
        }
      } catch (err) {
        console.error("Failed to load workflow:", err);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="h-screen flex flex-col">
      <Toolbar
        onExecute={handleExecute}
        onSave={handleSaveWorkflow}
        onLoad={handleLoadWorkflow}
        isExecuting={isExecuting}
        selectedNodeId={selectedNodeId}
        nodeCount={nodes.length}
        edgeCount={edges.length}
      />
      
      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 w-3/4">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            fitView
            attribs={{ id: "react-flow-canvas" }}
          >
            <Background color="#e0e0e0" gap={16} />
            <Controls />
            <MiniMap />
          </ReactFlow>
        </div>

        <div className="w-1/4 border-l border-gray-200 bg-white overflow-y-auto">
          {selectedNodeId ? (
            <WorkflowManager
              nodeId={selectedNodeId}
              nodes={nodes}
              edges={edges}
              onNodesChange={setNodes}
            />
          ) : (
            <ExecutionPanel
              isExecuting={isExecuting}
              result={executionResult}
              nodeCount={nodes.length}
              edgeCount={edges.length}
            />
          )}
        </div>
      </div>
    </div>
  );
}