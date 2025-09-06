#!/usr/bin/env python3
"""
Test script for error handling and logging functionality.

This script tests the custom exception classes and logging configuration
to ensure they work correctly with the SDK.
"""

import sys
import os

# Add the current directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from n8n_python_sdk.workflow import Workflow
from n8n_python_sdk.node import Node
from n8n_python_sdk.nodes.manual_trigger import ManualTriggerNode
from n8n_python_sdk.exceptions import WorkflowError, NodeError, ValidationError, ExportError
from n8n_python_sdk.logging_config import configure_logging, enable_debug_logging
import logging


def test_logging_configuration():
    """Test the logging configuration functionality."""
    print("🧪 Testing logging configuration...")
    
    # Test basic configuration
    logger = configure_logging(level='DEBUG')
    logger.info("Logging configuration test successful")
    
    # Test debug logging
    enable_debug_logging()
    logger.debug("Debug logging is working")
    
    print("✅ Logging configuration tests passed")


def test_workflow_error_handling():
    """Test workflow error handling."""
    print("🧪 Testing workflow error handling...")
    
    # Test empty workflow name
    try:
        workflow = Workflow("")
        print("❌ Empty workflow name should raise WorkflowError")
        return False
    except WorkflowError as e:
        print(f"✅ Caught expected WorkflowError for empty name: {e}")
    
    # Test duplicate node addition
    try:
        workflow = Workflow("Test Workflow")
        node1 = ManualTriggerNode(name="Trigger", node_id="test-id")
        node2 = ManualTriggerNode(name="Trigger 2", node_id="test-id")  # Same ID
        
        workflow.add_node(node1)
        workflow.add_node(node2)  # Should raise WorkflowError
        print("❌ Duplicate node ID should raise WorkflowError")
        return False
    except WorkflowError as e:
        print(f"✅ Caught expected WorkflowError for duplicate node: {e}")
    
    # Test connection to non-existent node
    try:
        workflow = Workflow("Test Workflow")
        node1 = ManualTriggerNode(name="Trigger 1")
        node2 = ManualTriggerNode(name="Trigger 2")
        
        workflow.add_node(node1)
        # Don't add node2 to workflow
        workflow.connect(node1, node2)  # Should raise WorkflowError
        print("❌ Connection to non-existent node should raise WorkflowError")
        return False
    except WorkflowError as e:
        print(f"✅ Caught expected WorkflowError for non-existent node connection: {e}")
    
    print("✅ Workflow error handling tests passed")
    return True


def test_node_error_handling():
    """Test node error handling."""
    print("🧪 Testing node error handling...")
    
    # Test empty node type
    try:
        node = Node("", "Test Node")
        print("❌ Empty node type should raise NodeError")
        return False
    except NodeError as e:
        print(f"✅ Caught expected NodeError for empty node type: {e}")
    
    # Test empty node name
    try:
        node = Node("test.node", "")
        print("❌ Empty node name should raise NodeError")
        return False
    except NodeError as e:
        print(f"✅ Caught expected NodeError for empty node name: {e}")
    
    print("✅ Node error handling tests passed")
    return True


def test_export_error_handling():
    """Test export error handling."""
    print("🧪 Testing export error handling...")
    
    # Test export validation error
    try:
        workflow = Workflow("Test Workflow")
        # Empty workflow should fail validation
        workflow.export("/tmp/test_workflow.json", validate=True)
        print("❌ Empty workflow export should raise ValidationError")
        return False
    except ValidationError as e:
        print(f"✅ Caught expected ValidationError for empty workflow: {e}")
    except ExportError as e:
        # ValidationError might be wrapped in ExportError
        if "validation failed" in str(e).lower():
            print(f"✅ Caught expected validation error (as ExportError): {e}")
        else:
            print(f"❌ Unexpected ExportError: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")
        return False
    
    print("✅ Export error handling tests passed")
    return True


def test_successful_workflow_creation():
    """Test successful workflow creation with logging."""
    print("🧪 Testing successful workflow creation...")
    
    try:
        # Create a valid workflow
        workflow = Workflow("Test Success Workflow")
        node = ManualTriggerNode(name="Success Trigger")
        workflow.add_node(node)
        
        # Test export without validation errors
        workflow.export("/tmp/test_success_workflow.json", validate=True)
        
        print("✅ Successful workflow creation and export")
        return True
    except Exception as e:
        print(f"❌ Unexpected error in successful workflow test: {type(e).__name__}: {e}")
        return False


def main():
    """Run all error handling and logging tests."""
    print("🚀 Starting error handling and logging tests...\n")
    
    all_tests_passed = True
    
    try:
        # Configure logging for tests
        test_logging_configuration()
        print()
        
        # Run error handling tests
        if not test_workflow_error_handling():
            all_tests_passed = False
        print()
        
        if not test_node_error_handling():
            all_tests_passed = False
        print()
        
        if not test_export_error_handling():
            all_tests_passed = False
        print()
        
        if not test_successful_workflow_creation():
            all_tests_passed = False
        print()
        
    except Exception as e:
        print(f"❌ Test suite failed with unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        all_tests_passed = False
    
    # Final results
    print("="*50)
    if all_tests_passed:
        print("🎉 All error handling and logging tests PASSED!")
        print("✅ Custom exceptions are working correctly")
        print("✅ Logging configuration is functional") 
        print("✅ Error handling is comprehensive")
        return True
    else:
        print("❌ Some error handling tests FAILED!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)