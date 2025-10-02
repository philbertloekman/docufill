# DocuFill - Document Template Filler

A beautiful desktop application for filling Word document templates with data from Excel configurations. Built with Python, pywebview, and Mantine UI.

## Features

✨ **Modern UI** - Clean, responsive interface built with Mantine components  
📊 **Excel Configuration** - Define fields and validation in Excel  
📝 **Multiple Documents** - Fill multiple Word documents at once  
🔄 **Multiple Values** - Support for fields with multiple entries  
✅ **Validation** - Automatic validation of templates before use  
💾 **Timestamped Output** - Automatically organized output files  
🎯 **User-Friendly** - Tooltips and notes for every field  

## Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd docufill
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify setup
```bash
python check_setup.py
```

This will check that all dependencies, directories, and files are in place.

## Usage

### Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python app.py
```

The application will open in a new window with a modern desktop interface.

## Template Structure

Each template is a folder in the `template/` directory with the following structure:

```
template/
└── My Template/
    ├── config.xlsx          # Configuration file (required)
    ├── Document1.docx       # Word template 1
    ├── Document2.docx       # Word template 2
    └── ...                  # More Word documents
```

### Excel Configuration Format

The `config.xlsx` file should have the following columns:

| Column | Required | Description |
|--------|----------|-------------|
| `label` | Yes | Display name shown to user in form |
| `key` | Yes | Placeholder key used in Word documents (e.g., `client_name`) |
| `type` or `multiple` | No | `TRUE` if field accepts multiple values, `FALSE` for single value |
| `note` | No | Help text/instructions shown to the user |

#### Example Excel Configuration:

| label | key | type | note |
|-------|-----|------|------|
| Client Name | client_name | FALSE | Full legal name of the client |
| Project Name | project_name | FALSE | Name of the project |
| Team Members | team_members | TRUE | Add all team members |
| Start Date | start_date | FALSE | Format: MM/DD/YYYY |

### Word Document Placeholders

In your Word documents, use curly braces to mark placeholders:

```
Dear {client_name},

This document is for {project_name}.

Team members: {team_members}

Start date: {start_date}
```

When you fill out the form, the placeholders will be replaced with the actual values.

## How to Use

### 1. Create a Template

1. Create a new folder in `template/`
2. Add a `config.xlsx` file with your field definitions
3. Add one or more `.docx` files with placeholders like `{field_key}`

### 2. Fill Documents

1. Launch the application: `python app.py`
2. Select a template from the list
3. Fill out the form fields
   - For single-value fields, just type the value
   - For multiple-value fields, type and press Enter to add each value
4. Click "Fill Documents"
5. Your filled documents will be saved in the `output/` folder with timestamps

### 3. Access Output Files

- Click "Browse Folders" → "Open Output Folder" in the app
- Or navigate to the `output/` folder manually
- Files are named: `YYYYMMDD_HHMMSS_OriginalName.docx`

## Features in Detail

### Template Validation

Templates are automatically validated when loaded:
- ✅ Valid templates show a green badge
- ❌ Invalid templates show errors and cannot be used
- Validation checks:
  - Config file exists
  - Required columns present
  - No duplicate field keys
  - Valid key formats (letters, numbers, underscores only)

### Multiple Value Fields

Fields marked with `type=TRUE` or `multiple=TRUE` allow multiple entries:
- Type a value and press Enter to add
- Click the × to remove a value
- Press Backspace when input is empty to remove the last value
- Multiple values are joined with commas in the output

### Field Notes

Hover over or view the note (💡) under each field for:
- Format requirements (e.g., "MM/DD/YYYY")
- Validation rules (e.g., "10-digit phone number")
- Examples (e.g., "Full legal name of taxpayer")

## Project Structure

```
docufill/
├── app.py                       # Main application entry point
├── run.sh                       # Quick start script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   └── index.html          # Frontend UI (Mantine components)
│   ├── constants/
│   │   ├── __init__.py
│   │   └── excel_constants.py  # Excel configuration constants
│   └── utils/
│       ├── excel_reader.py     # Excel configuration reader
│       └── document_filler.py  # Word document filler utility
├── template/                    # Template folders
│   ├── Exchange Agreement Package/
│   │   ├── config.xlsx
│   │   └── *.docx
│   ├── ID Form and Timeline/
│   │   ├── config.xlsx
│   │   └── *.docx
│   └── Sub of Buyer/
│       ├── config.xlsx
│       └── *.docx
├── test/                        # Testing and development tools
│   ├── test_excel_reader.py   # Test suite for Excel reader
│   ├── cli_excel_reader.py    # CLI tool for testing configs
│   └── check_setup.py          # Setup verification tool
└── output/                      # Generated documents (timestamped)
```

## Development Tools

### Test Excel Reader

```bash
# Test all templates
python test/test_excel_reader.py

