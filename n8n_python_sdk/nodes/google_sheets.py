"""
n8n Python SDK - Google Sheets Node

This module contains the GoogleSheetsNode class for n8n Google Sheets nodes.
"""

from typing import Dict, Any, Optional, List, Union
try:
    from ..node import Node
except ImportError:
    from node import Node


class GoogleSheetsNode(Node):
    """
    Represents an n8n Google Sheets node.
    
    The Google Sheets node allows reading from and writing to Google Sheets
    as part of a workflow.
    """
    
    def __init__(
        self,
        name: str = "Google Sheets",
        operation: str = "appendOrUpdate",
        document_id: Optional[Union[str, Dict[str, Any]]] = None,
        sheet_name: Optional[Union[str, Dict[str, Any]]] = None,
        columns: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None,
        credential_id: Optional[str] = None,
        credential_name: Optional[str] = None,
        node_id: Optional[str] = None,
        position: Optional[List[int]] = None
    ):
        """
        Initialize a Google Sheets node.
        
        Args:
            name: The display name for the node
            operation: The operation to perform (appendOrUpdate, read, append, etc.)
            document_id: Google Sheets document ID or resource locator object
            sheet_name: Sheet name or resource locator object
            columns: Column configuration for the operation
            options: Additional options for the operation
            credential_id: ID of the Google Sheets OAuth2 credential
            credential_name: Name of the Google Sheets OAuth2 credential
            node_id: Unique identifier for the node (auto-generated if None)
            position: [x, y] coordinates for node position in workflow
        """
        parameters = {
            "operation": operation,
            "options": options or {}
        }
        
        # Add document ID
        if document_id is not None:
            if isinstance(document_id, str):
                parameters["documentId"] = {
                    "__rl": True,
                    "value": document_id,
                    "mode": "list"
                }
            else:
                parameters["documentId"] = document_id
                
        # Add sheet name
        if sheet_name is not None:
            if isinstance(sheet_name, str):
                parameters["sheetName"] = {
                    "__rl": True,
                    "value": "gid=0",  # Default to first sheet
                    "mode": "list",
                    "cachedResultName": sheet_name
                }
            else:
                parameters["sheetName"] = sheet_name
                
        # Add columns configuration
        if columns is not None:
            parameters["columns"] = columns
            
        # Set up credentials
        credentials = {}
        if credential_id and credential_name:
            credentials["googleSheetsOAuth2Api"] = {
                "id": credential_id,
                "name": credential_name
            }
            
        super().__init__(
            node_type="n8n-nodes-base.googleSheets",
            name=name,
            node_id=node_id,
            type_version=4.7,
            parameters=parameters,
            credentials=credentials,
            position=position or [0, 0]
        )
        
    @classmethod
    def append_or_update(
        cls,
        name: str = "Append or update row in sheet",
        document_id: Optional[Union[str, Dict[str, Any]]] = None,
        sheet_name: Optional[Union[str, Dict[str, Any]]] = None,
        columns: Optional[Dict[str, Any]] = None,
        matching_columns: Optional[List[str]] = None,
        credential_id: Optional[str] = None,
        credential_name: Optional[str] = None,
        node_id: Optional[str] = None,
        position: Optional[List[int]] = None
    ):
        """
        Create a Google Sheets node configured for append or update operation.
        
        Args:
            name: The display name for the node
            document_id: Google Sheets document ID or resource locator object
            sheet_name: Sheet name or resource locator object
            columns: Column mappings for the operation
            matching_columns: Columns to use for matching existing rows
            credential_id: ID of the Google Sheets OAuth2 credential
            credential_name: Name of the Google Sheets OAuth2 credential
            node_id: Unique identifier for the node (auto-generated if None)
            position: [x, y] coordinates for node position in workflow
        """
        # Set up columns configuration
        columns_config = columns or {}
        if not isinstance(columns_config, dict):
            columns_config = {}
            
        # Add default mapping mode if not specified
        if "mappingMode" not in columns_config:
            columns_config["mappingMode"] = "defineBelow"
            
        # Add matching columns if provided
        if matching_columns and "matchingColumns" not in columns_config:
            columns_config["matchingColumns"] = matching_columns
            
        return cls(
            name=name,
            operation="appendOrUpdate",
            document_id=document_id,
            sheet_name=sheet_name,
            columns=columns_config if columns_config else None,
            credential_id=credential_id,
            credential_name=credential_name,
            node_id=node_id,
            position=position
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert Google Sheets node to n8n-compatible dictionary format."""
        # Use the base implementation since the parameters are already properly formatted
        return super().to_dict()