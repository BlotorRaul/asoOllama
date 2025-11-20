# Instrucțiuni Testare Docker

## Pași pentru testare

### 1. Construirea imaginilor (dacă nu sunt deja construite)

```powershell
docker compose build
```

Această comandă va construi toate cele 3 imagini:
- `pythonproject1-ollama` - Ollama cu modelul llama3.2:1b
- `pythonproject1-mcp-server` - Serverul MCP
- `pythonproject1-adk-web` - ADK-Web cu agentul

**Timp estimat:** 5-10 minute (prima dată, pentru descărcarea dependențelor)

### 2. Pornirea tuturor serviciilor

```powershell
docker compose up -d
```

Această comandă va porni toate cele 3 containere în background.

### 3. Verificarea statusului

```powershell
docker compose ps
```

Ar trebui să vezi:
- `ollama-container` - STATUS: Up (healthy sau starting)
- `mcp-server-container` - STATUS: Up (healthy sau starting)
- `adk-web-container` - STATUS: Up (healthy sau starting)

### 4. Verificarea log-urilor

#### Pentru Ollama (verifică dacă descarcă modelul):
```powershell
docker compose logs -f ollama
```
Apasă `Ctrl+C` pentru a ieși din log-uri.

#### Pentru MCP Server:
```powershell
docker compose logs -f mcp-server
```

#### Pentru ADK-Web:
```powershell
docker compose logs -f adk-web
```

#### Pentru toate serviciile:
```powershell
docker compose logs -f
```

### 5. Accesarea serviciilor

#### ADK-Web (Interfața principală):
Deschide în browser: **http://localhost:8000**

Aici vei putea:
- Interacționa cu agentul AI
- Testa tool-urile MCP (list_directory, get_file_content)
- Face întrebări despre fișierele din folderul Test

#### MCP Server:
Endpoint: **http://localhost:8001/mcp**

#### Ollama:
Endpoint: **http://localhost:11434**

### 6. Testarea agentului

În interfața web de la `http://localhost:8000`, încearcă să întrebi:

1. **"Listează fișierele din folderul Test"**
   - Ar trebui să folosească tool-ul `list_directory`

2. **"Ce conține fișierul raul/fdgr.txt?"**
   - Ar trebui să folosească tool-ul `get_file_content`

3. **"Arată-mi structura folderului Test"**
   - Ar trebui să navigheze prin directoare

### 7. Oprirea serviciilor

```powershell
docker compose down
```

### 8. Oprirea și ștergerea volumelor (resetează totul)

```powershell
docker compose down -v
```

**Atenție:** Aceasta va șterge și datele Ollama (modelele descărcate).

### 9. Reconstruirea unei imagini (dacă ai modificat codul)

```powershell
docker compose build --no-cache <nume-serviciu>
```

Exemple:
```powershell
docker compose build --no-cache mcp-server
docker compose build --no-cache adk-web
docker compose build --no-cache ollama
```

### 10. Accesarea unui container (pentru debugging)

```powershell
docker compose exec <nume-serviciu> /bin/bash
```

Exemple:
```powershell
docker compose exec mcp-server /bin/bash
docker compose exec adk-web /bin/bash
docker compose exec ollama /bin/sh
```

## Comenzi utile

### Verificare rapidă status:
```powershell
docker compose ps
```

### Verificare ultimele log-uri (fără follow):
```powershell
docker compose logs --tail=50
```

### Restart un serviciu:
```powershell
docker compose restart <nume-serviciu>
```

### Stop un serviciu:
```powershell
docker compose stop <nume-serviciu>
```

### Start un serviciu:
```powershell
docker compose start <nume-serviciu>
```

## Troubleshooting

### Dacă un container nu pornește:
1. Verifică log-urile: `docker compose logs <nume-serviciu>`
2. Verifică dacă porturile sunt libere (8000, 8001, 11434)
3. Reconstruiește imaginea: `docker compose build --no-cache <nume-serviciu>`

### Dacă Ollama nu descarcă modelul:
- Modelul va fi descărcat automat la prima utilizare
- Poți verifica: `docker compose exec ollama ollama list`

### Dacă MCP Server este "unhealthy":
- Este normal! Serverul funcționează corect
- Healthcheck-ul returnează 406 pentru request-uri non-MCP, ceea ce este comportament normal

## Structura proiectului în Docker

- **Ollama**: Rulează pe portul 11434, descarcă modelul `llama3.2:1b`
- **MCP Server**: Rulează pe portul 8001, gestionează folderul `gggg/Test`
- **ADK-Web**: Rulează pe portul 8000, conectat la Ollama și MCP Server

Toate comunică prin rețeaua Docker `agent-network`.

