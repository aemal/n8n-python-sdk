#!/usr/bin/env python3
"""
n8n Python SDK - Sample Workflow Creation

This script demonstrates how to create a complete n8n workflow using the Python SDK.
It reproduces the example workflow from the PRD that fetches user data from JSONPlaceholder
API and appends/updates it to a Google Sheets document.
"""

import sys
import os

# Add the current directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from n8n_python_sdk.workflow import Workflow
    from n8n_python_sdk.node import Node
    from n8n_python_sdk.nodes.manual_trigger import ManualTriggerNode
    from n8n_python_sdk.nodes.http_request import HTTPRequestNode
    from n8n_python_sdk.nodes.google_sheets import GoogleSheetsNode
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure the n8n_python_sdk package is properly installed or in the Python path")
    sys.exit(1)


def create_sample_workflow():
    """
    Create a sample n8n workflow that reproduces the example from the PRD.
    
    This workflow:
    1. Starts with a manual trigger
    2. Makes an HTTP request to fetch user data from JSONPlaceholder API
    3. Appends/updates the data to a Google Sheets document
    
    Returns:
        Workflow: The complete workflow ready for export
    """
    # Create a new workflow
    workflow = Workflow(name="Users to Google Sheet")
    
    # Create the manual trigger node
    trigger = ManualTriggerNode(
        node_id="3effa98f-f88c-4c8d-a2f2-3dbf15ea77bd",
        name="When clicking 'Execute workflow'",
        position=[-288, -16]
    )
    
    # Create the HTTP request node
    http = HTTPRequestNode(
        node_id="087c2d01-6a20-47c6-9599-6a0136c99183",
        name="HTTP Request",
        url="https://jsonplaceholder.typicode.com/users",
        method="GET",
        response_format="json",
        position=[-32, -16]
    )
    
    # Create the Google Sheets node with complex configuration
    sheets = GoogleSheetsNode.append_or_update(
        node_id="66bf1544-26d7-4f0d-9130-a7714ae1beed",
        name="Append or update row in sheet",
        document_id={
            "__rl": True,
            "value": "193K6ZufOQgQcV-7P4D6jyS8ejNfxIv32yvT2bR5lT2k",
            "mode": "list",
            "cachedResultName": "Users",
            "cachedResultUrl": "https://docs.google.com/spreadsheets/d/193K6ZufOQgQcV-7P4D6jyS8ejNfxIv32yvT2bR5lT2k/edit?usp=drivesdk"
        },
        sheet_name={
            "__rl": True,
            "value": "gid=0",
            "mode": "list",
            "cachedResultName": "Sheet1",
            "cachedResultUrl": "https://docs.google.com/spreadsheets/d/193K6ZufOQgQcV-7P4D6jyS8ejNfxIv32yvT2bR5lT2k/edit#gid=0"
        },
        columns={
            "mappingMode": "defineBelow",
            "value": {
                "name": "={{ $json.name }}",
                "username": "={{ $json.username }}",
                "email": "={{ $json.email }}",
                "phone": "={{ $json.phone }}",
                "website": "={{ $json.website }}"
            },
            "matchingColumns": [
                "email"
            ],
            "schema": [
                {
                    "id": "name",
                    "displayName": "name",
                    "required": False,
                    "defaultMatch": False,
                    "display": True,
                    "type": "string",
                    "canBeUsedToMatch": True
                },
                {
                    "id": "username",
                    "displayName": "username",
                    "required": False,
                    "defaultMatch": False,
                    "display": True,
                    "type": "string",
                    "canBeUsedToMatch": True
                },
                {
                    "id": "email",
                    "displayName": "email",
                    "required": False,
                    "defaultMatch": False,
                    "display": True,
                    "type": "string",
                    "canBeUsedToMatch": True,
                    "removed": False
                },
                {
                    "id": "phone",
                    "displayName": "phone",
                    "required": False,
                    "defaultMatch": False,
                    "display": True,
                    "type": "string",
                    "canBeUsedToMatch": True
                },
                {
                    "id": "website",
                    "displayName": "website",
                    "required": False,
                    "defaultMatch": False,
                    "display": True,
                    "type": "string",
                    "canBeUsedToMatch": True
                }
            ],
            "attemptToConvertTypes": False,
            "convertFieldsToString": False
        },
        credential_id="Heyjvh3DnLP9bR1B",
        credential_name="Google Sheets account 3",
        position=[240, -16]
    )
    
    # Add nodes to workflow
    workflow.add_nodes(trigger, http, sheets)
    
    # Connect nodes
    workflow.connect(trigger, http)
    workflow.connect(http, sheets)
    
    return workflow


if __name__ == "__main__":
    print("Creating sample n8n workflow...")
    
    try:
        # Create the sample workflow
        workflow = create_sample_workflow()
        
        print(f"Created workflow: {workflow.name}")
        print(f"Number of nodes: {len(workflow.nodes)}")
        print(f"Node names: {[node.name for node in workflow.nodes]}")
        print(f"Number of connections: {len(workflow.connections)}")
        
        # Export the workflow to a JSON file
        output_path = "n8n-workflows/workflow.json"
        workflow.export(output_path, pretty=True, validate=True)
        
        print(f"Sample workflow created and exported to {output_path}")
        print("✅ Workflow export completed successfully!")
        
        # Validate the created workflow
        validation_errors = workflow.validate()
        if validation_errors:
            print(f"⚠️  Workflow validation warnings: {validation_errors}")
        else:
            print("✅ Workflow validation passed!")
            
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)