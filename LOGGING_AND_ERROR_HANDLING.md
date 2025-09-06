# n8n Python SDK - Logging and Error Handling Guide

This guide covers the comprehensive logging and error handling features of the n8n Python SDK. These features help you debug issues, understand SDK behavior, and handle errors gracefully in your applications.

## Table of Contents

- [Overview](#overview)
- [Custom Exception Classes](#custom-exception-classes)
- [Logging Configuration](#logging-configuration)
- [Error Handling Best Practices](#error-handling-best-practices)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

## Overview

The n8n Python SDK provides:

- **Custom Exception Classes**: Specific exception types for different error scenarios
- **Comprehensive Logging**: Detailed logging with configurable levels and outputs
- **Error Codes**: Programmatic error identification with standardized error codes
- **Graceful Error Handling**: Robust error handling throughout the SDK

## Custom Exception Classes

The SDK defines a hierarchy of custom exceptions for specific error scenarios:

### Base Exception

```python
from n8n_python_sdk.exceptions import SDKError

# Base exception for all SDK errors
class SDKError(Exception):
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)
```

### Specific Exception Types

| Exception Class | Use Case | Example Scenarios |
|----------------|----------|-------------------|
| `WorkflowError` | Workflow operations | Duplicate nodes, invalid connections |
| `NodeError` | Node operations | Invalid parameters, missing fields |
| `ExportError` | Export operations | File system errors, serialization failures |
| `ValidationError` | Validation failures | Invalid workflows, missing required fields |
| `ImportError` | Import operations | Invalid JSON, missing fields |
| `ConnectionError` | Node connections | Invalid connections, circular dependencies |

### Error Codes

Each exception can include a standardized error code for programmatic handling:

```python
from n8n_python_sdk.exceptions import ErrorCodes

# Available error codes
ErrorCodes.WORKFLOW_INVALID_NAME    # "WF001"
ErrorCodes.WORKFLOW_NO_NODES        # "WF002"
ErrorCodes.NODE_INVALID_TYPE        # "ND001"
ErrorCodes.EXPORT_FILE_ERROR        # "EX001"
# ... and many more
```

## Logging Configuration

### Basic Configuration

```python
from n8n_python_sdk.logging_config import configure_logging

# Configure basic logging
logger = configure_logging(level='INFO')
```

### Advanced Configuration

```python
import logging
from n8n_python_sdk.logging_config import configure_logging

# Configure with custom format and file output
logger = configure_logging(
    level=logging.DEBUG,
    format_string='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    enable_file_logging=True,
    log_file_path='n8n_sdk.log',
    max_file_size=10 * 1024 * 1024,  # 10MB
    backup_count=5
)
```

### Logging Levels

| Level | Description | When to Use |
|-------|-------------|-------------|
| `DEBUG` | Detailed information | Development, troubleshooting |
| `INFO` | General information | Production monitoring |
| `WARNING` | Warning messages | Potential issues |
| `ERROR` | Error conditions | Error tracking |
| `CRITICAL` | Critical failures | System failures |

### Quick Configuration Functions

```python
from n8n_python_sdk.logging_config import (
    enable_debug_logging,
    disable_logging,
    set_log_level
)

# Enable debug logging for troubleshooting
enable_debug_logging()

# Change log level dynamically
set_log_level('WARNING')

# Disable all logging
disable_logging()
```

## Error Handling Best Practices

### 1. Catch Specific Exceptions

```python
from n8n_python_sdk.exceptions import WorkflowError, NodeError

try:
    workflow = Workflow("My Workflow")
    node = Node("invalid.type", "Test Node")
    workflow.add_node(node)
except NodeError as e:
    print(f"Node error: {e}")
    if e.code == ErrorCodes.NODE_INVALID_TYPE:
        # Handle specific error
        pass
except WorkflowError as e:
    print(f"Workflow error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2. Use Error Codes for Programmatic Handling

```python
from n8n_python_sdk.exceptions import WorkflowError, ErrorCodes

def handle_workflow_error(error: WorkflowError):
    if error.code == ErrorCodes.WORKFLOW_DUPLICATE_NODE:
        return "A node with that ID already exists"
    elif error.code == ErrorCodes.WORKFLOW_INVALID_NAME:
        return "Please provide a valid workflow name"
    else:
        return f"Workflow error: {error.message}"

try:
    workflow = Workflow("")  # Empty name
except WorkflowError as e:
    message = handle_workflow_error(e)
    print(message)  # "Please provide a valid workflow name"
```

### 3. Log Errors with Context

```python
from n8n_python_sdk.logging_config import get_logger

logger = get_logger('my_app')

try:
    workflow.export("invalid/path/workflow.json")
except ExportError as e:
    logger.error(f"Failed to export workflow '{workflow.name}': {e}")
    # Handle error gracefully
```

## Usage Examples

### Example 1: Basic Error Handling

```python
from n8n_python_sdk import Workflow
from n8n_python_sdk.nodes import ManualTriggerNode, HTTPRequestNode
from n8n_python_sdk.exceptions import WorkflowError, ExportError
from n8n_python_sdk.logging_config import configure_logging

# Configure logging
configure_logging(level='INFO')

try:
    # Create workflow
    workflow = Workflow("API Data Processor")
    
    # Add nodes
    trigger = ManualTriggerNode(name="Start")
    http_node = HTTPRequestNode(
        name="Fetch Data",
        url="https://api.example.com/data"
    )
    
    workflow.add_node(trigger)
    workflow.add_node(http_node)
    
    # Connect nodes
    workflow.connect(trigger, http_node)
    
    # Export workflow
    workflow.export("workflows/api_processor.json")
    
    print("✅ Workflow created successfully!")
    
except WorkflowError as e:
    print(f"❌ Workflow error: {e}")
except ExportError as e:
    print(f"❌ Export error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

### Example 2: Advanced Error Handling with Logging

```python
import logging
from n8n_python_sdk import Workflow
from n8n_python_sdk.exceptions import *
from n8n_python_sdk.logging_config import configure_logging, get_logger

# Configure detailed logging
configure_logging(
    level=logging.DEBUG,
    enable_file_logging=True,
    log_file_path='workflow_creation.log'
)

logger = get_logger('workflow_builder')

def create_workflow_safely(name: str, nodes_config: list):
    """Create a workflow with comprehensive error handling."""
    try:
        logger.info(f"Creating workflow: {name}")
        workflow = Workflow(name)
        
        nodes = []
        for node_config in nodes_config:
            try:
                # Create node based on config
                node = create_node_from_config(node_config)
                workflow.add_node(node)
                nodes.append(node)
                logger.debug(f"Added node: {node.name}")
            except NodeError as e:
                logger.error(f"Failed to create node: {e}")
                raise
        
        # Create connections
        for i in range(len(nodes) - 1):
            workflow.connect(nodes[i], nodes[i + 1])
            logger.debug(f"Connected {nodes[i].name} to {nodes[i + 1].name}")
        
        # Validate before export
        validation_errors = workflow.validate()
        if validation_errors:
            raise ValidationError(f"Validation failed: {', '.join(validation_errors)}")
        
        logger.info("Workflow created successfully")
        return workflow
        
    except WorkflowError as e:
        logger.error(f"Workflow creation failed: {e}")
        raise
    except ValidationError as e:
        logger.error(f"Workflow validation failed: {e}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error during workflow creation: {e}")
        raise

# Usage
try:
    workflow = create_workflow_safely("My Workflow", node_configs)
    workflow.export("output/my_workflow.json")
except Exception as e:
    logger.error(f"Workflow creation process failed: {e}")
```

### Example 3: Error Recovery Strategies

```python
from n8n_python_sdk import Workflow
from n8n_python_sdk.exceptions import *
from n8n_python_sdk.logging_config import configure_logging
import time

configure_logging(level='INFO')

def create_workflow_with_retry(name: str, max_retries: int = 3):
    """Create workflow with retry logic for transient errors."""
    for attempt in range(max_retries):
        try:
            workflow = Workflow(name)
            
            # Add some complexity that might fail
            for i in range(5):
                node = ManualTriggerNode(name=f"Node_{i}")
                workflow.add_node(node)
            
            return workflow
            
        except WorkflowError as e:
            if e.code == ErrorCodes.WORKFLOW_DUPLICATE_NODE:
                # This is likely a programming error, don't retry
                raise
            elif attempt < max_retries - 1:
                # Retry for other workflow errors
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                raise
        except Exception as e:
            # For unexpected errors, retry with backoff
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            else:
                raise

# Usage with error recovery
try:
    workflow = create_workflow_with_retry("Resilient Workflow")
    print("Workflow created successfully after potential retries")
except Exception as e:
    print(f"Failed to create workflow after retries: {e}")
```

## Troubleshooting

### Common Issues and Solutions

#### 1. No Log Output

**Problem**: No log messages are appearing.

**Solution**:
```python
from n8n_python_sdk.logging_config import configure_logging

# Ensure logging is configured
configure_logging(level='DEBUG')  # Use DEBUG for maximum visibility
```

#### 2. Import Errors

**Problem**: `ImportError` when importing exception classes.

**Solution**:
```python
# Use try/except for backwards compatibility
try:
    from n8n_python_sdk.exceptions import WorkflowError
except ImportError:
    # Fallback for older versions
    WorkflowError = Exception
```

#### 3. Log File Permission Issues

**Problem**: Cannot write to log file.

**Solution**:
```python
import os
from n8n_python_sdk.logging_config import configure_logging

# Ensure directory exists and is writable
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

configure_logging(
    enable_file_logging=True,
    log_file_path=os.path.join(log_dir, "n8n_sdk.log")
)
```

#### 4. Too Verbose Logging

**Problem**: Too many log messages in production.

**Solution**:
```python
from n8n_python_sdk.logging_config import configure_logging

# Use WARNING or ERROR level in production
configure_logging(level='WARNING')
```

### Debugging Tips

1. **Enable Debug Logging**: Use `enable_debug_logging()` to see detailed SDK behavior
2. **Check Error Codes**: Use error codes for programmatic error identification
3. **Log Context**: Include relevant context (workflow names, node IDs) in error messages
4. **Use Structured Logging**: Consider using structured logging formats for better parsing
5. **Monitor Log Files**: Set up log rotation and monitoring for production systems

## Advanced Topics

### Custom Exception Handling

You can extend the SDK's exception hierarchy:

```python
from n8n_python_sdk.exceptions import SDKError

class CustomWorkflowError(SDKError):
    """Custom exception for application-specific workflow errors."""
    pass

def validate_business_rules(workflow):
    if len(workflow.nodes) > 100:
        raise CustomWorkflowError("Workflow exceeds maximum node limit", "APP001")
```

### Integration with External Logging Systems

```python
import logging
import structlog
from n8n_python_sdk.logging_config import get_logger

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.LoggerAdapter,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

# Use with SDK
logger = structlog.get_logger("n8n_sdk")

try:
    workflow = Workflow("Test")
except WorkflowError as e:
    logger.error("workflow_creation_failed", 
                error_code=e.code, 
                error_message=str(e))
```

This comprehensive guide covers all aspects of error handling and logging in the n8n Python SDK. Use these features to build robust applications that gracefully handle errors and provide excellent debugging capabilities.