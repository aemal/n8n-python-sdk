"""
n8n Python SDK - Exception Classes

This module contains custom exception classes for the n8n Python SDK.
These exceptions provide specific error handling for different types of
errors that can occur during workflow creation and management.
"""


class SDKError(Exception):
    """
    Base exception for all n8n Python SDK errors.
    
    This is the base class for all custom exceptions in the SDK.
    All other SDK exceptions inherit from this class.
    
    Args:
        message (str): A descriptive error message
        code (str, optional): An error code for programmatic error handling
    """
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class WorkflowError(SDKError):
    """
    Exception raised for errors in the Workflow class.
    
    This exception is raised when there are issues with workflow operations
    such as adding nodes, creating connections, or validating workflows.
    
    Examples:
        - Adding a node that already exists
        - Creating connections to non-existent nodes
        - Invalid workflow configurations
    """
    pass


class NodeError(SDKError):
    """
    Exception raised for errors in the Node class and its subclasses.
    
    This exception is raised when there are issues with node operations
    such as invalid parameters, missing required fields, or node validation failures.
    
    Examples:
        - Invalid node parameters
        - Missing required node properties
        - Node validation failures
    """
    pass


class ExportError(SDKError):
    """
    Exception raised for errors during workflow export operations.
    
    This exception is raised when there are issues exporting workflows
    to JSON format or writing files to disk.
    
    Examples:
        - File system errors during export
        - JSON serialization failures
        - Invalid export parameters
    """
    pass


class ValidationError(SDKError):
    """
    Exception raised for validation errors in workflows or nodes.
    
    This exception is raised when validation checks fail for workflows,
    nodes, or other SDK components.
    
    Examples:
        - Workflow validation failures
        - Node parameter validation failures
        - Invalid data structures
    """
    pass


class ImportError(SDKError):
    """
    Exception raised for errors during workflow import operations.
    
    This exception is raised when there are issues importing workflows
    from JSON files or parsing workflow data.
    
    Examples:
        - Invalid JSON format
        - Missing required workflow fields
        - Unsupported workflow versions
    """
    pass


class ConnectionError(SDKError):
    """
    Exception raised for errors in node connections.
    
    This exception is raised when there are issues with creating,
    modifying, or validating connections between nodes.
    
    Examples:
        - Invalid connection parameters
        - Circular dependency loops
        - Connection to non-existent nodes
    """
    pass


# Error code constants for programmatic error handling
class ErrorCodes:
    """Constants for error codes used throughout the SDK."""
    
    # Workflow errors
    WORKFLOW_INVALID_NAME = "WF001"
    WORKFLOW_NO_NODES = "WF002"
    WORKFLOW_DUPLICATE_NODE = "WF003"
    WORKFLOW_VALIDATION_FAILED = "WF004"
    
    # Node errors
    NODE_INVALID_TYPE = "ND001"
    NODE_INVALID_PARAMETERS = "ND002"
    NODE_MISSING_REQUIRED_FIELD = "ND003"
    NODE_VALIDATION_FAILED = "ND004"
    
    # Connection errors
    CONNECTION_SOURCE_NOT_FOUND = "CN001"
    CONNECTION_TARGET_NOT_FOUND = "CN002"
    CONNECTION_INVALID_OUTPUT = "CN003"
    CONNECTION_CIRCULAR_DEPENDENCY = "CN004"
    
    # Export errors
    EXPORT_FILE_ERROR = "EX001"
    EXPORT_SERIALIZATION_ERROR = "EX002"
    EXPORT_VALIDATION_ERROR = "EX003"
    
    # Import errors
    IMPORT_FILE_NOT_FOUND = "IM001"
    IMPORT_INVALID_JSON = "IM002"
    IMPORT_MISSING_FIELDS = "IM003"
    IMPORT_UNSUPPORTED_VERSION = "IM004"


def create_error(error_type: type, message: str, code: str = None) -> SDKError:
    """
    Helper function to create SDK errors with consistent formatting.
    
    Args:
        error_type: The exception class to create
        message: The error message
        code: Optional error code from ErrorCodes
        
    Returns:
        An instance of the specified exception type
        
    Example:
        >>> error = create_error(WorkflowError, "Invalid workflow", ErrorCodes.WORKFLOW_INVALID_NAME)
        >>> raise error
    """
    return error_type(message, code)