"use client";

import { Edge, EdgeProps, MarkerType } from "reactflow";
import { BezierEdge } from "reactflow";

interface YesNoEdgeProps extends EdgeProps {
  label?: string;
}

export function YesNoEdge({ label, style, ...props }: YesNoEdgeProps) {
  const isYes = props.type === "yes";
  const color = isYes ? "#22c55e" : "#ef4444";
  const labelText = label || (isYes ? "YES" : "NO");

  return (
    <BezierEdge
      {...props}
      markerEnd={
        <MarkerType
          type="arrowclosed"
          color={color}
          width={20}
          height={20}
        />
      }
      style={{
        ...style,
        stroke: color,
        strokeWidth: 2,
      } as React.CSSProperties}
      label={labelText}
      labelStyle={{
        fill: color,
        fontSize: 11,
        fontWeight: 600,
        background: "white",
        padding: "2px 6px",
        borderRadius: 4,
        boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
      }}
      labelShowBg={true}
      labelBgStyle={{
        fill: "white",
        padding: 2,
        borderRadius: 4,
      }}
      labelBgBorderRadius={4}
    />
  );
}