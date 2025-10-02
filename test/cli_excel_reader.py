#!/usr/bin/env python3
"""
CLI tool for testing Excel configuration reader
Usage: python cli_excel_reader.py [config_file_path]
"""

import sys
import argparse
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.excel_reader import ExcelConfigReader, find_config_file


def main():
    parser = argparse.ArgumentParser(description='Test Excel configuration reader')
    parser.add_argument('config_file', nargs='?', help='Path to Excel config file (optional)')
    parser.add_argument('--list-templates', action='store_true', help='List all available templates')
    parser.add_argument('--template', help='Test specific template by name')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    if args.list_templates:
        list_templates()
        return
    
    if args.template:
        test_template(args.template, args.verbose)
        return
    
    if args.config_file:
        test_specific_file(args.config_file, args.verbose)
    else:
        # Test all templates
        test_all_templates(args.verbose)


def list_templates():
    """List all available templates"""
    templates_dir = Path('template')
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return
    
    print("📁 Available templates:")
    for template_dir in sorted(templates_dir.iterdir()):
        if template_dir.is_dir():
            config_file = find_config_file(template_dir)
            if config_file:
                print(f"  ✅ {template_dir.name}")
            else:
                print(f"  ❌ {template_dir.name} (no config.xlsx found)")


def test_template(template_name: str, verbose: bool = False):
    """Test a specific template by name"""
    template_dir = Path('template') / template_name
    
    if not template_dir.exists():
        print(f"❌ Template '{template_name}' not found")
        return
    
    config_file = find_config_file(template_dir)
    if not config_file:
        print(f"❌ No config.xlsx found in template '{template_name}'")
        return
    
    test_specific_file(str(config_file), verbose)


def test_specific_file(file_path: str, verbose: bool = False):
    """Test a specific Excel file"""
    print(f"🔍 Testing: {file_path}")
    print("=" * 60)
    
    try:
        reader = ExcelConfigReader(file_path)
        fields = reader.read_fields()
        
        print(f"✅ Successfully read {len(fields)} fields")
        
        if verbose:
            print("\n📋 Field details:")
            for i, field in enumerate(fields, 1):
                multiple_indicator = "📝 (multiple)" if field['multiple'] else "📄 (single)"
                print(f"  {i:2d}. {multiple_indicator} {field['label']}")
                print(f"      Key: {{{field['key']}}}")
                if field['note']:
                    print(f"      Note: {field['note']}")
                print()
        else:
            # Show summary
            multiple_fields = reader.get_multiple_value_fields()
            single_fields = reader.get_single_value_fields()
            
            print(f"📝 Multiple value fields: {len(multiple_fields)}")
            print(f"📄 Single value fields: {len(single_fields)}")
            
            if multiple_fields:
                print("\nMultiple value fields:")
                for field in multiple_fields:
                    print(f"  - {field['label']}")
        
        # Validation
        validation = reader.validate_config()
        if validation['valid']:
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration has errors:")
            for error in validation['errors']:
                print(f"  - {error}")
        
        if validation['warnings']:
            print("⚠️  Warnings:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()


def test_all_templates(verbose: bool = False):
    """Test all available templates"""
    templates_dir = Path('template')
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return
    
    config_files = []
    for template_dir in templates_dir.iterdir():
        if template_dir.is_dir():
            config_file = find_config_file(template_dir)
            if config_file:
                config_files.append((template_dir.name, config_file))
    
    if not config_files:
        print("❌ No config files found")
        return
    
    print(f"🔍 Found {len(config_files)} templates to test")
    print("=" * 60)
    
    all_passed = True
    
    for template_name, config_path in config_files:
        print(f"\n📋 {template_name}")
        print("-" * 40)
        
        try:
            reader = ExcelConfigReader(config_path)
            fields = reader.read_fields()
            validation = reader.validate_config()
            
            print(f"✅ {len(fields)} fields, {'valid' if validation['valid'] else 'invalid'}")
            
            if not validation['valid']:
                all_passed = False
                for error in validation['errors']:
                    print(f"  ❌ {error}")
            
            if validation['warnings']:
                for warning in validation['warnings']:
                    print(f"  ⚠️  {warning}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All templates passed validation!")
    else:
        print("❌ Some templates failed validation")


if __name__ == '__main__':
    main()
