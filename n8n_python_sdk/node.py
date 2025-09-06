"""
n8n Python SDK - Node Module

This module contains the base Node class and specialized node implementations.
"""

from typing import Dict, Any, Optional, List, Tuple, Union
import uuid
import logging
try:
    from .exceptions import NodeError, ErrorCodes
except ImportError:
    from exceptions import NodeError, ErrorCodes

# Configure logger for the node module
logger = logging.getLogger('n8n_sdk.node')


class Node:
    """
    Base class for all n8n nodes.
    
    This class provides the common functionality that all n8n nodes share,
    such as id, name, type, and position.
    """
    
    def __init__(
        self,
        node_type: str,
        name: str,
        node_id: Optional[str] = None,
        type_version: Union[int, float] = 1,
        parameters: Optional[Dict[str, Any]] = None,
        position: Optional[List[int]] = None,
        credentials: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new node.
        
        Args:
            node_type: The n8n node type (e.g., 'n8n-nodes-base.httpRequest')
            name: The display name for the node
            node_id: Unique identifier for the node (auto-generated if None)
            type_version: Version of the node type
            parameters: Node-specific parameters
            position: [x, y] coordinates for node position in workflow
            credentials: Credentials configuration for the node
        """
        if not node_type or not node_type.strip():
            raise NodeError("Node type cannot be empty", ErrorCodes.NODE_INVALID_TYPE)
        if not name or not name.strip():
            raise NodeError("Node name cannot be empty", ErrorCodes.NODE_MISSING_REQUIRED_FIELD)
        
        self.id = node_id if node_id else str(uuid.uuid4())
        self.type = node_type.strip()
        self.name = name.strip()
        self.type_version = type_version
        self.parameters = parameters or {}
        self.position = position or [0, 0]
        self.credentials = credentials or {}
        
        logger.debug(f"Created node '{self.name}' (ID: {self.id}, Type: {self.type})")
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to n8n-compatible dictionary format."""
        node_dict = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "typeVersion": self.type_version,
            "position": list(self.position),  # Convert to list for JSON serialization
            "parameters": self.parameters
        }
        
        # Only include credentials if they exist
        if self.credentials:
            node_dict["credentials"] = self.credentials
            
        return node_dict
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """Create node from dictionary."""
        return cls(
            node_type=data.get("type", ""),
            name=data.get("name", ""),
            node_id=data.get("id"),
            type_version=data.get("typeVersion", 1),
            parameters=data.get("parameters", {}),
            position=data.get("position", [0, 0]),
            credentials=data.get("credentials", {})
        )
    
    def validate(self) -> List[str]:
        """
        Validate the node configuration and return list of validation errors.
        
        Returns:
            List of validation error messages. Empty list if valid.
        """
        errors = []
        
        # Check required fields
        if not self.id:
            errors.append("Node ID is required")
        if not self.name:
            errors.append("Node name is required")
        if not self.type:
            errors.append("Node type is required")
        
        # Validate position format
        if not isinstance(self.position, list) or len(self.position) != 2:
            errors.append("Position must be a list of 2 numbers")
        else:
            try:
                float(self.position[0])
                float(self.position[1])
            except (TypeError, ValueError):
                errors.append("Position coordinates must be numeric")
        
        # Validate type version
        if not isinstance(self.type_version, (int, float)):
            errors.append("Type version must be numeric")
        
        # Validate parameters and credentials are dictionaries
        if not isinstance(self.parameters, dict):
            errors.append("Parameters must be a dictionary")
        if not isinstance(self.credentials, dict):
            errors.append("Credentials must be a dictionary")
            
        return errors
    
    def is_valid(self) -> bool:
        """
        Check if the node configuration is valid.
        
        Returns:
            True if the node is valid, False otherwise.
        """
        return len(self.validate()) == 0
        
    def __repr__(self) -> str:
        return f"Node(type='{self.type}', name='{self.name}', id='{self.id}')"
        
    def __eq__(self, other) -> bool:
        """Check equality based on node id."""
        if not isinstance(other, Node):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Make Node hashable based on id."""
        return hash(self.id)