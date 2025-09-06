# n8n Python SDK

A Python SDK for creating and managing n8n workflows programmatically.

## Overview

The n8n Python SDK provides a simple and intuitive way to create, modify, and export n8n workflows using Python code. Instead of manually creating workflows through the n8n interface, you can now define your automation workflows as code.

## Features

- **Programmatic Workflow Creation**: Create n8n workflows using Python classes and methods
- **Node Support**: Built-in support for popular n8n nodes including HTTP Request, Google Sheets, and Manual Trigger
- **JSON Export**: Export workflows to n8n-compatible JSON files
- **Workflow Import**: Import existing n8n workflows from JSON files
- **Validation**: Built-in validation to ensure workflows are properly configured
- **Type Hints**: Full type hint support for better development experience

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/n8n-python-sdk.git
cd n8n-python-sdk

# Install in development mode
pip install -e .
```

## Quick Start

```python
from n8n_python_sdk import Workflow, ManualTriggerNode, HTTPRequestNode, GoogleSheetsNode

# Create a new workflow
workflow = Workflow(name="My First Workflow")

# Add nodes
trigger = ManualTriggerNode(name="Manual Trigger")
http_node = HTTPRequestNode(
    name="Fetch Data",
    url="https://api.example.com/data",
    method="GET"
)
sheets_node = GoogleSheetsNode.append_or_update(
    name="Save to Sheets",
    document_id="your-sheet-id",
    sheet="Sheet1"
)

# Add nodes to workflow
workflow.add_nodes([trigger, http_node, sheets_node])

# Connect nodes
workflow.connect(trigger, http_node)
workflow.connect(http_node, sheets_node)

# Export to JSON
workflow.export("my_workflow.json")
```

## Supported Nodes

Currently supported n8n nodes:

- **ManualTriggerNode**: Manual trigger to start workflows
- **HTTPRequestNode**: Make HTTP requests to APIs
- **GoogleSheetsNode**: Read from and write to Google Sheets

More nodes will be added in future releases.

## Documentation

For detailed documentation and examples, see the [docs](docs/) directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.