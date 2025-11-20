"""
Script pentru a rula adk-web cu agentul.
Folosește: python gggg/run_web.py
SAU: python -m gggg.run_web
"""
import sys
import os
from pathlib import Path

# Obține directorul root al proiectului
project_root = Path(__file__).resolve().parent.parent
agents_dir = project_root / "agents"

# Adaugă directorul root la path pentru importuri
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("=" * 60)
    print("Starting ADK Web server with root_agent...")
    print("=" * 60)
    
    # Verifică dacă directorul agents există
    if not agents_dir.exists():
        print(f"✗ Error: Agents directory not found at {agents_dir}")
        print("Please ensure the agents directory structure exists.")
        sys.exit(1)
    
    # Verifică agentul înainte de pornire
    try:
        from agents.root_agent.agent import root_agent
        print(f"✓ Agent name: {root_agent.name}")
        print(f"✓ Model: {root_agent.model}")
        print(f"✓ Tools available: {len(root_agent.tools) if hasattr(root_agent, 'tools') else 0}")
        print("=" * 60)
    except Exception as e:
        print(f"✗ Error importing agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Rulează adk-web folosind CLI-ul ADK
    print("\nStarting web server...")
    print("Access the web interface at the URL shown above (usually http://localhost:8000)")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Folosește subprocess pentru a rula adk-web CLI cu directorul agents
        import subprocess
        
        # Construiește comanda - specifică directorul agents și host-ul
        cmd = [
            sys.executable, 
            "-m", 
            "google.adk.cli", 
            "web",
            "--host", "0.0.0.0",  # Ascultă pe toate interfețele pentru Docker
            str(agents_dir)  # Specifică directorul agents ca AGENTS_DIR
        ]
        
        print(f"Running: {' '.join(cmd)}")
        print("=" * 60)
        
        # Rulează comanda
        result = subprocess.run(cmd, check=False)
        
        if result.returncode != 0:
            print(f"\n✗ Error: adk-web exited with code {result.returncode}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped by user.")
    except FileNotFoundError:
        print("\n✗ Error: Python executable not found")
        print(f"Python path: {sys.executable}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error running adk-web: {e}")
        print("\nPlease ensure:")
        print("  1. google-adk is installed: pip install google-adk")
        print("  2. You are running from the project root directory")
        print("  3. Virtual environment is activated (if using one)")
        import traceback
        traceback.print_exc()
        sys.exit(1)

