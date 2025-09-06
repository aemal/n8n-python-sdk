"""
n8n Python SDK - Workflow Module

This module contains the Workflow class for creating and managing n8n workflows.
"""

from typing import List, Dict, Any, Optional, Union
import json
import uuid
import os
import logging
from datetime import datetime
try:
    from .node import Node
    from .exceptions import WorkflowError, ValidationError, ExportError, ErrorCodes
except ImportError:
    from node import Node
    from exceptions import WorkflowError, ValidationError, ExportError, ErrorCodes

# Configure logger for the workflow module
logger = logging.getLogger('n8n_sdk.workflow')


class Workflow:
    """
    Represents an n8n workflow with nodes and connections.
    
    A workflow contains nodes and the connections between them,
    and can be exported to n8n-compatible JSON format.
    """
    
    def __init__(self, name: str = "New Workflow", workflow_id: Optional[str] = None):
        """
        Initialize a new workflow.
        
        Args:
            name: The name of the workflow
            workflow_id: Unique identifier for the workflow (auto-generated if None)
        """
        if not name or not name.strip():
            raise WorkflowError("Workflow name cannot be empty", ErrorCodes.WORKFLOW_INVALID_NAME)
        
        self.id = workflow_id if workflow_id else str(uuid.uuid4())
        self.name = name.strip()
        self.nodes: List[Node] = []
        self.connections: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
        self.active = True
        self.settings: Dict[str, Any] = {}
        self.tags: List[str] = []
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        
        logger.info(f"Created new workflow: '{self.name}' (ID: {self.id})")
        
    def add_node(self, node: Node) -> None:
        """
        Add a single node to the workflow.
        
        Args:
            node: The node to add to the workflow
            
        Raises:
            WorkflowError: If node is not a Node instance or if a node with the same ID already exists
        """
        if not isinstance(node, Node):
            error_msg = f"Expected Node instance, got {type(node).__name__}"
            logger.error(f"Failed to add node to workflow '{self.name}': {error_msg}")
            raise WorkflowError(error_msg, ErrorCodes.NODE_INVALID_TYPE)
        
        # Check if node with same ID already exists
        if any(existing_node.id == node.id for existing_node in self.nodes):
            error_msg = f"Node with ID '{node.id}' already exists in workflow"
            logger.error(f"Failed to add node to workflow '{self.name}': {error_msg}")
            raise WorkflowError(error_msg, ErrorCodes.WORKFLOW_DUPLICATE_NODE)
        
        # Check if node with same name already exists
        if any(existing_node.name == node.name for existing_node in self.nodes):
            error_msg = f"Node with name '{node.name}' already exists in workflow"
            logger.warning(f"Adding node to workflow '{self.name}': {error_msg}")
        
        self.nodes.append(node)
        self.updated_at = datetime.now().isoformat()
        
        logger.debug(f"Added node '{node.name}' (ID: {node.id}, Type: {node.type}) to workflow '{self.name}'")
        
    def add_nodes(self, *nodes: Node) -> None:
        """
        Add multiple nodes to the workflow.
        
        Args:
            *nodes: Variable number of nodes to add to the workflow
            
        Raises:
            TypeError: If any node is not a Node instance
            ValueError: If any node ID already exists
        """
        for node in nodes:
            self.add_node(node)
        
    def connect(
        self, 
        from_node: Node, 
        to_node: Node, 
        output_type: str = "main", 
        input_type: str = "main",
        output_index: int = 0,
        input_index: int = 0
    ) -> None:
        """
        Create a connection between two nodes.
        
        Args:
            from_node: The source node
            to_node: The target node
            output_type: Type of output (default: "main")
            input_type: Type of input (default: "main")  
            output_index: Output index (default: 0)
            input_index: Input index (default: 0)
            
        Raises:
            WorkflowError: If either node is not in the workflow
        """
        # Verify both nodes are in the workflow
        if from_node not in self.nodes:
            error_msg = f"Source node '{from_node.name}' is not in the workflow"
            logger.error(f"Failed to create connection in workflow '{self.name}': {error_msg}")
            raise WorkflowError(error_msg, ErrorCodes.CONNECTION_SOURCE_NOT_FOUND)
        if to_node not in self.nodes:
            error_msg = f"Target node '{to_node.name}' is not in the workflow"
            logger.error(f"Failed to create connection in workflow '{self.name}': {error_msg}")
            raise WorkflowError(error_msg, ErrorCodes.CONNECTION_TARGET_NOT_FOUND)
        
        # Initialize connection structure using node names (as n8n uses names for connections)
        source_name = from_node.name
        if source_name not in self.connections:
            self.connections[source_name] = {}
        
        if output_type not in self.connections[source_name]:
            self.connections[source_name][output_type] = []
        
        # Ensure we have enough output slots
        while len(self.connections[source_name][output_type]) <= output_index:
            self.connections[source_name][output_type].append([])
        
        # Create the connection
        connection = {
            "node": to_node.name,
            "type": input_type,
            "index": input_index
        }
        
        self.connections[source_name][output_type][output_index].append(connection)
        self.updated_at = datetime.now().isoformat()
        
        # Ensure target node has empty connection placeholder if it doesn't exist
        target_name = to_node.name
        if target_name not in self.connections:
            self.connections[target_name] = {
                "main": [[]]
            }
        
        logger.debug(f"Connected '{from_node.name}' to '{to_node.name}' in workflow '{self.name}' "
                    f"(output: {output_type}[{output_index}] -> input: {input_type}[{input_index}])")
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert workflow to dictionary format compatible with n8n.
        
        Returns:
            Dictionary representation of the workflow
        """
        return {
            "id": self.id,
            "name": self.name,
            "nodes": [node.to_dict() for node in self.nodes],
            "connections": self.connections,
            "active": self.active,
            "settings": self.settings,
            "tags": self.tags,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "pinData": {},
            "meta": {
                "instanceId": self.id
            }
        }
        
    def export(self, file_path: str, pretty: bool = True, validate: bool = True) -> None:
        """
        Export workflow to JSON file compatible with n8n.
        
        Args:
            file_path: Path where the workflow JSON will be saved
            pretty: Whether to format the JSON with indentation for readability
            validate: Whether to validate the workflow before export
            
        Raises:
            ExportError: If the file cannot be written or JSON serialization fails
            ValidationError: If validation fails and validate=True
        """
        logger.info(f"Starting export of workflow '{self.name}' to {file_path}")
        
        try:
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(os.path.abspath(file_path))
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
                logger.debug(f"Created directory: {dir_path}")
            
            # Validate workflow if requested
            if validate:
                logger.debug(f"Validating workflow '{self.name}' before export")
                validation_errors = self.validate()
                if validation_errors:
                    error_msg = f"Workflow validation failed: {', '.join(validation_errors)}"
                    logger.error(f"Export failed for workflow '{self.name}': {error_msg}")
                    raise ValidationError(error_msg, ErrorCodes.EXPORT_VALIDATION_ERROR)
                logger.debug(f"Workflow '{self.name}' validation passed")
            
            # Convert workflow to dictionary
            workflow_dict = self.to_dict()
            logger.debug(f"Converted workflow '{self.name}' to dictionary format")
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(workflow_dict, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(workflow_dict, f, ensure_ascii=False)
            
            # Update timestamp
            self.updated_at = datetime.now().isoformat()
            
            logger.info(f"Successfully exported workflow '{self.name}' to {file_path}")
            
        except IOError as e:
            error_msg = f"Failed to export workflow to {file_path}: {str(e)}"
            logger.error(error_msg)
            raise ExportError(error_msg, ErrorCodes.EXPORT_FILE_ERROR)
        except (ValueError, TypeError) as e:
            error_msg = f"JSON serialization failed: {str(e)}"
            logger.error(f"Export failed for workflow '{self.name}': {error_msg}")
            raise ExportError(error_msg, ErrorCodes.EXPORT_SERIALIZATION_ERROR)
        except Exception as e:
            error_msg = f"Export failed: {str(e)}"
            logger.error(f"Unexpected error during export of workflow '{self.name}': {error_msg}")
            raise ExportError(error_msg)
    
    def validate(self) -> List[str]:
        """
        Validate the workflow and return list of validation errors.
        
        Returns:
            List of validation error messages. Empty list if valid.
        """
        errors = []
        
        # Check workflow name
        if not self.name:
            errors.append("Workflow name is required")
        
        # Check nodes
        if not self.nodes:
            errors.append("Workflow must contain at least one node")
        
        # Check for duplicate node IDs
        node_ids = [node.id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            errors.append("Duplicate node IDs found")
        
        # Check for duplicate node names
        node_names = [node.name for node in self.nodes]
        if len(node_names) != len(set(node_names)):
            errors.append("Duplicate node names found")
        
        # Validate each node
        for i, node in enumerate(self.nodes):
            node_errors = node.validate()
            for error in node_errors:
                errors.append(f"Node {i+1} ({node.name}): {error}")
        
        # Validate connections
        node_names_set = {node.name for node in self.nodes}
        for source_name, outputs in self.connections.items():
            if source_name not in node_names_set:
                errors.append(f"Connection source '{source_name}' does not exist")
            
            for output_type, output_groups in outputs.items():
                for output_group in output_groups:
                    for connection in output_group:
                        if isinstance(connection, dict) and 'node' in connection:
                            target_name = connection['node']
                            if target_name not in node_names_set:
                                errors.append(f"Connection target '{target_name}' does not exist")
        
        return errors
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        """
        Create workflow from dictionary data.
        
        Args:
            data: Dictionary representation of an n8n workflow
            
        Returns:
            Workflow instance created from the dictionary data
            
        Raises:
            ValueError: If the data is missing required fields
        """
        # Create workflow instance
        workflow = cls(
            name=data.get("name", "Imported Workflow"),
            workflow_id=data.get("id")
        )
        
        # Set additional properties
        workflow.active = data.get("active", True)
        workflow.settings = data.get("settings", {})
        workflow.tags = data.get("tags", [])
        workflow.created_at = data.get("createdAt", workflow.created_at)
        workflow.updated_at = data.get("updatedAt", workflow.updated_at)
        
        # Import nodes
        nodes_data = data.get("nodes", [])
        for node_data in nodes_data:
            node = Node.from_dict(node_data)
            workflow.nodes.append(node)
        
        # Import connections
        workflow.connections = data.get("connections", {})
        
        return workflow
        
    @classmethod
    def from_json(cls, filename: str) -> 'Workflow':
        """
        Load workflow from JSON file.
        
        Args:
            filename: Path to the JSON file containing the workflow
            
        Returns:
            Workflow instance loaded from the file
            
        Raises:
            FileNotFoundError: If the file does not exist
            json.JSONDecodeError: If the file contains invalid JSON
            ValueError: If the workflow data is invalid
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Workflow file not found: {filename}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in workflow file {filename}: {str(e)}", e.doc, e.pos)