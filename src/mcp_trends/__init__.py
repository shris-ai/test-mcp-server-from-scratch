# mcp_trends/__init__.py


#from .server import app, cli_run as run_server

#__all__ = ["app", "run_server"]


'''
#from .server import  run
from .server import run_mcp_dev as run
import asyncio

def main():
    """Main entry point for the package."""
    asyncio.run(run())

# Optionally expose other important items at package level
__all__ = ['main', 'server']

'''

from .server import run

def main():
    """Main entry point for the package."""
    import asyncio
    import sys
    
    async def run_main():
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            from .server import server as server_instance
            from mcp.server.models import InitializationOptions
            from mcp.server.lowlevel import NotificationOptions
            init_options = InitializationOptions(
                server_name="mcp-trends",
                server_version="0.1.0",
                capabilities=server_instance.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
    
            await run(read_stream, write_stream, init_options)
    
    asyncio.run(run_main())

__all__ = ['main', 'run']

'''
from .server import app, cli_run as run_server

__all__ = ["app", "run_server"]

# For direct execution
def main():
    import sys
    import asyncio
    from mcp_trends.server import main as srv_main
    asyncio.run(srv_main(sys.stdin.buffer, sys.stdout.buffer, {}))

if __name__ == "__main__":
    main()
'''
