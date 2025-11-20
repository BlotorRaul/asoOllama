#!/bin/sh
# Script pentru inițializarea Ollama și preîncărcarea modelului

echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Așteptăm ca Ollama să pornească
echo "Waiting for Ollama to start..."
sleep 10

# Preîncărcăm modelul llama3.2:1b
echo "Pulling model llama3.2:1b..."
ollama pull llama3.2:1b || echo "Warning: Failed to pull model, it will be pulled on first use"

# Verificăm dacă modelul a fost preîncărcat
sleep 2
if ollama list 2>/dev/null | grep -q "llama3.2:1b"; then
    echo "✓ Model llama3.2:1b successfully loaded"
else
    echo "ℹ Model will be pulled on first use"
fi

# Așteptăm ca procesul Ollama să continue
wait $OLLAMA_PID

