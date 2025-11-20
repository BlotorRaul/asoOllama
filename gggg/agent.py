from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://127.0.0.1:8001/mcp"
    )
)

root_agent = LlmAgent(
    name="root_agent",
    model=LiteLlm(model="ollama_chat/llama3.2:1b"),
    description=(
        "Agent to help with file system operations like reading files and listing directories."
    ),
    instruction=(
        "You are a helpful agent who can read file contents and list directory contents. "
        "Use the available tools to help users navigate and understand their file system."
    ),
    tools=[toolset],
)