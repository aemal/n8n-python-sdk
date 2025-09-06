#!/usr/bin/env python3
"""
n8n Python SDK - Workflow Validation Script

This script validates the exported workflow by comparing it with the original
and testing various node configurations to ensure flexibility.
"""

import sys
import os
import json

# Add the current directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from n8n_python_sdk.workflow import Workflow
from n8n_python_sdk.nodes.manual_trigger import ManualTriggerNode
from n8n_python_sdk.nodes.http_request import HTTPRequestNode
from n8n_python_sdk.nodes.google_sheets import GoogleSheetsNode


def compare_workflows():
    """Compare the generated workflow with the original PRD example."""
    print("🔍 Comparing generated workflow with PRD example...")
    
    # Load the generated workflow
    try:
        with open("n8n-workflows/workflow.json", "r") as f:
            generated = json.load(f)
    except FileNotFoundError:
        print("❌ Generated workflow file not found!")
        return False
    
    # Load the original workflow
    try:
        with open("n8n/n8n-sample-workflows/workflow001.json", "r") as f:
            original = json.load(f)
    except FileNotFoundError:
        print("❌ Original workflow file not found!")
        return False
    
    # Compare key structures
    checks = [
        ("Number of nodes", len(generated["nodes"]), len(original["nodes"])),
        ("Manual trigger node type", generated["nodes"][0]["type"], original["nodes"][0]["type"]),
        ("HTTP request node type", generated["nodes"][1]["type"], original["nodes"][1]["type"]),
        ("Google Sheets node type", generated["nodes"][2]["type"], original["nodes"][2]["type"]),
        ("Number of connections", len(generated["connections"]), len(original["connections"])),
    ]
    
    all_passed = True
    for check_name, generated_value, original_value in checks:
        if generated_value == original_value:
            print(f"✅ {check_name}: Match ({generated_value})")
        else:
            print(f"❌ {check_name}: Mismatch (generated: {generated_value}, original: {original_value})")
            all_passed = False
    
    # Check node parameters
    print("\n🔍 Checking node parameters...")
    
    # HTTP Request URL
    gen_url = generated["nodes"][1]["parameters"]["url"]
    orig_url = original["nodes"][1]["parameters"]["url"]
    if gen_url == orig_url:
        print(f"✅ HTTP Request URL: Match ({gen_url})")
    else:
        print(f"❌ HTTP Request URL: Mismatch")
        all_passed = False
    
    # Google Sheets operation
    gen_op = generated["nodes"][2]["parameters"]["operation"]
    orig_op = original["nodes"][2]["parameters"]["operation"]
    if gen_op == orig_op:
        print(f"✅ Google Sheets operation: Match ({gen_op})")
    else:
        print(f"❌ Google Sheets operation: Mismatch")
        all_passed = False
    
    return all_passed


def test_node_configurations():
    """Test different node configurations to ensure flexibility."""
    print("\n🧪 Testing node configuration flexibility...")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Different HTTP methods
    total_tests += 1
    try:
        http_post = HTTPRequestNode(
            name="POST Request",
            url="https://api.example.com/users",
            method="POST",
            body={"name": "Test User"},
            body_content_type="json"
        )
        print("✅ Test 1: HTTP POST configuration successful")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 1: HTTP POST configuration failed: {e}")
    
    # Test 2: Different Google Sheets configurations
    total_tests += 1
    try:
        sheets_read = GoogleSheetsNode(
            name="Read Sheet",
            operation="read",
            document_id="test-document-id",
            sheet_name="Sheet1"
        )
        print("✅ Test 2: Google Sheets read configuration successful")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 2: Google Sheets read configuration failed: {e}")
    
    # Test 3: Workflow validation with different configurations
    total_tests += 1
    try:
        test_workflow = Workflow("Test Workflow")
        trigger = ManualTriggerNode(name="Test Trigger")
        test_workflow.add_node(trigger)
        
        validation_errors = test_workflow.validate()
        if not validation_errors:
            print("✅ Test 3: Workflow validation successful")
            tests_passed += 1
        else:
            print(f"❌ Test 3: Workflow validation failed: {validation_errors}")
    except Exception as e:
        print(f"❌ Test 3: Workflow validation failed: {e}")
    
    print(f"\n📊 Configuration tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests


def main():
    """Main validation function."""
    print("🚀 Starting workflow validation...\n")
    
    # Test 1: Compare with PRD example
    comparison_passed = compare_workflows()
    
    # Test 2: Test node configurations
    config_tests_passed = test_node_configurations()
    
    # Final results
    print("\n" + "="*50)
    if comparison_passed and config_tests_passed:
        print("🎉 All validation tests PASSED!")
        print("✅ The sample workflow implementation successfully reproduces the PRD example")
        print("✅ Node configurations are flexible and working correctly")
        return True
    else:
        print("❌ Some validation tests FAILED!")
        if not comparison_passed:
            print("❌ Generated workflow doesn't match PRD example")
        if not config_tests_passed:
            print("❌ Node configuration tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)