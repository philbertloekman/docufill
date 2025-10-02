#!/usr/bin/env python3
"""
DocuFill Setup Checker
Verifies that the application is properly set up and ready to run
"""

import sys
from pathlib import Path

def check_dependencies():
    """Check if all required Python packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = {
        'pandas': 'pandas',
        'openpyxl': 'openpyxl',
        'docx': 'python-docx',
        'webview': 'pywebview'
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    return missing

def check_directories():
    """Check if required directories exist"""
    print("\n📁 Checking directories...")
    
    base_dir = Path(__file__).parent.parent
    required_dirs = {
        'template': base_dir / 'template',
        'output': base_dir / 'output',
        'src': base_dir / 'src',
        'src/ui': base_dir / 'src' / 'ui',
        'src/utils': base_dir / 'src' / 'utils',
        'src/constants': base_dir / 'src' / 'constants',
    }
    
    missing = []
    for name, path in required_dirs.items():
        if path.exists():
            print(f"  ✅ {name}/")
        else:
            print(f"  ❌ {name}/ - MISSING")
            missing.append(path)
    
    return missing

def check_files():
    """Check if required files exist"""
    print("\n📄 Checking files...")
    
    base_dir = Path(__file__).parent.parent
    required_files = {
        'app.py': base_dir / 'app.py',
        'index.html': base_dir / 'src' / 'ui' / 'index.html',
        'requirements.txt': base_dir / 'requirements.txt',
        'excel_reader.py': base_dir / 'src' / 'utils' / 'excel_reader.py',
        'document_filler.py': base_dir / 'src' / 'utils' / 'document_filler.py',
        'excel_constants.py': base_dir / 'src' / 'constants' / 'excel_constants.py',
    }
    
    missing = []
    for name, path in required_files.items():
        if path.exists():
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - MISSING")
            missing.append(path)
    
    return missing

def check_templates():
    """Check if templates exist and are valid"""
    print("\n📋 Checking templates...")
    
    templates_dir = Path(__file__).parent.parent / 'template'
    
    if not templates_dir.exists():
        print("  ⚠️  Templates directory not found")
        return []
    
    template_folders = [d for d in templates_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if not template_folders:
        print("  ⚠️  No template folders found")
        print("  ℹ️  Add template folders to template/ to get started")
        return []
    
    print(f"  ✅ Found {len(template_folders)} template folder(s)")
    
    for folder in template_folders:
        config_file = folder / 'config.xlsx'
        docx_files = list(folder.glob('*.docx')) + list(folder.glob('*.doc'))
        docx_files = [f for f in docx_files if not f.name.startswith('~$')]
        
        has_config = config_file.exists()
        has_docs = len(docx_files) > 0
        
        status = "✅" if (has_config and has_docs) else "⚠️"
        print(f"  {status} {folder.name}")
        
        if not has_config:
            print(f"      ❌ config.xlsx missing")
        else:
            print(f"      ✅ config.xlsx found")
        
        if not has_docs:
            print(f"      ❌ No Word documents found")
        else:
            print(f"      ✅ {len(docx_files)} Word document(s)")
    
    return []

def check_virtual_env():
    """Check if running in virtual environment"""
    print("\n🐍 Checking Python environment...")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print(f"  ✅ Running in virtual environment")
    else:
        print(f"  ⚠️  Not in virtual environment")
        print(f"  ℹ️  Recommended: source venv/bin/activate")
    
    print(f"  Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    return in_venv

def main():
    """Run all checks"""
    print("=" * 60)
    print("DocuFill Setup Checker")
    print("=" * 60)
    
    issues = []
    
    # Check Python environment
    in_venv = check_virtual_env()
    if not in_venv:
        issues.append("Not in virtual environment")
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        issues.extend([f"Missing package: {pkg}" for pkg in missing_deps])
    
    # Check directories
    missing_dirs = check_directories()
    if missing_dirs:
        issues.extend([f"Missing directory: {d}" for d in missing_dirs])
    
    # Check files
    missing_files = check_files()
    if missing_files:
        issues.extend([f"Missing file: {f}" for f in missing_files])
    
    # Check templates
    check_templates()
    
    # Summary
    print("\n" + "=" * 60)
    if not issues:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou're ready to run DocuFill:")
        print("  python app.py")
        print("\nOr use the startup script:")
        print("  ./run.sh")
    else:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        
        if missing_deps:
            print("\n💡 To fix missing packages:")
            print("  pip install -r requirements.txt")
        
        if not in_venv:
            print("\n💡 To use virtual environment:")
            print("  source venv/bin/activate")
            print("  Or create one: python3 -m venv venv")
    
    print("=" * 60)
    
    return 0 if not issues else 1

if __name__ == '__main__':
    sys.exit(main())