# Test specific template  
python test/test_excel_reader.py "template/My Template/config.xlsx"
```

### CLI Excel Reader

```bash
# List all templates
python test/cli_excel_reader.py --list-templates

# Test specific template
python test/cli_excel_reader.py --template "Exchange Agreement Package"

# Verbose output
python test/cli_excel_reader.py --template "My Template" --verbose
```

### Setup Checker

```bash
# Verify your setup
python test/check_setup.py
```

### Convert .doc to .docx

```bash
# Convert all .doc files in a template folder
python convert_doc_to_docx.py "template/ID Form and Timeline"

# Convert all .doc files in all templates
python convert_doc_to_docx.py --all

# Convert a single file
python convert_doc_to_docx.py "path/to/file.doc"
```

## API Reference

### DocuFillAPI Class

The backend API exposed to the frontend:

#### Methods

- `get_templates()` - Get all available templates
- `validate_template(template_name)` - Validate a template's configuration
- `get_template_fields(template_name)` - Get fields for a template
- `fill_documents(template_name, form_data)` - Fill documents with data
- `open_folder(folder_type)` - Open templates or output folder

### ExcelConfigReader Class

For reading Excel configurations:

- `read_fields()` - Read all fields from Excel
- `validate_config()` - Validate configuration
- `get_field_keys()` - Get list of field keys
- `get_field_by_key(key)` - Get specific field
- `get_multiple_value_fields()` - Get fields accepting multiple values

### DocumentFiller Class

For filling Word documents:

- `fill_document(template_path, output_path, data)` - Fill single document
- `fill_multiple_documents(template_dir, output_dir, docx_files, data)` - Fill multiple documents

## Troubleshooting

### Template not showing up
- Make sure the folder is in `template/`
- Ensure `config.xlsx` exists and is valid
- Check that Excel file has required columns: `label`, `key`

### Fields not filling in Word document
- Ensure placeholder format is `{field_key}` (with curly braces)
- Check that the key in Excel matches the placeholder exactly
- Placeholders are case-sensitive

### .doc files not filling
- **Issue**: Legacy `.doc` files cannot be filled automatically
- **Solution**: Convert `.doc` files to `.docx` format
- **Conversion**: Use the provided script: `python convert_doc_to_docx.py <template_folder>`
- **Manual**: Open in Word and "Save As" → `.docx` format
- **Validation**: Templates with only `.doc` files are marked as invalid and cannot be used

### Template validation errors
- **Issue**: Template shows as invalid and cannot be opened
- **Common causes**:
  - No `.docx` files found (only `.doc` files)
  - Invalid Excel configuration file
  - Missing required columns in Excel file
  - Corrupted Excel file
- **Solution**: Fix the validation errors shown when clicking the template
- **Close errors**: Click the × button or press Escape to close error messages

### Application won't start
- Make sure virtual environment is activated
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8 or higher recommended)

## Dependencies

- **pandas** - Excel file reading
- **openpyxl** - Excel file format support
- **python-docx** - Word document manipulation
- **pywebview** - Desktop application framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues, questions, or contributions, please open an issue on GitHub.