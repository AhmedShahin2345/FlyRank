import asyncio
import json
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_CMD = os.environ.get("MCP_CMD", "npx")
SERVER_ARGS = json.loads(os.environ.get("MCP_ARGS", '["-y","@modelcontextprotocol/server-filesystem","/tmp/mcp-test"]'))


async def main():
    async with stdio_client(StdioServerParameters(command=SERVER_CMD, args=SERVER_ARGS)) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"TOOLS ({len(tools.tools)} available to the server):")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description.splitlines()[0] if t.description else ''}")

            task = os.environ.get("TASK", "list")
            if task == "list":
                print("\n=== TASK 1: list the project directory ===")
                res = await session.call_tool("list_directory", {"path": "/tmp/mcp-test/project"})
                for c in res.content:
                    print(c.text)
            elif task == "read":
                print("\n=== TASK 2: read the budget notes file ===")
                res = await session.call_tool("read_text_file", {"path": "/tmp/mcp-test/project/budget-notes.txt"})
                for c in res.content:
                    print(c.text)
            elif task == "search":
                print("\n=== TASK 3: search the project for all notes files, then read file metadata ===")
                res = await session.call_tool("search_files", {"path": "/tmp/mcp-test/project", "pattern": "*.txt"})
                for c in res.content:
                    print(c.text)
                res2 = await session.call_tool("get_file_info", {"path": "/tmp/mcp-test/project/event-notes.txt"})
                for c in res2.content:
                    print(c.text)
            print("\nEach result above came from a real tool call through the MCP protocol — chat alone cannot read these files.")


if __name__ == "__main__":
    asyncio.run(main())