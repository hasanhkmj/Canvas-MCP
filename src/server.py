from fastmcp import FastMCP
from .tools import courses, content, assignments, social

def create_server():
    mcp = FastMCP("canvas-mcp")
    
    # Register tools from modules
    courses.register_tools(mcp)
    content.register_tools(mcp)
    assignments.register_tools(mcp)
    social.register_tools(mcp)
    
    return mcp

mcp = create_server()

def main():
    mcp.run(transport="sse", port=2222)

if __name__ == "__main__":
    main()
