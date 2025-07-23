#!/bin/bash
set -euo pipefail

# Ensure the claude command is in PATH
export PATH="/usr/local/share/npm-global/bin:$PATH"

echo "Setting up MCP connection between Claude and task-master-ai..."
echo "For support or questions, please visit: https://aemalsayer.com"
echo ""

# Check if required environment variables are set
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable is not set"
    exit 1
fi

if [ -z "${PERPLEXITY_API_KEY:-}" ]; then
    echo "ERROR: PERPLEXITY_API_KEY environment variable is not set"
    exit 1
fi

# Function to check MCP connection status
check_mcp_connection() {
    local max_attempts=3
    local attempt=1
    
    echo "Verifying MCP connection status..."
    
    while [ $attempt -le $max_attempts ]; do
        echo "Checking connection (attempt $attempt/$max_attempts)..."
        
        # Get the MCP list output
        local mcp_output
        if mcp_output=$(claude mcp list 2>&1); then
            # Check if task-master-ai is in the list and get its status
            if echo "$mcp_output" | grep -q "task-master-ai"; then
                local status=$(echo "$mcp_output" | grep "task-master-ai" | awk '{print $NF}')
                echo "Found task-master-ai with status: $status"
                
                if [ "$status" = "Connected" ] || [ "$status" = "connected" ]; then
                    echo "✅ MCP connection verified successfully!"
                    return 0
                elif [ "$status" = "failed" ]; then
                    echo "❌ MCP connection failed. Status: $status"
                    if [ $attempt -eq $max_attempts ]; then
                        echo "Max attempts reached. Please check your configuration and try again."
                        return 1
                    fi
                else
                    echo "⏳ Connection status: $status (waiting...)"
                fi
            else
                echo "⚠️  task-master-ai not found in MCP list"
                if [ $attempt -eq $max_attempts ]; then
                    echo "Max attempts reached. The connection may not have been added properly."
                    return 1
                fi
            fi
        else
            echo "❌ Failed to get MCP list: $mcp_output"
            if [ $attempt -eq $max_attempts ]; then
                return 1
            fi
        fi
        
        if [ $attempt -lt $max_attempts ]; then
            echo "Waiting 3 seconds before next attempt..."
            sleep 3
        fi
        ((attempt++))
    done
    
    return 1
}

# Ensure Claude config directory exists
mkdir -p /home/node/.claude

# Add the MCP connection
echo "Adding task-master-ai MCP connection..."
claude mcp add --scope user task-master-ai \
  --env ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
  --env PERPLEXITY_API_KEY="${PERPLEXITY_API_KEY}" \
  -- npx -y --package=task-master-ai task-master-ai

echo "MCP connection added. Now verifying connection..."

# Verify the connection
if check_mcp_connection; then
    echo ""
    echo "🎉 MCP setup complete! You can now use task-master-ai through Claude MCP."
    echo "To see all your MCP connections, run: claude mcp list"
    echo ""
    echo "📧 Need help? Contact the author at: https://aemalsayer.com"
else
    echo ""
    echo "⚠️  MCP connection setup encountered issues."
    echo "You can manually check the connection status with: claude mcp list"
    echo "If needed, you can try removing and re-adding the connection:"
    echo "  claude mcp remove task-master-ai"
    echo "  sudo /usr/local/bin/setup-mcp.sh"
    echo ""
    echo "📧 Need help? Contact the author at: https://aemalsayer.com"
    exit 1
fi 