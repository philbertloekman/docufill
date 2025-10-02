# DocuFill Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     DocuFill Application                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐              ┌──────────────┐            │
│  │   Frontend   │◄────────────►│   Backend    │            │
│  │  (HTML/CSS)  │   pywebview  │   (Python)   │            │
│  └──────────────┘              └──────────────┘            │
│         │                              │                     │
│         │                              │                     │
│         ▼                              ▼                     │
│  ┌──────────────┐              ┌──────────────┐            │
│  │  Mantine UI  │              │  API Layer   │            │
│  │  Components  │              │ (DocuFillAPI)│            │
│  └──────────────┘              └──────────────┘            │
│                                        │                     │
│                          ┌─────────────┼─────────────┐      │
│                          ▼             ▼             ▼      │
│                   ┌───────────┐ ┌───────────┐ ┌─────────┐ │
│                   │   Excel   │ │ Document  │ │  File   │ │
│                   │  Reader   │ │  Filler   │ │ System  │ │
│                   └───────────┘ └───────────┘ └─────────┘ │
│                          │             │             │      │
│                          └─────────────┼─────────────┘      │
│                                        ▼                     │
│                                ┌──────────────┐            │
│                                │  File System │            │
│                                │  templates/  │            │
│                                │  output/     │            │
│                                └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Frontend Layer (`index.html`)

**Responsibilities:**
- User interface rendering
- User input handling
- Form generation
- API communication

**Key Components:**
- Navigation sidebar
- Template selection grid
- Dynamic form builder
- Alert/notification system
- Tag input for multiple values

**Communication:**
- JavaScript → Python via `pywebview.api`
- Async/await pattern for API calls

### 2. Backend Layer (`app.py`)

**DocuFillAPI Class**

```python
DocuFillAPI
├── __init__()              # Setup directories
├── get_templates()         # List all templates
├── validate_template()     # Validate configuration
├── get_template_fields()   # Get form fields
├── fill_documents()        # Process documents
├── refresh_templates()     # Reload templates and Excel configs
└── open_folder()          # Open file explorer
```

**Data Flow:**
1. Frontend calls API method
2. API validates request
3. API delegates to utility classes
4. API returns structured response
5. Frontend updates UI

### 3. Utility Layer

#### Excel Reader (`src/utils/excel_reader.py`)

```python
ExcelConfigReader
├── __init__(file_path)
├── read_fields()           # Read all fields
├── validate_config()       # Validate structure
├── get_field_keys()        # Get key list
├── get_field_by_key()      # Lookup field
├── get_multiple_value_fields()
└── get_single_value_fields()

Private Methods:
├── _validate_file()        # Check file exists
├── _validate_columns()     # Check columns
├── _parse_dataframe()      # Parse Excel data
├── _get_multiple_value()   # Get multiple flag
└── _parse_boolean()        # Parse TRUE/FALSE
```

#### Document Filler (`src/utils/document_filler.py`)

```python
DocumentFiller
├── fill_document()         # Fill single document
├── fill_multiple_documents() # Fill multiple
└── _replace_in_text()      # Replace placeholders

Helper Functions:
└── create_output_filename() # Generate timestamped name
```

### 4. Constants Layer (`src/constants/excel_constants.py`)

```python
EXCEL_COLUMNS = {
    'LABEL': 'label',
    'KEY': 'key',
    'MULTIPLE': 'multiple',
    'TYPE': 'type',
    'NOTE': 'note'
}

EXCEL_REQUIRED_COLUMNS = ['label', 'key']
EXCEL_MULTIPLE_COLUMNS = ['multiple', 'type']
EXCEL_BOOLEAN_MAPPING = {'TRUE': True, 'FALSE': False}
DEFAULT_CONFIG_EXCEL_FILENAME = 'config.xlsx'
```

## Data Flow

### Template Loading Flow

```
1. User opens app
   ↓
2. Frontend: Call get_templates()
   ↓
3. Backend: Scan templates/ directory
   ↓
4. Backend: For each folder:
   - Find config.xlsx
   - Find .docx files
   - Count documents
   ↓
5. Backend: Return template list
   ↓
6. Frontend: Render template cards
   ↓
7. User clicks template
   ↓
8. Frontend: Call validate_template()
   ↓
9. Backend: Validate configuration
   ↓
10. Frontend: Show validation result
```

### Document Filling Flow

```
1. User selects template
   ↓
2. Frontend: Call get_template_fields()
   ↓
3. Backend: Read config.xlsx
   ↓
4. ExcelConfigReader: Parse fields
   ↓
5. Backend: Return field list
   ↓
6. Frontend: Generate form
   ↓
7. User fills form
   ↓
8. User clicks "Fill Documents"
   ↓
9. Frontend: Collect form data
   ↓
10. Frontend: Call fill_documents()
    ↓
11. Backend: Get template documents
    ↓
12. DocumentFiller: For each document:
    - Load .docx file
    - Replace placeholders
    - Save to output/
    ↓
13. Backend: Return results
    ↓
14. Frontend: Show success message
```

