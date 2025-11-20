import os
import logging
from fastmcp import FastMCP
from pathlib import Path


logging.basicConfig(level=logging.INFO)

mcp = FastMCP("ASO Test Folder MCP")

# Configurare prin variabile de mediu (pentru Docker) cu default pentru local
BASE_DIR = Path(os.getenv("MCP_BASE_DIR", str(Path(__file__).resolve().parent / "Test")))
BASE_DIR.mkdir(parents=True, exist_ok=True)

@mcp.tool()
def list_directory(dir_path: str = ".") -> list[str]:
    """Return the list of files and directories in the Test folder."""
    try:
        path = (BASE_DIR / dir_path).resolve()
        if not path.exists():
            return [f"Eroare: directorul {dir_path} nu există."]
        if not path.is_dir():
            return [f"Eroare: {dir_path} nu este un director."]
        return [p.name for p in path.iterdir()]
    except Exception as e:
        return [f"Eroare: {e}"]

@mcp.tool()
def get_file_content(file_path: str) -> str:
    """Return the content of a file from the Test folder."""
    try:
        path = (BASE_DIR / file_path).resolve()
        if not path.exists():
            return f"Eroare: fișierul {file_path} nu există."
        if not path.is_file():
            return f"Eroare: {file_path} nu este un fișier."
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Eroare: {e}"

if __name__ == "__main__":
    # Configurare port și host prin variabile de mediu
    PORT = int(os.getenv("MCP_PORT", "8001"))
    HOST = os.getenv("MCP_HOST", "0.0.0.0")
    
    logging.info(f"Server started in folder: {BASE_DIR}")
    logging.info(f"Server listening on {HOST}:{PORT}")
    mcp.run(transport="streamable-http", port=PORT, host=HOST)
