#!/usr/bin/env python3
"""
Test script that imports the SDK from a subdirectory.

This tests that the SDK can be imported from different directory contexts.
"""

import sys
import os

# Add the parent directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports_from_subdirectory():
    """Test importing SDK from a subdirectory."""
    print("🧪 Testing SDK imports from subdirectory...")
    
    try:
        from n8n_python_sdk import Workflow, ManualTriggerNode, HTTPRequestNode
        from n8n_python_sdk import configure_logging
        
        print("✅ Successfully imported SDK classes from subdirectory")
        
        # Test functionality
        configure_logging(level='INFO')
        workflow = Workflow("Subdirectory Test")
        
        trigger = ManualTriggerNode(name="Trigger from subdir")
        http = HTTPRequestNode(name="HTTP from subdir", url="https://example.com")
        
        workflow.add_nodes(trigger, http)
        workflow.connect(trigger, http)
        
        # Export to current directory
        workflow.export("subdirectory_test_workflow.json")
        
        print(f"✅ Successfully created workflow from subdirectory: {workflow.name}")
        print(f"   - Nodes: {len(workflow.nodes)}")
        print(f"   - Export location: {os.path.abspath('subdirectory_test_workflow.json')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Subdirectory import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_imports_from_subdirectory()
    if success:
        print("\n🎉 Subdirectory import test PASSED!")
    else:
        print("\n❌ Subdirectory import test FAILED!")
    sys.exit(0 if success else 1)