## File System Structure

```
docufill/
│
├── templates/                    # Input templates
│   └── {Template Name}/
│       ├── config.xlsx          # Configuration
│       ├── Document1.docx       # Template 1
│       ├── Document2.docx       # Template 2
│       └── ...
│
├── output/                      # Filled documents
│   ├── 20251001_153045_Document1.docx
│   ├── 20251001_153045_Document2.docx
│   └── ...
│
├── src/                         # Source code
│   ├── constants/
│   │   └── excel_constants.py
│   └── utils/
│       ├── excel_reader.py
│       └── document_filler.py
│
├── app.py                       # Backend entry point
├── index.html                   # Frontend UI
└── venv/                        # Virtual environment
```

## API Endpoints

### `get_templates() → List[Dict]`

**Returns:**
```json
[
  {
    "name": "Template Name",
    "path": "/path/to/template",
    "has_config": true,
    "config_file": "config.xlsx",
    "docx_files": ["Doc1.docx", "Doc2.docx"],
    "file_count": 2
  }
]
```

### `validate_template(name) → Dict`

**Returns:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Field 'x' has empty label"]
}
```

### `get_template_fields(name) → List[Dict]`

**Returns:**
```json
[
  {
    "label": "Client Name",
    "key": "client_name",
    "multiple": false,
    "note": "Full legal name"
  }
]
```

### `fill_documents(name, data) → Dict`

**Request:**
```json
{
  "client_name": "John Doe",
  "team_members": ["Alice", "Bob"]
}
```

**Returns:**
```json
{
  "success": true,
  "message": "Successfully filled 2 documents",
  "files": ["20251001_153045_Doc1.docx"],
  "errors": []
}
```

### `refresh_templates() → Dict`

**Returns:**
```json
{
  "success": true,
  "message": "Successfully refreshed 3 template(s)",
  "template_count": 3
}
```

## Error Handling

### Frontend
- Try-catch blocks around API calls
- Display user-friendly error messages
- Graceful degradation

### Backend
- Exception handling at API level
- Detailed error messages for debugging
- Structured error responses

### Validation Layers
1. **File Level**: Check file existence
2. **Structure Level**: Check Excel columns
3. **Data Level**: Check field values
4. **Business Level**: Check duplicate keys

## Security Considerations

### File System Access
- Restricted to templates/ and output/ directories
- No arbitrary file access
- Safe path handling with pathlib

### Input Validation
- Excel file format validation
- Field key format validation (alphanumeric + underscore)
- No code injection in placeholders

### Output Safety
- Timestamped filenames prevent overwrites
- Output directory isolation
- No executable content in documents

## Performance Considerations

### Optimization Points
1. **Template Caching**: Could cache template validation
2. **Lazy Loading**: Load templates on-demand
3. **Async Processing**: Large documents in background
4. **Batch Operations**: Multiple documents at once

### Current Performance
- Fast for typical use (< 100 fields, < 10 documents)
- Excel reading: ~50-100ms per file
- Document filling: ~100-200ms per document
- UI updates: Immediate feedback

## Testing Strategy

### Unit Tests (`test_excel_reader.py`)
- Excel reader functionality
- Field parsing
- Validation logic
- Edge cases

### Integration Tests (Manual)
- Template loading
- Form generation
- Document filling
- File system operations

### CLI Tool (`cli_excel_reader.py`)
- Quick validation
- Template testing
- Field inspection

## Extension Points

### Adding New Features

1. **New Field Types**
   - Add to `EXCEL_COLUMNS` constant
   - Update `ExcelConfigReader` parsing
   - Update frontend form generation

2. **New Document Formats**
   - Create new filler class (PDF, etc.)
   - Add to `DocumentFiller` or separate utility
   - Update API to handle new formats

3. **Additional Validation**
   - Add to `validate_config()` method
   - Define validation rules in constants
   - Update error messages

4. **Custom UI Components**
   - Add to `index.html`
   - Style with CSS
   - Connect to backend API

## Dependencies

### Core
- `pandas` - Excel data manipulation
- `openpyxl` - Excel file format
- `python-docx` - Word document processing
- `pywebview` - Desktop app framework

### Python Standard Library
- `pathlib` - Path handling
- `datetime` - Timestamps
- `typing` - Type hints

## Deployment

### Desktop Application
- Bundle with PyInstaller
- Include templates/
- Create installer for OS

### Requirements
- Python 3.8+
- macOS/Windows/Linux
- Modern web browser (for UI rendering)

## Maintenance

### Code Organization
- Clear separation of concerns
- Modular architecture
- Documented functions
- Type hints throughout

### Extensibility
- Plugin-ready architecture
- Configuration-driven
- API-based communication
- Utility functions

### Documentation
- Code comments
- Docstrings
- Architecture docs (this file)
- User guides

---

This architecture provides a solid foundation for a desktop document filling application with room for growth and customization.

