#!/bin/bash
set -euo pipefail

# Load environment variables from .env file
if [ -f "/workspace/.env" ]; then
    echo "Loading environment variables from .env file..."
    # Export variables from .env file
    export $(grep -v '^#' /workspace/.env | grep -v '^$' | xargs)
else
    echo "ERROR: .env file not found at /workspace/.env"
    echo "Please copy .env.example to .env and fill in your API keys"
    exit 1
fi

# Validate that required API keys are set and not placeholder values
if [ -z "${ANTHROPIC_API_KEY:-}" ] || [ "${ANTHROPIC_API_KEY}" = "sk-ant-api03-your_key_here" ]; then
    echo "ERROR: ANTHROPIC_API_KEY is not set or still contains placeholder value"
    echo "Please edit /workspace/.env and set your actual Anthropic API key"
    exit 1
fi

if [ -z "${PERPLEXITY_API_KEY:-}" ] || [ "${PERPLEXITY_API_KEY}" = "pplx-your_key_here" ]; then
    echo "ERROR: PERPLEXITY_API_KEY is not set or still contains placeholder value"
    echo "Please edit /workspace/.env and set your actual Perplexity API key"
    exit 1
fi

# Add npm global bin to PATH
export PATH="/usr/local/share/npm-global/bin:$PATH"

# Run the original setup script with the loaded environment
exec /usr/local/bin/setup-mcp.sh