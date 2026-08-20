import { NextRequest, NextResponse } from "next/server";
import { inngest } from "@/lib/inngest";

export async function POST(request: NextRequest) {
  try {
    const { nodes, edges } = await request.json();
    
    if (!nodes || !edges) {
      return NextResponse.json(
        { success: false, error: "Missing nodes or edges" },
        { status: 400 }
      );
    }

    // Send event to Inngest
    await inngest.send({
      name: "workflow/execute",
      data: { nodes, edges },
    });

    return NextResponse.json({
      success: true,
      message: "Workflow execution started",
    });
  } catch (error) {
    console.error("Failed to start workflow:", error);
    return NextResponse.json(
      { success: false, error: "Failed to start workflow execution" },
      { status: 500 }
    );
  }
}