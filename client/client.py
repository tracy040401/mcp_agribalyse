import sys
import asyncio
import os
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

# Load environment variables from .env
load_dotenv()


class MCPClient:
    def __init__(self, api_key: str):
        # Initialize OpenAI client and exit stack for MCP contexts
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None
        
    async def connect_to_server(self):
        """Start the MCP server and initialize the session."""
        # Determine command based on script type
        cmd = "python"
        params = StdioServerParameters(command=cmd, args=["server/server.py"])

        # Enter stdio_client and ClientSession contexts, keep open until cleanup
        read, write = await self.exit_stack.enter_async_context(stdio_client(params))
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )

        # Initialize MCP session and list tools
        await self.session.initialize()
         # 📌 Charger les tools
        tools_resp = await self.session.list_tools()
        self.tools = tools_resp.tools

        # 📌 Charger les resources
        res_resp = await self.session.list_resources()
        self.resources = res_resp.resources

            
    async def process_query(self, query: str) -> str:
        """Send a user query to gpt-4o, handle any tool call, and return GPT's answer."""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        # List MCP tools and resources and build function definitions for GPT
        tools = (await self.session.list_tools()).tools
        tool_defs = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in tools
        ]
        
        resources = await self.session.list_resources()
        print(resources)
        
        # Build initial conversation messages
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant with access to live-news tools. "
                    "When asked for information, you can use these tools to get the most "
                    "If you need some parameters, please use ressources to get parameters before calling the right tool."
                ),
            },
            {"role": "user", "content": query},
        ]

        # 1) Initial call to GPT-4o with tool definitions
        resp = await self.openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tool_defs,
            tool_choice="auto",
        )

        msg = resp.choices[0].message

        # 2) If GPT decided to call a tool
        if msg.tool_calls:
            call = msg.tool_calls[0].function
            name = call.name
            args = json.loads(call.arguments or "{}")
            print(f"Calling tool: {name} with args: {args}")

            # Execute the tool via MCP
            result = await self.session.call_tool(name, args)

            # Add the tool response back into the conversation
            messages.append({
                "role": "function",
                "name": name,
                "content": result.content,
            })

            # 3) Follow-up GPT call to incorporate the tool result
            followup = await self.openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            return followup.choices[0].message.content or ""

        # 4) No tool call: return GPT's direct answer
        return msg.content or ""
    
    async def chat_loop(self):
        """Interactive REPL: read queries, process them, print answers."""
        print("MCP-powered News Chat (type 'quit' to exit)")
        while True:
            q = input("\n> ").strip()
            if not q or q.lower() == "quit":
                break
            try:
                ans = await self.process_query(q)
                print("\n" + ans)
            except Exception as e:
                print("Error:", e)
        
    async def cleanup(self):
        """Close all MCP contexts and sessions."""
        await self.exit_stack.aclose()
        
async def main():

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY in your environment.")
        sys.exit(1)

    client = MCPClient(api_key)
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())