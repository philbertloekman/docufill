#!/usr/bin/env python3
"""
Test script for Excel configuration reader
Tests the ExcelConfigReader with actual config files
"""

import sys
import os
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.excel_reader import ExcelConfigReader, read_config, find_config_file
from constants.excel_constants import EXCEL_COLUMNS, EXCEL_REQUIRED_COLUMNS


def test_excel_reader():
    """Test the Excel reader with all available config files"""
    
    # Find all template directories
    templates_dir = Path('template')
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    config_files = []
    for template_dir in templates_dir.iterdir():
        if template_dir.is_dir():
            config_file = find_config_file(template_dir)
            if config_file:
                config_files.append((template_dir.name, config_file))
    
    if not config_files:
        print("❌ No config files found")
        return False
    
    print(f"🔍 Found {len(config_files)} config files to test:")
    for name, path in config_files:
        print(f"  - {name}: {path}")
    
    print("\n" + "="*60)
    
    all_tests_passed = True
    
    for template_name, config_path in config_files:
        print(f"\n📋 Testing: {template_name}")
        print(f"📁 File: {config_path}")
        print("-" * 40)
        
        try:
            # Test 1: Basic reading
            print("1️⃣ Testing basic file reading...")
            reader = ExcelConfigReader(config_path)
            fields = reader.read_fields()
            print(f"   ✅ Successfully read {len(fields)} fields")
            
            # Test 2: Validation
            print("2️⃣ Testing configuration validation...")
            validation = reader.validate_config()
            if validation['valid']:
                print("   ✅ Configuration is valid")
            else:
                print("   ❌ Configuration has errors:")
                for error in validation['errors']:
                    print(f"      - {error}")
                all_tests_passed = False
            
            if validation['warnings']:
                print("   ⚠️  Warnings:")
                for warning in validation['warnings']:
                    print(f"      - {warning}")
            
            # Test 3: Field details
            print("3️⃣ Field details:")
            if fields:
                for i, field in enumerate(fields[:5], 1):  # Show first 5 fields
                    multiple_indicator = "📝 (multiple)" if field['multiple'] else "📄 (single)"
                    print(f"   {i}. {multiple_indicator} {field['label']}")
                    print(f"      Key: {{{field['key']}}}")
                    if field['note']:
                        print(f"      Note: {field['note']}")
                
                if len(fields) > 5:
                    print(f"   ... and {len(fields) - 5} more fields")
            else:
                print("   ⚠️  No fields found")
            
            # Test 4: Convenience functions
            print("4️⃣ Testing convenience functions...")
            fields_alt = read_config(config_path)
            if len(fields_alt) == len(fields):
                print("   ✅ read_config() works correctly")
            else:
                print("   ❌ read_config() returned different results")
                all_tests_passed = False
            
            # Test 5: Field filtering
            print("5️⃣ Testing field filtering...")
            multiple_fields = reader.get_multiple_value_fields()
            single_fields = reader.get_single_value_fields()
            all_keys = reader.get_field_keys()
            
            print(f"   📝 Multiple value fields: {len(multiple_fields)}")
            print(f"   📄 Single value fields: {len(single_fields)}")
            print(f"   🔑 Total field keys: {len(all_keys)}")
            
            if len(multiple_fields) + len(single_fields) == len(fields):
                print("   ✅ Field filtering works correctly")
            else:
                print("   ❌ Field filtering mismatch")
                all_tests_passed = False
            
            # Test 6: Field lookup
            if fields:
                print("6️⃣ Testing field lookup...")
                first_key = fields[0]['key']
                found_field = reader.get_field_by_key(first_key)
                if found_field and found_field['key'] == first_key:
                    print(f"   ✅ Field lookup works for key: {first_key}")
                else:
                    print(f"   ❌ Field lookup failed for key: {first_key}")
                    all_tests_passed = False
            
        except Exception as e:
            print(f"   ❌ Error testing {template_name}: {e}")
            all_tests_passed = False
        
        print()
    
    print("="*60)
    if all_tests_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")
    
    return all_tests_passed


def test_specific_file(file_path: str):
    """Test a specific Excel file"""
    print(f"🔍 Testing specific file: {file_path}")
    print("="*60)
    
    try:
        reader = ExcelConfigReader(file_path)
        
        # Show raw DataFrame info
        import pandas as pd
        df = pd.read_excel(file_path)
        print(f"📊 Raw DataFrame info:")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   First few rows:")
        print(df.head().to_string())
        print()
        
        # Test our reader
        fields = reader.read_fields()
        print(f"📋 Parsed fields ({len(fields)}):")
        for i, field in enumerate(fields, 1):
            multiple_indicator = "📝" if field['multiple'] else "📄"
            print(f"   {i}. {multiple_indicator} {field['label']}")
            print(f"      Key: {{{field['key']}}}")
            print(f"      Multiple: {field['multiple']}")
            if field['note']:
                print(f"      Note: {field['note']}")
            print()
        
        # Validation
        validation = reader.validate_config()
        print(f"✅ Validation: {'PASSED' if validation['valid'] else 'FAILED'}")
        if validation['errors']:
            print("Errors:")
            for error in validation['errors']:
                print(f"  - {error}")
        if validation['warnings']:
            print("Warnings:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Test specific file
        file_path = sys.argv[1]
        test_specific_file(file_path)
    else:
        # Test all config files
        test_excel_reader()
