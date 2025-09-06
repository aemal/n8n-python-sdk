"""
n8n Python SDK - HTTP Request Node

This module contains the HTTPRequestNode class for n8n HTTP request nodes.
"""

from typing import Dict, Any, Optional, List, Union
try:
    from ..node import Node
except ImportError:
    from node import Node


class HTTPRequestNode(Node):
    """
    Represents an n8n HTTP Request node.
    
    The HTTP Request node allows making HTTP requests to external APIs
    and services as part of a workflow.
    """
    
    def __init__(
        self,
        name: str = "HTTP Request",
        url: str = "",
        method: str = "GET",
        node_id: Optional[str] = None,
        authentication: str = "none",
        headers: Optional[Dict[str, str]] = None,
        query_parameters: Optional[Dict[str, str]] = None,
        body_content_type: str = "json",
        body: Optional[Union[str, Dict[str, Any]]] = None,
        response_format: str = "json",
        options: Optional[Dict[str, Any]] = None,
        position: Optional[List[int]] = None
    ):
        """
        Initialize an HTTP Request node.
        
        Args:
            name: The display name for the node
            url: The URL to make the request to
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            node_id: Unique identifier for the node (auto-generated if None)
            authentication: Authentication method (none, basicAuth, headerAuth, etc.)
            headers: HTTP headers to include
            query_parameters: Query parameters to include
            body_content_type: Content type for request body (json, form, raw, etc.)
            body: Request body (for POST, PUT requests)
            response_format: Expected response format (json, text, etc.)
            options: Additional options for the HTTP request
            position: [x, y] coordinates for node position in workflow
        """
        parameters = {
            "url": url,
            "options": options or {}
        }
        
        # Only add method if it's not GET (default)
        if method != "GET":
            parameters["method"] = method
            
        # Add authentication if not none
        if authentication != "none":
            parameters["authentication"] = authentication
            
        # Add headers if provided
        if headers:
            parameters["headers"] = {
                "parameters": [
                    {"name": key, "value": value} 
                    for key, value in headers.items()
                ]
            }
            
        # Add query parameters if provided
        if query_parameters:
            parameters["qs"] = {
                "parameters": [
                    {"name": key, "value": value}
                    for key, value in query_parameters.items()
                ]
            }
            
        # Add body if provided
        if body is not None:
            if body_content_type == "json":
                parameters["sendBody"] = True
                parameters["bodyContentType"] = "json"
                if isinstance(body, dict):
                    parameters["jsonParameters"] = True
                else:
                    parameters["body"] = body
            elif body_content_type == "form":
                parameters["sendBody"] = True
                parameters["bodyContentType"] = "form-urlencoded"
                parameters["bodyParameters"] = {
                    "parameters": [
                        {"name": key, "value": value}
                        for key, value in body.items()
                    ] if isinstance(body, dict) else []
                }
            else:
                parameters["sendBody"] = True
                parameters["bodyContentType"] = body_content_type
                parameters["body"] = body
                
        # Add response format if not default
        if response_format != "json":
            parameters["responseFormat"] = response_format
            
        super().__init__(
            node_type="n8n-nodes-base.httpRequest",
            name=name,
            node_id=node_id,
            type_version=4.2,
            parameters=parameters,
            position=position or [0, 0]
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert HTTP Request node to n8n-compatible dictionary format."""
        # Use the base implementation since the parameters are already properly formatted
        return super().to_dict()