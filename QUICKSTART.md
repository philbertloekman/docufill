# DocuFill Quick Start Guide

Get up and running with DocuFill in 5 minutes!

## 🚀 Quick Start

### 1. Install and Run

```bash
# Make the startup script executable (first time only)
chmod +x run.sh

# Run the application
./run.sh
```

Or manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python app.py
```

### 2. Using the Application

The application opens with a modern desktop interface showing your available templates.

#### **Fill Templates Tab**

1. **Select a Template**
   - Click on any template card with a green "✓ Valid" badge
   - Invalid templates will show errors and cannot be used

2. **Fill Out the Form**
   - Enter values for each field
   - For multiple-value fields: type and press Enter to add items
   - Hover over field notes (💡) for help

3. **Submit**
   - Click "Fill Documents" button
   - Files are saved to `output/` with timestamps

4. **Success!**
   - You'll see a success message with file names
   - Files are named: `YYYYMMDD_HHMMSS_OriginalName.docx`

5. **Refresh Templates** (when needed)
   - Click "🔄 Refresh Templates" button to reload templates
   - Use this when you add, remove, or modify template folders
   - The app will re-scan all Excel configurations

#### **Browse Folders Tab**

- **Templates Folder** - View and edit your templates
- **Output Folder** - Access your filled documents

## 📝 Creating Your First Template

### Step 1: Create Template Folder

```bash
mkdir template/"My First Template"
cd template/"My First Template"
```

### Step 2: Create Excel Configuration

Create `config.xlsx` with these columns:

| label | key | type | note |
|-------|-----|------|------|
| Client Name | client_name | FALSE | Full name of the client |
| Project Title | project_title | FALSE | Title of the project |
| Team Members | team_members | TRUE | Press Enter to add each member |
| Start Date | start_date | FALSE | Format: MM/DD/YYYY |

### Step 3: Create Word Template

Create `Letter.docx` with this content:

```
Dear {client_name},

Thank you for choosing us for {project_title}.

Our team will include: {team_members}

Project start date: {start_date}

Best regards,
Your Company
```

### Step 4: Test It!

1. Open DocuFill
2. Select "My First Template"
3. Fill out the form:
   - Client Name: John Doe
   - Project Title: Website Redesign
   - Team Members: Alice, Bob, Charlie (press Enter after each)
   - Start Date: 10/15/2025
4. Click "Fill Documents"
5. Open the output folder to see your filled document!

## 🎯 Key Features

### Multiple Values
For fields like lists, addresses, or team members:
- Type value and press **Enter** to add
- Click **×** to remove
- Press **Backspace** (when empty) to remove last item

### Placeholders in Word
Use `{key}` format:
- ✅ `{client_name}`
- ✅ `{project_title}`
- ❌ `{{client_name}}`
- ❌ `client_name`

### Field Types
- **Single Value** (`type=FALSE`): Regular text input
- **Multiple Values** (`type=TRUE`): Tag input with Enter to add

## 📋 Example Templates

The project includes 3 example templates in `template/`:
1. **Exchange Agreement Package** - 27 fields, 6 documents
2. **ID Form and Timeline** - 27 fields, 2 documents
3. **Sub of Buyer** - 27 fields, 3 documents

Study these to understand the template structure!

## 🛠️ Testing Your Templates

Use the CLI tool to validate templates before using them:

```bash
# List all templates
python test/cli_excel_reader.py --list-templates

# Test specific template
python test/cli_excel_reader.py --template "My First Template" --verbose
```

## ⚠️ Common Issues

### Template doesn't appear
- Check that `config.xlsx` exists
- Verify Excel has `label` and `key` columns
- Click "🔄 Refresh Templates" to reload templates
- Run validation: `python test/cli_excel_reader.py --template "YourTemplate"`

### Placeholders not replaced
- Use exact format: `{key}` with curly braces
- Keys are case-sensitive
- No spaces: `{client_name}` not `{ client_name }`

### Multiple values not working
- Set `type` column to `TRUE` in Excel
- Press Enter after typing each value
- Don't use commas manually

## 🎨 Tips & Tricks

1. **Organize Your Templates**
   - Use clear, descriptive folder names in `template/`
   - Group related documents together
   - Keep config.xlsx up to date

2. **Write Good Field Notes**
   - Explain format requirements
   - Give examples
   - Include validation rules

3. **Test Before Production**
   - Use the CLI tool to validate
   - Test with sample data first
   - Check all placeholders are replaced

4. **Backup Your Work**
   - Templates are just files - easy to backup
   - Output folder grows over time - archive old files
   - Keep template versions if you update them

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the example templates in `template/`
- Create your own templates
- Check out the API reference for advanced usage

## 💡 Need Help?

- Check [README.md](README.md) troubleshooting section
- Review example templates
- Test with CLI tool: `python test/cli_excel_reader.py --help`

Happy document filling! 🎉

