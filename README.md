# n8n Python SDK

A comprehensive Python SDK for programmatically creating and managing n8n workflows. This SDK enables developers to define n8n workflows using Python code, eliminating the need to manually configure workflows in the n8n GUI.

## Overview

The n8n Python SDK provides a fluent API for building automation workflows that can be exported as JSON files compatible with n8n. Whether you're creating simple API integrations or complex data processing pipelines, this SDK makes it easy to define, validate, and export workflows programmatically.

**Key Features:**

- 🔧 **Programmatic Workflow Creation** - Define workflows using Python code instead of GUI
- 🧩 **Multiple Node Types** - Support for Manual Triggers, HTTP Requests, Google Sheets, and more
- ✅ **Built-in Validation** - Comprehensive workflow and node validation with detailed error messages
- 📋 **Error Handling** - Custom exception hierarchy with specific error codes for debugging
- 📊 **Logging System** - Configurable logging with multiple output options and levels
- 🔄 **JSON Export/Import** - Full compatibility with n8n workflow JSON format
- 🧪 **Extensive Testing** - Comprehensive test suites covering all functionality
- 📖 **Rich Documentation** - Detailed guides and examples for all features

![n8n Python SDK Workflow Creation](images/00-vibebox.jpeg)

## Quick Start

### Installation

Clone this repository and include it in your project:

```bash
git clone https://github.com/yourusername/n8n-python-sdk.git
cd n8n-python-sdk
```

### Basic Usage

```python
from n8n_python_sdk import (
    Workflow, 
    ManualTriggerNode, 
    HTTPRequestNode, 
    GoogleSheetsNode,
    configure_logging
)

# Configure logging (optional)
configure_logging(level='INFO')

# Create a new workflow
workflow = Workflow("My API to Sheets Workflow")

# Create nodes
trigger = ManualTriggerNode(name="Start Process")
api_call = HTTPRequestNode(
    name="Fetch User Data",
    url="https://jsonplaceholder.typicode.com/users"
)
sheets_node = GoogleSheetsNode.append_or_update(
    name="Save to Google Sheets",
    document_id="your-google-sheet-id-here",
    sheet_name="Sheet1",
    columns={
        "mappingMode": "defineBelow",
        "value": {
            "name": "={{ $json.name }}",
            "email": "={{ $json.email }}",
            "phone": "={{ $json.phone }}"
        },
        "matchingColumns": ["email"]
    }
)

# Build the workflow
workflow.add_nodes(trigger, api_call, sheets_node)
workflow.connect(trigger, api_call)
workflow.connect(api_call, sheets_node)

# Export to n8n format
workflow.export("my_workflow.json")
print("✅ Workflow created and exported successfully!")
```

## 🚀 Getting Started

### Run the Sample Workflow

The easiest way to see the SDK in action:

```bash
python3 main.py
```

This creates a complete workflow (Manual Trigger → HTTP Request → Google Sheets) and exports it to `n8n-workflows/workflow.json`.

### Interactive Usage

```bash
python3
```

Then in the Python REPL:

```python
>>> from n8n_python_sdk import Workflow, ManualTriggerNode
>>> workflow = Workflow("Interactive Test")
>>> trigger = ManualTriggerNode(name="Click to Start")
>>> workflow.add_node(trigger)
>>> workflow.export("interactive_test.json")
>>> print(f"Created workflow with {len(workflow.nodes)} nodes")
```

## 🧩 Supported Node Types

### Manual Trigger Node
Perfect for workflows that need to be started manually:

```python
trigger = ManualTriggerNode(name="Manual Start")
```

### HTTP Request Node
For API calls and web requests:

```python
http_node = HTTPRequestNode(
    name="API Call",
    url="https://api.example.com/data",
    method="GET",  # GET, POST, PUT, DELETE, etc.
    headers={"Authorization": "Bearer token"},
    query_parameters={"limit": "100"}
)
```

### Google Sheets Node
For Google Sheets integration:

```python
sheets_node = GoogleSheetsNode.append_or_update(
    name="Update Sheet",
    document_id="your-sheet-id",
    sheet_name="Sheet1",
    columns={
        "mappingMode": "defineBelow",
        "value": {
            "name": "={{ $json.name }}",
            "email": "={{ $json.email }}"
        }
    }
)
```

## 🔧 Advanced Features

### Error Handling

The SDK provides comprehensive error handling with custom exceptions:

```python
from n8n_python_sdk.exceptions import WorkflowError, NodeError, ValidationError

try:
    workflow = Workflow("My Workflow")
    # ... workflow operations ...
    workflow.export("output.json", validate=True)
except WorkflowError as e:
    print(f"Workflow error: {e} (Code: {e.code})")
except ValidationError as e:
    print(f"Validation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Logging Configuration

Configure logging to monitor SDK operations:

```python
from n8n_python_sdk.logging_config import (
    configure_logging, 
    enable_debug_logging,
    set_log_level
)

# Basic configuration
configure_logging(level='INFO')

# Advanced configuration with file output
configure_logging(
    level='DEBUG',
    enable_file_logging=True,
    log_file_path='n8n_sdk.log',
    max_file_size=10*1024*1024  # 10MB
)

# Quick debug mode
enable_debug_logging()

# Change log level dynamically
set_log_level('WARNING')
```

### Workflow Validation

Validate workflows before export:

```python
# Manual validation
errors = workflow.validate()
if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ Workflow is valid!")

# Automatic validation during export
workflow.export("workflow.json", validate=True)  # Raises exception if invalid
```

## 🧪 Testing

The SDK includes comprehensive test suites:

```bash
# Test all functionality and error handling
python3 test_error_handling.py

