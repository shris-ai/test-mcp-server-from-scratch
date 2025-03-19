import json
import logging
from typing import Any
import os
from collections.abc import Sequence
import mcp
from mcp.server import Server
from mcp.types import(
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)
from mcp.shared.exceptions import McpError
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
from dotenv import load_dotenv
from . import tools

load_dotenv()

logging.basicConfig(
    filename="mcp_trends.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp-trends")

server = Server("mcp-trends-server")

tool_handlers={}
def add_tool_handler(tool_class: tools.ToolHandler):
    global tool_handlers
    logger.debug(f"Registering tool handler: {tool_class.name}")
    tool_handlers[tool_class.name] = tool_class
    logger.debug(f"Registered tool_handlers: {tool_handlers}")

def get_tool_handler(name:str) -> tools.ToolHandler | None:
    logger.debug(f"Looking for tool handler: {name}")
    if name not in tool_handlers:
        logger.warning(f"Tool Handler '{name}' not found.")
        return None
    return tool_handlers[name]

# Register 
add_tool_handler(tools.CreateToolHandler_GetTrends_InterestByRegion())

@server.list_tools()
async def list_tools() -> list[Tool]:
    logger.debug("Listing all available tools...")
    return [th.get_tool_description() for th in tool_handlers.values()]

@server.call_tool()
async def call_tool(name:str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    logger.info(f"Calling tool '{name}' with arguments {arguments}")

    if not isinstance(arguments, dict):
        logger.error("Arguments must be dictionary")
        raise RuntimeError("arguments must be dictionary")

    tool_handler = get_tool_handler(name)
    print(tool_handler)
    if not tool_handler:
        logger.error(f"Unknown tool: {name}")
        raise ValueError(f"Unknown tool: {name}")

    try:
        print(f"Running tool {name}")
        logger.debug(f"Running tool {name}")
        return TextContent(text=tool_handler.run_tool(arguments))
    except Exception as e:
        logger.error(f"Error running tool: {str(e)}")
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")
    
'''
async def run():
    logger.info("Starting Trends MCP server")
    # Import here to avoid issues with event loops
    #from mcp.server.stdio import stdio_server

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
    
        await server.run(
            read_stream,
            write_stream,
            #server.create_initialization_options()
            InitializationOptions(
                server_name="mcp-trends",
                server_version="0.0.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
 '''       
  
# Add this new function for mcp dev
async def run_mcp_dev(read_stream, write_stream, initialization_options):
    logger.info("Starting Trends MCP server via mcp dev")
    await server.run(
        read_stream,
        write_stream,
        initialization_options
    )
    
async def run(read_stream, write_stream, initialization_options):
    logger.info("Starting Trends MCP server via mcp dev")
    await server.run(
        read_stream,
        write_stream,
        initialization_options
    )