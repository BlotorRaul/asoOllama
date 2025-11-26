import os
import sys
from pathlib import Path

# Adauga directorul root al proiectului la path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

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
        "You have access to two tools:\n"
        "1. list_directory(dir_path) - Lists files and directories in a folder. "
        "   - Use '.' or empty string for the root folder (Test folder)\n"
        "   - Use relative paths like 'ana' or 'raul' for subdirectories\n"
        "   - When user asks about 'Test' folder, use '.' as dir_path\n"
        "   - Always call this tool when user asks what files exist or what's in a folder\n"
        "2. get_file_content(file_path) - Reads the content of a file\n"
        "   - Use relative paths like 'readme.txt' or 'ana/info.txt'\n"
        "   - Always call this tool when user asks about file contents\n\n"
        "IMPORTANT: When a user asks about files or folders, you MUST call the appropriate tool. "
        "Do not just describe what you think might be there - actually call list_directory or get_file_content "
        "to get the real information. The Test folder is mounted at the root, so use '.' to list its contents. "
        "If the user mentions '/app/Test' or '/Test', they mean the root folder - use '.' as the path parameter."
    ),
    tools=[toolset],
)

