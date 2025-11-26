import os
import logging
from fastmcp import FastMCP
from pathlib import Path


logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to see all requests
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Set logger for mcp.server to see all MCP requests
mcp_logger = logging.getLogger("mcp.server")
mcp_logger.setLevel(logging.DEBUG)

mcp = FastMCP("ASO Test Folder MCP")

# Configurare prin variabile de mediu (pentru Docker) cu default pentru local
BASE_DIR = Path(os.getenv("MCP_BASE_DIR", str(Path(__file__).resolve().parent / "Test")))
BASE_DIR.mkdir(parents=True, exist_ok=True)

@mcp.tool()
def list_directory(dir_path: str = ".") -> list[str]:
    """List files and directories. Use "." for root folder, or a relative path like "ana" or "raul/fdgr.txt"."""
    logger = logging.getLogger(__name__)
    try:
        original_path = dir_path
        logger.info(f"=== list_directory CALLED with: '{dir_path}' ===")
        print(f"=== list_directory CALLED with: '{dir_path}' ===", flush=True)
        
        # Normalizează path-ul: gestionează path-uri absolute care încep cu /app/
        if dir_path.startswith("/app/"):
            # Elimină /app/ și normalizează
            dir_path = dir_path[5:]  # Elimină "/app/"
            logger.info(f"  After removing /app/: '{dir_path}'")
            print(f"  After removing /app/: '{dir_path}'", flush=True)
            # Dacă este "Test" sau "data" sau gol, înseamnă root folder
            if dir_path.lower().rstrip("/") in ["test", "data", ""]:
                dir_path = "."
                logger.info(f"  Normalized to root: '{dir_path}'")
                print(f"  Normalized to root: '{dir_path}'", flush=True)
        elif dir_path.startswith("/"):
            dir_path = dir_path[1:]  # Elimină "/" de la început
            logger.info(f"  After removing leading /: '{dir_path}'")
            print(f"  After removing leading /: '{dir_path}'", flush=True)
        
        # Dacă path-ul este "Test" sau "Test/", înseamnă că vrea folderul root (BASE_DIR)
        if dir_path.lower().rstrip("/") in ["test", ""]:
            dir_path = "."
            logger.info(f"  Normalized 'Test' to root: '{dir_path}'")
            print(f"  Normalized 'Test' to root: '{dir_path}'", flush=True)
        
        if dir_path.startswith(".."):
            logger.error(f"  Path traversal detected: '{dir_path}'")
            print(f"  Path traversal detected: '{dir_path}'", flush=True)
            return [f"Eroare: path-ul {dir_path} nu este permis (path traversal)."]
        
        logger.info(f"  Final normalized path: '{dir_path}'")
        logger.info(f"  BASE_DIR: {BASE_DIR.resolve()}")
        print(f"  Final normalized path: '{dir_path}'", flush=True)
        print(f"  BASE_DIR: {BASE_DIR.resolve()}", flush=True)
        
        # Construiește path-ul relativ la BASE_DIR
        path = BASE_DIR / dir_path
        path_resolved = path.resolve()
        logger.info(f"  Constructed path: {path}")
        logger.info(f"  Resolved path: {path_resolved}")
        logger.info(f"  Path exists: {path_resolved.exists()}")
        print(f"  Constructed path: {path}", flush=True)
        print(f"  Resolved path: {path_resolved}", flush=True)
        print(f"  Path exists: {path_resolved.exists()}", flush=True)
        
        # Verifică că path-ul este în interiorul BASE_DIR (prevenire path traversal)
        try:
            path_resolved.relative_to(BASE_DIR.resolve())
            logger.info(f"  Path is within BASE_DIR: OK")
            print(f"  Path is within BASE_DIR: OK", flush=True)
        except ValueError:
            logger.error(f"  Path traversal detected: {path_resolved} not in {BASE_DIR.resolve()}")
            print(f"  Path traversal detected: {path_resolved} not in {BASE_DIR.resolve()}", flush=True)
            return [f"Eroare: path-ul {dir_path} nu este permis (path traversal)."]
        
        if not path_resolved.exists():
            logger.error(f"  Directory does not exist: {path_resolved}")
            print(f"  Directory does not exist: {path_resolved}", flush=True)
            return [f"Eroare: directorul {dir_path} nu există."]
        if not path_resolved.is_dir():
            logger.error(f"  Path is not a directory: {path_resolved}")
            print(f"  Path is not a directory: {path_resolved}", flush=True)
            return [f"Eroare: {dir_path} nu este un director."]
        
        items = [p.name for p in path_resolved.iterdir()]
        logger.info(f"  Found {len(items)} items: {items}")
        print(f"  Found {len(items)} items: {items}", flush=True)
        return items
    except Exception as e:
        logger.error(f"  Exception in list_directory: {e}", exc_info=True)
        print(f"  Exception in list_directory: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return [f"Eroare: {e}"]

@mcp.tool()
def get_file_content(file_path: str) -> str:
    """Get the content of a file. Use relative paths like "readme.txt" or "ana/info.txt"."""
    try:
        original_path = file_path
        # Normalizează path-ul: gestionează path-uri absolute care încep cu /app/
        if file_path.startswith("/app/"):
            # Elimină /app/ și normalizează
            file_path = file_path[5:]  # Elimină "/app/"
            # Dacă începe cu "Test/" sau "data/", elimină prefixul
            if file_path.startswith("Test/"):
                file_path = file_path[5:]  # Elimină "Test/"
            elif file_path.startswith("data/"):
                file_path = file_path[5:]  # Elimină "data/"
        elif file_path.startswith("/"):
            file_path = file_path[1:]  # Elimină "/" de la început
        
        if file_path.startswith(".."):
            return f"Eroare: path-ul {file_path} nu este permis (path traversal)."
        
        logging.info(f"get_file_content: original='{original_path}' -> normalized='{file_path}'")
        
        # Construiește path-ul relativ la BASE_DIR
        path = BASE_DIR / file_path
        # Resolve doar pentru a normaliza, dar verifică că rămâne în BASE_DIR
        path = path.resolve()
        
        # Verifică că path-ul este în interiorul BASE_DIR (prevenire path traversal)
        try:
            path.relative_to(BASE_DIR.resolve())
        except ValueError:
            return f"Eroare: path-ul {file_path} nu este permis (path traversal)."
        
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
    
    # Verifică că BASE_DIR există și are conținut
    BASE_DIR_abs = BASE_DIR.resolve()
    logging.info(f"Server started in folder: {BASE_DIR_abs}")
    logging.info(f"BASE_DIR exists: {BASE_DIR_abs.exists()}")
    if BASE_DIR_abs.exists():
        try:
            items = list(BASE_DIR_abs.iterdir())
            logging.info(f"BASE_DIR contains {len(items)} items: {[item.name for item in items]}")
        except Exception as e:
            logging.warning(f"Could not list BASE_DIR contents: {e}")
    else:
        logging.warning(f"BASE_DIR does not exist! Creating it...")
        BASE_DIR_abs.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Server listening on {HOST}:{PORT}")
    mcp.run(transport="streamable-http", port=PORT, host=HOST)
