import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

# Configurare prin variabile de mediu (pentru Docker) cu default-uri pentru local
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8001/mcp")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

# Setare variabila de mediu pentru LiteLLM (daca Ollama ruleaza pe alt URL)
if OLLAMA_BASE_URL != "http://127.0.0.1:11434":
    os.environ["OLLAMA_API_BASE"] = OLLAMA_BASE_URL

toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MCP_SERVER_URL
    )
)

# Configurare model Ollama
model_config = f"ollama_chat/{OLLAMA_MODEL}"

root_agent = LlmAgent(
    name="root_agent",
    model=LiteLlm(model=model_config),
    description=(
        "Agent to help with file system operations like reading files and listing directories."
    ),
    instruction=(
        "You are a helpful agent who can read file contents and list directory contents. "
        "Use the available tools to help users navigate and understand their file system."
    ),
    tools=[toolset],
)