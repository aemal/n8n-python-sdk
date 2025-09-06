"""
n8n Python SDK - JSON Parser Utilities

This module contains utilities for parsing and validating n8n JSON workflow files.
"""

import json
from typing import Dict, Any, Optional, List
from pathlib import Path


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file exists and has a .json extension.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if file exists and has .json extension, False otherwise
        
    Raises:
        ValueError: If file_path is empty or None
        FileNotFoundError: If file does not exist
        ValueError: If file does not have .json extension
    """
    if not file_path:
        raise ValueError("File path cannot be empty or None")
    
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    if path.suffix.lower() != '.json':
        raise ValueError(f"File must have .json extension: {file_path}")
    
    return True


def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Read and parse JSON content from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file cannot be found or opened
        json.JSONDecodeError: If file contains invalid JSON
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if not content.strip():
            raise ValueError(f"JSON file is empty: {file_path}")
            
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {str(e)}", e.doc, e.pos)
            
        return data
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not open file: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")


def validate_workflow_structure(data: Dict[str, Any]) -> bool:
    """
    Validate that parsed JSON has the expected n8n workflow structure.
    
    Args:
        data: Parsed JSON data to validate
        
    Returns:
        True if structure is valid
        
    Raises:
        ValueError: If the workflow structure is invalid
    """
    if not isinstance(data, dict):
        raise ValueError("Workflow data must be a dictionary")
    
    # Check for required top-level keys
    required_keys = ["nodes", "connections"]
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required keys in workflow: {missing_keys}")
    
    # Validate nodes structure
    nodes = data["nodes"]
    if not isinstance(nodes, list):
        raise ValueError("Nodes must be a list")
    
    if len(nodes) == 0:
        raise ValueError("Workflow must contain at least one node")
    
    # Validate each node
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise ValueError(f"Node {i} must be a dictionary")
        
        required_node_keys = ["id", "name", "type", "position"]
        missing_node_keys = [key for key in required_node_keys if key not in node]
        if missing_node_keys:
            raise ValueError(f"Node {i} missing required keys: {missing_node_keys}")
        
        # Validate node properties
        if not isinstance(node["id"], str):
            raise ValueError(f"Node {i} id must be a string")
        if not isinstance(node["name"], str):
            raise ValueError(f"Node {i} name must be a string")
        if not isinstance(node["type"], str):
            raise ValueError(f"Node {i} type must be a string")
        if not isinstance(node["position"], list) or len(node["position"]) != 2:
            raise ValueError(f"Node {i} position must be a list of 2 numbers")
    
    # Validate connections structure
    connections = data["connections"]
    if not isinstance(connections, dict):
        raise ValueError("Connections must be a dictionary")
    
    # Get all node names for connection validation
    node_names = {node["name"] for node in nodes}
    
    # Validate connection structure
    for source_node, connection_data in connections.items():
        if source_node not in node_names:
            raise ValueError(f"Connection source node '{source_node}' not found in workflow nodes")
        
        if not isinstance(connection_data, dict):
            raise ValueError(f"Connection data for '{source_node}' must be a dictionary")
        
        # Check main connections
        if "main" in connection_data:
            main_connections = connection_data["main"]
            if not isinstance(main_connections, list):
                raise ValueError(f"Main connections for '{source_node}' must be a list")
            
            for conn_group in main_connections:
                if not isinstance(conn_group, list):
                    continue
                for conn in conn_group:
                    if not isinstance(conn, dict):
                        raise ValueError(f"Connection must be a dictionary")
                    if "node" not in conn:
                        raise ValueError(f"Connection missing 'node' key")
                    if conn["node"] not in node_names:
                        raise ValueError(f"Connection target node '{conn['node']}' not found in workflow nodes")
    
    return True


def read_node_json(file_path: str) -> Dict[str, Any]:
    """
    Main utility function to read and validate n8n workflow JSON files.
    
    Args:
        file_path: Path to the n8n JSON file
        
    Returns:
        Validated JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file path is invalid or workflow structure is invalid
        json.JSONDecodeError: If JSON is malformed
        IOError: If file cannot be read
    """
    # Step 1: Validate file path
    validate_file_path(file_path)
    
    # Step 2: Read and parse JSON
    data = read_json_file(file_path)
    
    # Step 3: Validate workflow structure
    validate_workflow_structure(data)
    
    return data


def process_workflow_directory(
    directory_path: str, 
    pattern: str = "*.json", 
    recursive: bool = False
) -> Dict[str, Dict[str, Any]]:
    """
    Process multiple workflow files from a directory.
    
    Args:
        directory_path: Path to directory containing workflow JSON files
        pattern: File pattern to match (default: "*.json")
        recursive: Whether to search subdirectories recursively
        
    Returns:
        Dictionary mapping filenames to their validated workflow data
        
    Raises:
        FileNotFoundError: If directory does not exist
        ValueError: If directory_path is not a directory
    """
    dir_path = Path(directory_path)
    
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")
    
    workflows = {}
    
    # Use glob to find files matching the pattern
    if recursive:
        json_files = dir_path.rglob(pattern)
    else:
        json_files = dir_path.glob(pattern)
    
    for file_path in json_files:
        try:
            # Try to parse each file
            workflow_data = read_node_json(str(file_path))
            workflows[file_path.name] = workflow_data
            
        except Exception as e:
            # Log errors but continue processing other files
            print(f"Warning: Failed to process {file_path.name}: {str(e)}")
            continue
    
    return workflows