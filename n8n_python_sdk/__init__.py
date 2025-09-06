"""
n8n Python SDK

A Python SDK for creating and managing n8n workflows programmatically.
This SDK provides a convenient way to build n8n workflows using Python,
with support for various node types and workflow operations.

Example:
    >>> from n8n_python_sdk import Workflow, ManualTriggerNode, HTTPRequestNode
    >>> 
    >>> # Create a new workflow
    >>> workflow = Workflow("My API Workflow")
    >>> 
    >>> # Add nodes
    >>> trigger = ManualTriggerNode(name="Start")
    >>> http = HTTPRequestNode(name="Fetch Data", url="https://api.example.com/data")
    >>> 
    >>> workflow.add_nodes(trigger, http)
    >>> workflow.connect(trigger, http)
    >>> 
    >>> # Export to n8n
    >>> workflow.export("my_workflow.json")

For more information and detailed usage examples, see the documentation.
"""

# Import core classes
from .workflow import Workflow
from .node import Node

# Import specialized node classes
from .nodes.manual_trigger import ManualTriggerNode
from .nodes.http_request import HTTPRequestNode
from .nodes.google_sheets import GoogleSheetsNode

# Import utility classes
from .exceptions import (
    SDKError,
    WorkflowError,
    NodeError,
    ExportError,
    ValidationError,
    ImportError as SDKImportError,  # Avoid conflict with built-in ImportError
    ConnectionError as SDKConnectionError,  # Avoid conflict with built-in ConnectionError
    ErrorCodes
)

from .logging_config import (
    configure_logging,
    get_logger,
    set_log_level,
    enable_debug_logging,
    disable_logging
)

# Version information
__version__ = "0.1.0"
__author__ = "n8n Python SDK Contributors"
__description__ = "Python SDK for creating and managing n8n workflows"

# Public API - these are the classes/functions users should import
__all__ = [
    # Core classes
    "Workflow",
    "Node",
    
    # Specialized node classes
    "ManualTriggerNode",
    "HTTPRequestNode", 
    "GoogleSheetsNode",
    
    # Exception classes
    "SDKError",
    "WorkflowError",
    "NodeError",
    "ExportError",
    "ValidationError",
    "SDKImportError",
    "SDKConnectionError",
    "ErrorCodes",
    
    # Logging utilities
    "configure_logging",
    "get_logger",
    "set_log_level",
    "enable_debug_logging",
    "disable_logging",
    
    # Version info
    "__version__",
]