# Test package imports and API
python3 test_package_imports.py

# Test cross-context imports
cd test_contexts
python3 test_from_subdirectory.py
python3 test_multiple_contexts.py
```

All tests should pass with ✅ status indicators.

## 📁 Project Structure

```
n8n_python_sdk/
├── __init__.py                    # Public API exports
├── workflow.py                    # Main Workflow class
├── node.py                        # Base Node class
├── exceptions.py                  # Custom exception classes
├── logging_config.py              # Logging utilities
├── nodes/                         # Specialized node implementations
│   ├── manual_trigger.py
│   ├── http_request.py
│   └── google_sheets.py
└── utils/                         # Utility modules
    └── json_parser.py

examples/
├── main.py                        # Sample workflow creation
├── test_error_handling.py         # Error handling examples
└── test_package_imports.py        # Import testing

documentation/
└── LOGGING_AND_ERROR_HANDLING.md  # Comprehensive guides
```

## 🎯 Use Cases

### Simple API Integration
```python
# Fetch data from an API and process it
workflow = Workflow("API Integration")
trigger = ManualTriggerNode(name="Start")
fetch = HTTPRequestNode(name="Get Data", url="https://api.example.com/users")

workflow.add_nodes(trigger, fetch)
workflow.connect(trigger, fetch)
workflow.export("api_integration.json")
```

### Data Pipeline
```python
# Multi-step data processing pipeline
workflow = Workflow("Data Pipeline")
trigger = ManualTriggerNode(name="Start Pipeline")
extract = HTTPRequestNode(name="Extract Data", url="https://source-api.com/data")
transform = HTTPRequestNode(name="Transform", url="https://processor.com/transform", method="POST")
load = GoogleSheetsNode.append_or_update(name="Load to Sheets", document_id="sheet-id")

workflow.add_nodes(trigger, extract, transform, load)
workflow.connect(trigger, extract)
workflow.connect(extract, transform)
workflow.connect(transform, load)
workflow.export("data_pipeline.json")
```

### Batch Processing
```python
# Create multiple similar workflows programmatically
for api_endpoint in ["users", "posts", "comments"]:
    workflow = Workflow(f"Process {api_endpoint.title()}")
    trigger = ManualTriggerNode(name=f"Start {api_endpoint}")
    api_call = HTTPRequestNode(
        name=f"Fetch {api_endpoint}",
        url=f"https://jsonplaceholder.typicode.com/{api_endpoint}"
    )
    
    workflow.add_nodes(trigger, api_call)
    workflow.connect(trigger, api_call)
    workflow.export(f"{api_endpoint}_workflow.json")
```

## 🔍 Troubleshooting

### Import Issues
If you encounter import errors, ensure the SDK is in your Python path:

```python
import sys
import os
sys.path.insert(0, '/path/to/n8n-python-sdk')

from n8n_python_sdk import Workflow
```

### Validation Errors
Common validation issues and solutions:

- **Empty workflow name**: Provide a non-empty name when creating workflows
- **No nodes**: Add at least one node to the workflow before exporting
- **Invalid connections**: Ensure both nodes exist in the workflow before connecting them
- **Duplicate node IDs**: Each node must have a unique ID within the workflow

### Logging Issues
If logging isn't working:

```python
# Ensure logging is configured
from n8n_python_sdk.logging_config import configure_logging
configure_logging(level='DEBUG')  # Use DEBUG for maximum visibility
```

## 📈 Extensibility

The SDK is designed for easy extension with new node types:

```python
from n8n_python_sdk import Node

class SlackNode(Node):
    def __init__(self, name: str, channel: str, message: str):
        super().__init__(
            node_type="n8n-nodes-base.slack",
            name=name,
            parameters={
                "channel": channel,
                "text": message
            }
        )

# Use your custom node
slack = SlackNode(name="Send Notification", channel="#general", message="Hello!")
workflow.add_node(slack)
```

## 🔗 n8n Integration

Generated workflow files can be directly imported into n8n:

1. **Export your workflow**: `workflow.export("my_workflow.json")`
2. **Open n8n**: Navigate to your n8n instance
3. **Import workflow**: Go to Workflows → Import from File
4. **Select file**: Choose your generated JSON file
5. **Configure credentials**: Set up any required API credentials
6. **Execute**: Your programmatically created workflow is ready!

## 🛠️ Development

### Prerequisites
- Python 3.6+
- No external dependencies required for core functionality

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Code Quality
The SDK follows Python best practices:
- Type hints throughout
- Comprehensive error handling
- Extensive documentation
- Full test coverage
- Clean, readable code structure

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter issues or have questions:

1. Check the comprehensive test files for usage examples
2. Review the error handling documentation
3. Enable debug logging to see detailed SDK operations
4. Consult the validation error messages for specific guidance

## 🎉 Credits

This n8n Python SDK was developed during the **n8n and Vibe Coding Hackathon** organized by n8n Ambassador **Aemal Sayer**.

**Hackathon Team:**
- Promit
- Aemal
- Mohammad
- Paul
- George
- David
- Ashwin

This SDK provides a powerful, Pythonic way to create and manage n8n workflows programmatically. It's designed to be intuitive for Python developers while maintaining full compatibility with n8n's workflow format.

**Happy Automating!** 🚀

---

**Note**: This SDK generates n8n-compatible JSON files. For actual workflow execution, you'll need an n8n instance. The SDK focuses on workflow definition and export, making it easy to version control and programmatically generate complex automation workflows.