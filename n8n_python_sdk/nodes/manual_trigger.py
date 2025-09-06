"""
n8n Python SDK - Manual Trigger Node

This module contains the ManualTriggerNode class for n8n manual trigger nodes.
"""

from typing import Dict, Any, Optional, List
try:
    from ..node import Node
except ImportError:
    from node import Node


class ManualTriggerNode(Node):
    """
    Represents an n8n Manual Trigger node.
    
    The Manual Trigger node is used to manually start workflow execution.
    It's typically the first node in a workflow.
    """
    
    def __init__(
        self,
        name: str = "When clicking 'Execute workflow'",
        node_id: Optional[str] = None,
        position: Optional[List[int]] = None
    ):
        """
        Initialize a Manual Trigger node.
        
        Args:
            name: The display name for the node (default: "When clicking 'Execute workflow'")
            node_id: Unique identifier for the node (auto-generated if None)
            position: [x, y] coordinates for node position in workflow
        """
        super().__init__(
            node_type="n8n-nodes-base.manualTrigger",
            name=name,
            node_id=node_id,
            type_version=1,
            parameters={},  # Manual trigger has empty parameters
            position=position or [0, 0]
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert Manual Trigger node to n8n-compatible dictionary format."""
        # Use the base implementation since Manual Trigger doesn't need special handling
        return super().to_dict()