# DocuFill Project Structure

## 📁 Directory Layout

```
docufill/
│
├── 🚀 Application Core
│   ├── app.py                      # Main backend application
│   ├── run.sh                      # Quick start script (./run.sh)
│   └── requirements.txt            # Python dependencies
│
├── 📚 Documentation
│   ├── README.md                   # Complete documentation
│   ├── QUICKSTART.md              # 5-minute setup guide
│   ├── ARCHITECTURE.md            # Technical architecture
│   ├── SUMMARY.md                 # Project summary
│   ├── PROJECT_OVERVIEW.md        # Complete overview
│   └── STRUCTURE.md               # This file
│
├── 💾 Source Code (src/)
│   ├── __init__.py
│   │
│   ├── ui/                         # User Interface
│   │   └── index.html             # Frontend HTML/CSS/JS
│   │
│   ├── utils/                      # Utility Functions
│   │   ├── __init__.py
│   │   ├── excel_reader.py        # Excel config parser
│   │   └── document_filler.py     # Word document processor
│   │
│   └── constants/                  # Configuration Constants
│       ├── __init__.py
│       └── excel_constants.py     # Excel column definitions
│
├── 🧪 Testing & Development (test/)
│   ├── check_setup.py             # Verify installation
│   ├── test_excel_reader.py       # Test suite
│   └── cli_excel_reader.py        # CLI validation tool
│
├── 📋 Templates (template/)
│   ├── Exchange Agreement Package/
│   │   ├── config.xlsx            # Field definitions
│   │   └── *.docx                 # 6 Word templates
│   │
│   ├── ID Form and Timeline/
│   │   ├── config.xlsx
│   │   └── *.doc                  # 2 Word templates
│   │
│   └── Sub of Buyer/
│       ├── config.xlsx
│       └── *.docx                 # 3 Word templates
│
├── 📤 Output (output/)
│   ├── .gitkeep                   # Keep folder in git
│   └── YYYYMMDD_HHMMSS_*.docx    # Generated documents
│
└── 🐍 Virtual Environment (venv/)
    └── ...                         # Python packages
```

## 🎯 Key Changes from Original Structure

### ✅ Renamed Directories
- `templates/` → `template/` (singular, cleaner)

### ✅ Organized Source Code
- Created `src/ui/` for frontend files
- Moved `index.html` → `src/ui/index.html`
- All UI code now in `src/` directory

### ✅ Created Test Directory
- Created `test/` for all testing tools
- Moved `test_excel_reader.py` → `test/`
- Moved `cli_excel_reader.py` → `test/`
- Moved `check_setup.py` → `test/`

## 📝 File Purposes

### Application Core

#### `app.py`
- Main application entry point
- Backend API (DocuFillAPI)
- Handles template loading and document filling
- Integration with pywebview

#### `run.sh`
- Quick start script
- Checks for virtual environment
- Installs dependencies if needed
- Launches application

### Source Code

#### `src/ui/index.html`
- Complete frontend interface
- Mantine-inspired CSS styling
- JavaScript for user interaction
- Communicates with Python backend via pywebview

#### `src/utils/excel_reader.py`
- Reads Excel configuration files
- Parses field definitions
- Validates configuration structure
- Supports both `type` and `multiple` columns

#### `src/utils/document_filler.py`
- Fills Word documents with data
- Replaces placeholders in paragraphs, tables, headers, footers
- Handles multiple value fields
- Generates timestamped output files

#### `src/constants/excel_constants.py`
- Column name definitions
- Boolean mappings
- Default configuration values

### Testing & Development

#### `test/check_setup.py`
- Verifies installation
- Checks dependencies
- Validates directory structure
- Tests template availability

#### `test/test_excel_reader.py`
- Comprehensive test suite
- Tests all templates
- Validates field parsing
- Checks for errors

#### `test/cli_excel_reader.py`
- Command-line interface
- Quick template validation
- List available templates
- Inspect field configurations

## 🚀 Usage Patterns

### Running the Application
```bash
# Quick start
./run.sh

# Manual start
source venv/bin/activate
python app.py
```

### Testing Templates
```bash
# Check setup
python test/check_setup.py

# List templates
python test/cli_excel_reader.py --list-templates

# Test specific template
python test/cli_excel_reader.py --template "Template Name" --verbose

# Run full test suite
python test/test_excel_reader.py
```

### Creating Templates
```bash
# Create new template folder
mkdir template/"My Template"

# Add configuration
cd template/"My Template"
# Create config.xlsx with required columns: label, key, type, note

# Add Word documents with placeholders
# Use {field_key} format in Word documents
```

## 🔧 Import Paths

### From Application Root
```python
# In app.py or root level scripts
from src.utils.excel_reader import ExcelConfigReader
from src.utils.document_filler import DocumentFiller
from src.constants.excel_constants import EXCEL_COLUMNS
```

### From Test Scripts
```python
# In test/ scripts
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.excel_reader import ExcelConfigReader
from constants.excel_constants import EXCEL_COLUMNS
```

## 📦 Distribution Structure

When packaging the application, include:

```
docufill/
├── app.py                  # Main application
├── requirements.txt        # Dependencies
├── src/                   # All source code
├── template/              # Example templates (optional)
├── output/                # Empty output directory
└── README.md             # User documentation
```

Exclude from distribution:
- `venv/` - Users create their own
- `test/` - Development tools only
- `output/*` - Generated files
- `.DS_Store`, `__pycache__/`, etc.

## 🎨 Design Principles

### Separation of Concerns
- **UI**: `src/ui/` - User interface
- **Logic**: `src/utils/` - Business logic
- **Config**: `src/constants/` - Configuration
- **Tests**: `test/` - Testing tools
- **Data**: `template/` and `output/` - User data

### Clean Imports
- All source code under `src/`
- Clear module hierarchy
- Easy to import and use

### Developer Friendly
- Tests isolated in `test/`
- Documentation at root level
- Clear file naming
- Comprehensive comments

## 🔄 Migration Notes

If you're updating from the old structure:

1. **Templates**: `templates/` → `template/`
2. **UI**: `index.html` → `src/ui/index.html`
3. **Tests**: `*.py` tools → `test/*.py`
4. **Imports**: Update any custom scripts to use new paths

All existing templates work without modification! 🎉

## 📊 Structure Benefits

### ✅ Better Organization
- Clear separation of concerns
- Easy to find files
- Logical grouping

### ✅ Scalability
- Easy to add new utilities to `src/utils/`
- Easy to add new UI components to `src/ui/`
- Easy to add new tests to `test/`

### ✅ Professional
- Industry-standard structure
- Clean, maintainable code
- Ready for distribution
- Template refresh functionality

### ✅ Development Friendly
- Tests don't clutter root
- Clear module boundaries
- Easy to navigate

---

**Structure Version**: 2.0  
**Last Updated**: October 1, 2025

