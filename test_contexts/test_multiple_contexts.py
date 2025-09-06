#!/usr/bin/env python3
"""
Test SDK imports in multiple contexts and scenarios.

This comprehensive test ensures the SDK works correctly in various scenarios
that users might encounter.
"""

import sys
import os
import tempfile
import subprocess

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import_after_chdir():
    """Test imports after changing working directory."""
    print("🧪 Testing imports after changing directory...")
    
    original_cwd = os.getcwd()
    try:
        # Change to a different directory
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            
            from n8n_python_sdk import Workflow, ManualTriggerNode
            
            workflow = Workflow("Directory Change Test")
            trigger = ManualTriggerNode(name="Test Trigger")
            workflow.add_node(trigger)
            
            print("✅ Import after directory change successful")
            return True
            
    except Exception as e:
        print(f"❌ Import after directory change failed: {e}")
        return False
    finally:
        os.chdir(original_cwd)


def test_subprocess_import():
    """Test importing SDK in a subprocess."""
    print("🧪 Testing imports in subprocess...")
    
    try:
        # Create a simple test script
        test_script = '''
import sys
sys.path.insert(0, r"{}")

try:
    from n8n_python_sdk import Workflow, __version__
    workflow = Workflow("Subprocess Test")
    print(f"SUCCESS: Created workflow in subprocess, SDK version: {{__version__}}")
except Exception as e:
    print(f"ERROR: {{e}}")
    sys.exit(1)
'''.format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Run the script in a subprocess
        result = subprocess.run([
            sys.executable, '-c', test_script
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and "SUCCESS:" in result.stdout:
            print("✅ Subprocess import test successful")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Subprocess import failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Subprocess import test failed: {e}")
        return False


def test_repeated_imports():
    """Test importing the same modules multiple times."""
    print("🧪 Testing repeated imports...")
    
    try:
        # Import multiple times to test for side effects
        for i in range(3):
            from n8n_python_sdk import Workflow, Node
            from n8n_python_sdk import ManualTriggerNode, HTTPRequestNode
            
            # Create objects to ensure functionality
            workflow = Workflow(f"Repeated Import Test {i+1}")
            node = ManualTriggerNode(name=f"Test Node {i+1}")
            workflow.add_node(node)
        
        print("✅ Repeated imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Repeated imports failed: {e}")
        return False


def test_selective_imports():
    """Test various selective import patterns."""
    print("🧪 Testing selective import patterns...")
    
    try:
        # Test different selective import patterns
        from n8n_python_sdk import Workflow
        from n8n_python_sdk import (ManualTriggerNode, HTTPRequestNode)
        from n8n_python_sdk import configure_logging as setup_logging
        from n8n_python_sdk import WorkflowError, NodeError
        
        # Test functionality
        setup_logging(level='WARNING')
        workflow = Workflow("Selective Import Test")
        trigger = ManualTriggerNode(name="Selective Trigger")
        http = HTTPRequestNode(name="Selective HTTP", url="https://test.example")
        
        workflow.add_nodes(trigger, http)
        workflow.connect(trigger, http)
        
        print("✅ Selective import patterns successful")
        return True
        
    except Exception as e:
        print(f"❌ Selective import patterns failed: {e}")
        return False


def test_error_handling_imports():
    """Test that error handling works correctly with imports."""
    print("🧪 Testing error handling with imports...")
    
    try:
        from n8n_python_sdk import Workflow, WorkflowError, NodeError, ErrorCodes
        
        # Test error scenarios
        try:
            workflow = Workflow("")  # Should raise WorkflowError
            print("❌ Empty workflow name should have raised error")
            return False
        except WorkflowError as e:
            if e.code == ErrorCodes.WORKFLOW_INVALID_NAME:
                print("✅ WorkflowError correctly raised and handled")
            else:
                print(f"❌ Unexpected error code: {e.code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling import test failed: {e}")
        return False


def main():
    """Run all context tests."""
    print("🚀 Starting SDK package context tests...\n")
    
    all_tests_passed = True
    test_functions = [
        test_import_after_chdir,
        test_subprocess_import,
        test_repeated_imports,
        test_selective_imports,
        test_error_handling_imports
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
        print("🎉 All SDK package context tests PASSED!")
        print("✅ Package works correctly in different contexts")
        print("✅ Imports are robust and reliable")
        print("✅ Error handling works as expected")
        print("✅ Package initialization is stable")
        return True
    else:
        print("❌ Some SDK package context tests FAILED!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)