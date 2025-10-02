#!/usr/bin/env python3
"""
Test script to verify API serialization works correctly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from app import DocuFillAPI
import json

def test_api_serialization():
    """Test that all API methods return serializable data"""
    api = DocuFillAPI()
    
    print("Testing API serialization...")
    
    # Test get_templates
    try:
        templates = api.get_templates()
        json.dumps(templates)  # This will fail if not serializable
        print("✅ get_templates() - serializable")
    except Exception as e:
        print(f"❌ get_templates() - not serializable: {e}")
        return False
    
    # Test validate_template for each template
    for template in templates:
        try:
            validation = api.validate_template(template['name'])
            json.dumps(validation)  # This will fail if not serializable
            print(f"✅ validate_template('{template['name']}') - serializable")
        except Exception as e:
            print(f"❌ validate_template('{template['name']}') - not serializable: {e}")
            return False
    
    # Test get_template_fields for valid templates
    for template in templates:
        validation = api.validate_template(template['name'])
        if validation['valid']:
            try:
                fields = api.get_template_fields(template['name'])
                json.dumps(fields)  # This will fail if not serializable
                print(f"✅ get_template_fields('{template['name']}') - serializable")
            except Exception as e:
                print(f"❌ get_template_fields('{template['name']}') - not serializable: {e}")
                return False
    
    # Test fill_documents for a valid template
    valid_template = None
    for template in templates:
        validation = api.validate_template(template['name'])
        if validation['valid']:
            valid_template = template
            break
    
    if valid_template:
        try:
            # Create test data
            test_data = {}
            fields = api.get_template_fields(valid_template['name'])
            for field in fields[:3]:  # Test with first 3 fields
                test_data[field['key']] = f"Test {field['label']}"
            
            result = api.fill_documents(valid_template['name'], test_data)
            json.dumps(result)  # This will fail if not serializable
            print(f"✅ fill_documents('{valid_template['name']}') - serializable")
        except Exception as e:
            print(f"❌ fill_documents('{valid_template['name']}') - not serializable: {e}")
            return False
    
    # Test open_folder
    try:
        result = api.open_folder('templates')
        json.dumps(result)  # This will fail if not serializable
        print("✅ open_folder('templates') - serializable")
    except Exception as e:
        print(f"❌ open_folder('templates') - not serializable: {e}")
        return False
    
    print("\n🎉 All API methods return serializable data!")
    return True

if __name__ == '__main__':
    success = test_api_serialization()
    sys.exit(0 if success else 1)
