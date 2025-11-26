#!/bin/sh
# Script pentru initializarea Ollama si preincarcarea modelului

echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to start..."
sleep 10

echo "Pulling model llama3.2:1b..."
ollama pull llama3.2:1b || echo "Warning: Failed to pull model, it will be pulled on first use"

# Verificam daca modelul a fost preincarcat
sleep 2
if ollama list 2>/dev/null | grep -q "llama3.2:1b"; then
    echo "✓ Model llama3.2:1b successfully loaded"
else
    echo "ℹ Model will be pulled on first use"
fi

wait $OLLAMA_PID

