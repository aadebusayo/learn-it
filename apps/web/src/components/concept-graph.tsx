"use client";

import type { ConceptEdge, ConceptNode } from "@learn-it/shared";
import { Background, Controls, ReactFlow, type Edge, type Node } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

interface ConceptGraphProps {
  concepts: ConceptNode[];
  edges: ConceptEdge[];
}

const positions: Record<string, { x: number; y: number }> = {
  paper: { x: 360, y: 140 },
  matmul: { x: 40, y: 20 },
  dot: { x: 70, y: 170 },
  softmax: { x: 110, y: 320 },
  embeddings: { x: 630, y: 70 },
  info: { x: 660, y: 260 },
};

const statusTone: Record<ConceptNode["status"], string> = {
  strong: "#466b4f",
  developing: "#2e6f83",
  weak: "#b45f43",
  missing: "#6d5773",
};

export function ConceptGraph({ concepts, edges }: ConceptGraphProps) {
  const nodes: Node[] = concepts.map((concept) => ({
    id: concept.id,
    position: positions[concept.id] ?? { x: 0, y: 0 },
    data: {
      label: (
        <div className="min-w-40 px-2 py-1">
          <div className="text-sm font-semibold">{concept.label}</div>
          <div className="mt-1 flex items-center justify-between gap-2 text-xs text-ink/65">
            <span>Depth {concept.depth}</span>
            <span style={{ color: statusTone[concept.status] }}>{concept.status}</span>
          </div>
        </div>
      ),
    },
    style: { borderColor: statusTone[concept.status] },
  }));

  const flowEdges: Edge[] = edges.map((edge) => ({
    id: `${edge.source}-${edge.target}`,
    source: edge.source,
    target: edge.target,
    label: edge.relation,
    animated: edge.relation === "prerequisite",
    style: { stroke: edge.relation === "prerequisite" ? "#2e6f83" : "#8f8271" },
  }));

  return (
    <div className="h-[460px] overflow-hidden rounded-lg border border-line bg-panel">
      <ReactFlow nodes={nodes} edges={flowEdges} fitView proOptions={{ hideAttribution: true }}>
        <Background color="#d8d2c3" gap={18} />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
