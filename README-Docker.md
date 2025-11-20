# Dockerizare - System Administrator Agent

Acest proiect conține trei containere Docker care rulează împreună pentru a oferi un agent AI administrator de sistem.

## Structura

- **Ollama Container**: Rulează Ollama cu modelul `llama3.2:1b`
- **MCP Server Container**: Rulează serverul MCP pentru gestionarea fișierelor
- **ADK-Web Container**: Rulează interfața web ADK cu agentul AI

## Cerințe

- Docker
- Docker Compose

## Utilizare

### 1. Construirea imaginilor

```bash
docker-compose build
```

### 2. Pornirea tuturor serviciilor

```bash
docker-compose up -d
```

### 3. Verificarea statusului

```bash
docker-compose ps
```

### 4. Vizualizarea log-urilor

```bash
# Toate serviciile
docker-compose logs -f

# Un serviciu specific
docker-compose logs -f ollama
docker-compose logs -f mcp-server
docker-compose logs -f adk-web
```

### 5. Oprirea serviciilor

```bash
docker-compose down
```

### 6. Oprirea și ștergerea volumelor

```bash
docker-compose down -v
```

## Accesare servicii

- **ADK-Web**: http://localhost:8000
- **MCP Server**: http://localhost:8001/mcp
- **Ollama**: http://localhost:11434

## Configurare

Variabilele de mediu pot fi modificate în `docker-compose.yml`:

- `MCP_SERVER_URL`: URL-ul serverului MCP (default: `http://mcp-server:8001/mcp`)
- `OLLAMA_BASE_URL`: URL-ul serverului Ollama (default: `http://ollama:11434`)
- `OLLAMA_MODEL`: Modelul Ollama folosit (default: `llama3.2:1b`)

## Volume-uri

- `ollama-data`: Stochează modelele Ollama (persistent)
- `./gggg/Test:/app/data`: Directorul de date pentru MCP Server (montat din host)

## Troubleshooting

### Verificarea healthcheck-urilor

```bash
docker-compose ps
```

### Reconstruirea unei imagini

```bash
docker-compose build --no-cache <service-name>
```

### Accesarea unui container

```bash
docker-compose exec <service-name> /bin/bash
```

