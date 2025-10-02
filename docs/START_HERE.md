# 🚀 DocuFill - Start Here!

Welcome to DocuFill! This is your quick reference guide.

## ⚡ Quick Start

### First Time Setup
```bash
# 1. Create virtual environment (if not exists)
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify setup
python test/check_setup.py
```

### Running the App
```bash
# Easy way (recommended)
./run.sh

# Manual way
source venv/bin/activate
python app.py
```

## 📁 Project Structure

```
docufill/
├── app.py              # Run this to start the app
├── run.sh              # Or run this quick start script
│
├── src/                # All source code
│   ├── ui/            # Frontend (HTML/CSS/JS)
│   ├── utils/         # Backend utilities
│   └── constants/     # Configuration
│
├── template/          # Your templates go here
│   ├── Exchange Agreement Package/
│   ├── ID Form and Timeline/
│   └── Sub of Buyer/
│
├── test/              # Testing tools
│   ├── check_setup.py          # Verify installation
│   ├── cli_excel_reader.py     # Test templates
│   └── test_excel_reader.py    # Full test suite
│
└── output/            # Generated documents appear here
```

## 📋 Using Templates

### 1. Select Template
Open the app and click on any template card with a green ✓ badge.

### 2. Fill Form
- Type values for each field
- For multiple values: type and press **Enter** to add
- Hover over 💡 for field notes

### 3. Generate Documents
Click "Fill Documents" and find your files in `output/` folder!

## 🛠️ Creating Your Own Template

```bash
# 1. Create folder
mkdir template/"My Template"

# 2. Create config.xlsx with columns:
#    - label: Display name
#    - key: Placeholder name
#    - type: TRUE (multiple) or FALSE (single)
#    - note: Help text

# 3. Create Word documents with placeholders
#    Use {key} format, e.g., {client_name}

# 4. Test it
python test/cli_excel_reader.py --template "My Template" --verbose
```

## 🧪 Testing Tools

```bash
# Check if everything is set up correctly
python test/check_setup.py

# List all templates
python test/cli_excel_reader.py --list-templates

# Test specific template
python test/cli_excel_reader.py --template "Template Name" --verbose

# Run full test suite
python test/test_excel_reader.py
```

## 📚 Documentation

- **[README.md](README.md)** - Complete documentation
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute tutorial
- **[STRUCTURE.md](STRUCTURE.md)** - Project structure guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep-dive

## ❓ Common Issues

### Template not appearing?
```bash
# Check setup
python test/check_setup.py

# Verify template
python test/cli_excel_reader.py --template "Template Name"
```

### App won't start?
```bash
# Make sure virtual environment is active
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Placeholders not replaced?
- Use `{key}` format with curly braces
- Keys are case-sensitive
- Check spelling matches Excel config

## 🎯 Key Commands

| Action | Command |
|--------|---------|
| Start app | `./run.sh` or `python app.py` |
| Check setup | `python test/check_setup.py` |
| List templates | `python test/cli_excel_reader.py --list-templates` |
| Test template | `python test/cli_excel_reader.py --template "Name"` |
| Open templates folder | In app: Browse Folders → Templates |
| Open output folder | In app: Browse Folders → Output |

## ✨ Features

- ✅ Modern, beautiful UI
- ✅ Excel-based configuration
- ✅ Multiple document support
- ✅ Multiple value fields
- ✅ Field notes/tooltips
- ✅ Automatic validation
- ✅ Timestamped output
- ✅ Error handling

## 🎉 You're Ready!

Run `./run.sh` to start using DocuFill!

Need help? Check the documentation files listed above.

---

**Version**: 2.0  
**Last Updated**: October 1, 2025

