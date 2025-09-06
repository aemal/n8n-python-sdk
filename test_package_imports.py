#!/usr/bin/env python3
"""
Test script for SDK package imports and initialization.

This script tests that all classes and functions can be imported correctly
from the n8n_python_sdk package and that they work as expected.
"""

import sys
import os

# Add the current directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_imports():
    """Test importing core classes from the package."""
    print("🧪 Testing core class imports...")
    
    try:
        # Test direct imports
        from n8n_python_sdk import Workflow, Node
        print("✅ Successfully imported Workflow and Node")
        
        # Test instantiation
        workflow = Workflow("Test Workflow")
        print(f"✅ Successfully created workflow: {workflow.name}")
        
        # Test basic node creation
        node = Node("test.node", "Test Node")
        print(f"✅ Successfully created node: {node.name}")
        
        return True
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False


def test_specialized_node_imports():
    """Test importing specialized node classes."""
    print("🧪 Testing specialized node imports...")
    
    try:
        from n8n_python_sdk import ManualTriggerNode, HTTPRequestNode, GoogleSheetsNode
        print("✅ Successfully imported specialized node classes")
        
        # Test instantiation of each node type
        trigger = ManualTriggerNode(name="Test Trigger")
        print(f"✅ Successfully created ManualTriggerNode: {trigger.name}")
        
        http = HTTPRequestNode(name="Test HTTP", url="https://example.com")
        print(f"✅ Successfully created HTTPRequestNode: {http.name}")
        
        sheets = GoogleSheetsNode.append_or_update(name="Test Sheets")
        print(f"✅ Successfully created GoogleSheetsNode: {sheets.name}")
        
        return True
    except Exception as e:
        print(f"❌ Specialized node imports failed: {e}")
        return False


def test_exception_imports():
    """Test importing exception classes."""
    print("🧪 Testing exception class imports...")
    
    try:
        from n8n_python_sdk import (
            SDKError, WorkflowError, NodeError, ExportError, 
            ValidationError, SDKImportError, SDKConnectionError, ErrorCodes
        )
        print("✅ Successfully imported exception classes")
        
        # Test exception creation
        error = WorkflowError("Test error", ErrorCodes.WORKFLOW_INVALID_NAME)
        print(f"✅ Successfully created WorkflowError: {error}")
        
        # Test error codes
        code = ErrorCodes.NODE_INVALID_TYPE
        print(f"✅ Successfully accessed error code: {code}")
        
        return True
    except Exception as e:
        print(f"❌ Exception imports failed: {e}")
        return False


def test_logging_imports():
    """Test importing logging utilities."""
    print("🧪 Testing logging utility imports...")
    
    try:
        from n8n_python_sdk import (
            configure_logging, get_logger, set_log_level, 
            enable_debug_logging, disable_logging
        )
        print("✅ Successfully imported logging utilities")
        
        # Test logging configuration
        logger = configure_logging(level='INFO')
        print("✅ Successfully configured logging")
        
        # Test getting a logger
        custom_logger = get_logger('test')
        print("✅ Successfully got custom logger")
        
        return True
    except Exception as e:
        print(f"❌ Logging utility imports failed: {e}")
        return False


def test_version_info():
    """Test accessing version information."""
    print("🧪 Testing version information...")
    
    try:
        from n8n_python_sdk import __version__
        print(f"✅ Successfully imported version: {__version__}")
        
        # Verify version format
        if __version__ and isinstance(__version__, str):
            print("✅ Version has correct format")
            return True
        else:
            print("❌ Invalid version format")
            return False
    except Exception as e:
        print(f"❌ Version import failed: {e}")
        return False


def test_wildcard_import():
    """Test wildcard import functionality."""
    print("🧪 Testing wildcard import...")
    
    try:
        # Create a new namespace for wildcard import
        import importlib
        sdk_module = importlib.import_module('n8n_python_sdk')
        
        # Get all exported names
        exported_names = getattr(sdk_module, '__all__', [])
        print(f"✅ Found {len(exported_names)} exported names in __all__")
        
        # Test that all names in __all__ can be accessed
        missing_names = []
        for name in exported_names:
            if not hasattr(sdk_module, name):
                missing_names.append(name)
        
        if missing_names:
            print(f"❌ Missing names in module: {missing_names}")
            return False
        else:
            print("✅ All names in __all__ are accessible")
            return True
            
    except Exception as e:
        print(f"❌ Wildcard import test failed: {e}")
        return False


def test_end_to_end_workflow():
    """Test creating a complete workflow using imported classes."""
    print("🧪 Testing end-to-end workflow creation...")
    
    try:
        from n8n_python_sdk import (
            Workflow, ManualTriggerNode, HTTPRequestNode, 
            configure_logging, enable_debug_logging
        )
        
        # Configure logging for the test
        enable_debug_logging()
        
        # Create workflow with imported classes
        workflow = Workflow("Import Test Workflow")
        
        trigger = ManualTriggerNode(name="Start Process")
        http = HTTPRequestNode(
            name="Fetch API Data",
            url="https://jsonplaceholder.typicode.com/posts/1"
        )
        
        workflow.add_nodes(trigger, http)
        workflow.connect(trigger, http)
        
        # Test export
        workflow.export("/tmp/import_test_workflow.json")
        
        print("✅ Successfully created complete workflow using imports")
        print(f"   - Workflow: {workflow.name}")
        print(f"   - Nodes: {len(workflow.nodes)}")
        print(f"   - Connections: {len(workflow.connections)}")
        
        return True
    except Exception as e:
        print(f"❌ End-to-end workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_alternative_import_styles():
    """Test different import styles."""
    print("🧪 Testing alternative import styles...")
    
    try:
        # Test importing the whole module
        import n8n_python_sdk
        workflow = n8n_python_sdk.Workflow("Module Import Test")
        print("✅ Module-style import works")
        
        # Test importing with alias
        import n8n_python_sdk as n8n
        workflow2 = n8n.Workflow("Alias Import Test")
        print("✅ Alias import works")
        
        # Test selective imports
        from n8n_python_sdk import Workflow as WF, Node as N
        workflow3 = WF("Selective Import Test")
        node = N("test.type", "Test Node")
        print("✅ Selective imports with aliases work")
        
        return True
    except Exception as e:
        print(f"❌ Alternative import styles failed: {e}")
        return False


def main():
    """Run all import tests."""
    print("🚀 Starting SDK package import tests...\n")
    
    all_tests_passed = True
    test_functions = [
        test_core_imports,
        test_specialized_node_imports,
        test_exception_imports,
        test_logging_imports,
        test_version_info,
        test_wildcard_import,
        test_end_to_end_workflow,
        test_alternative_import_styles
    ]
    
    for test_func in test_functions:
        try:
            if not test_func():
                all_tests_passed = False
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with exception: {e}")
            all_tests_passed = False
            print()
    
    # Final results
    print("="*60)
    if all_tests_passed:
        print("🎉 All SDK package import tests PASSED!")
        print("✅ Core classes can be imported and used")
        print("✅ Specialized nodes work correctly")
        print("✅ Exception handling is accessible")
        print("✅ Logging utilities are functional")
        print("✅ Package initialization is working properly")
        return True
    else:
        print("❌ Some SDK package import tests FAILED!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)