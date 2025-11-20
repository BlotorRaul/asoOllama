import logging
from fastmcp import FastMCP
from pathlib import Path


logging.basicConfig(level=logging.INFO)

mcp = FastMCP("ASO Test Folder MCP")

BASE_DIR = Path(__file__).resolve().parent / "Test"
BASE_DIR.mkdir(exist_ok=True)

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

    logging.info(f"Server started in folder: {BASE_DIR}")
    mcp.run(transport="streamable-http", port=8001, host="0.0.0.0")
