from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

import asyncio
import os
from dotenv import load_dotenv
load_dotenv("./projects/.env")

MCP_SERVER_ABS_PATH = os.getenv("MCP_SERVER_ABS_PATH")
server_params = StdioServerParameters(
    command="python",
    args=[MCP_SERVER_ABS_PATH], # must be abs path
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent("openai:gpt-4.1", tools)
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    return agent_response

if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)