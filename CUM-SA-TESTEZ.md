# Cum să Testezi Proiectul Docker

## 1. Pornirea Serviciilor

```powershell
docker compose up -d
```

## 2. Verificarea Statusului

```powershell
docker compose ps
```

Ar trebui să vezi:
- `ollama-container` - Up (healthy)
- `mcp-server-container` - Up 
- `adk-web-container` - Up (healthy)

## 3. Accesarea Interfeței Web

Deschide în browser: **http://localhost:8000**

Ar trebui să vezi interfața "Agent Development Kit Dev UI".

## 4. Testarea Agentului

În interfața web, încearcă să întrebi:

### Test 1: Listare directoare
```
Listează fișierele din folderul Test
```

### Test 2: Citire fișier
```
Ce conține fișierul raul/fdgr.txt?
```

### Test 3: Navigare structură
```
Arată-mi structura folderului Test
```

### Test 4: Informații despre fișiere
```
Câte fișiere sunt în folderul raul?
```

## 5. Verificarea Log-urilor

### Toate serviciile:
```powershell
docker compose logs -f
```

### Un serviciu specific:
```powershell
docker compose logs -f adk-web
docker compose logs -f mcp-server
docker compose logs -f ollama
```

## 6. Verificarea Conectivității

### Test ADK-Web:
```powershell
curl http://localhost:8000
```

### Test MCP Server:
```powershell
curl http://localhost:8001/mcp
```

### Test Ollama:
```powershell
curl http://localhost:11434/api/tags
```

## 7. Oprirea Serviciilor

```powershell
docker compose down
```

## Ce Să Cauți în Interfața Web

1. **Interfața de chat** - unde poți scrie întrebări
2. **Răspunsuri de la agent** - ar trebui să folosească tool-urile MCP
3. **Istoric conversații** - pentru a vedea interacțiunile
4. **Tool-uri disponibile** - ar trebui să vezi `list_directory` și `get_file_content`

## Troubleshooting

### Dacă interfața nu se încarcă:
1. Verifică că containerul rulează: `docker compose ps`
2. Verifică log-urile: `docker compose logs adk-web`
3. Încearcă hard refresh: `Ctrl+F5`
4. Verifică firewall-ul pentru portul 8000

### Dacă agentul nu răspunde:
1. Verifică că Ollama rulează: `docker compose logs ollama`
2. Verifică că MCP Server rulează: `docker compose logs mcp-server`
3. Verifică log-urile agentului: `docker compose logs adk-web`

### Dacă tool-urile nu funcționează:
1. Verifică conectarea la MCP Server în log-uri
2. Verifică că folderul Test este montat corect
3. Verifică log-urile MCP Server pentru erori

