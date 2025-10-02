#!/usr/bin/env python3
"""
DocuFill - Document Template Filler Application
Main application entry point with webview backend
"""

import webview
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.excel_reader import ExcelConfigReader, find_config_file
from utils.document_filler import DocumentFiller


class DocuFillAPI:
    """API for DocuFill application"""
    
    def __init__(self):
        self.base_dir = str(Path(__file__).parent)
        self.templates_dir = str(Path(__file__).parent / 'template')
        self.output_dir = str(Path(__file__).parent / 'output')
        
        # Create directories if they don't exist
        Path(self.templates_dir).mkdir(exist_ok=True)
        Path(self.output_dir).mkdir(exist_ok=True)
        
        self.document_filler = DocumentFiller()
    
    def get_templates(self):
        """Get all available templates with their files"""
        templates = []
        
        try:
            for template_folder in Path(self.templates_dir).iterdir():
                if not template_folder.is_dir():
                    continue
                
                # Skip hidden folders
                if template_folder.name.startswith('.'):
                    continue
                
                # Find config file
                config_file = find_config_file(template_folder)
                
                # Find Word documents (excluding temp files)
                docx_files = [
                    f.name for f in template_folder.glob('*.docx')
                    if not f.name.startswith('~$')
                ]
                doc_files = [
                    f.name for f in template_folder.glob('*.doc')
                    if not f.name.startswith('~$')
                ]
                
                all_doc_files = docx_files + doc_files
                
                templates.append({
                    'name': str(template_folder.name),
                    'path': str(template_folder),
                    'has_config': bool(config_file is not None),
                    'config_file': str(config_file.name) if config_file else None,
                    'docx_files': [str(f) for f in all_doc_files],
                    'file_count': int(len(all_doc_files))
                })
        
        except Exception as e:
            print(f"Error getting templates: {e}")
        
        return templates
    
    def validate_template(self, template_name):
        """
        Validate a template's configuration and documents
        
        Returns:
            Dictionary with validation results
        """
        try:
            template_path = Path(self.templates_dir) / template_name
            
            if not template_path.exists():
                return {
                    'valid': False,
                    'errors': ['Template folder not found']
                }
            
            # Find config file
            config_file = find_config_file(template_path)
            
            if not config_file:
                return {
                    'valid': False,
                    'errors': ['No config.xlsx file found in template folder']
                }
            
            # Validate the config file
            reader = ExcelConfigReader(config_file)
            validation = reader.validate_config()
            
            # Check for document files
            doc_files = list(template_path.glob('*.doc*'))
            if not doc_files:
                validation['errors'].append('No Word documents (.doc or .docx) found in template folder')
            
            # Check for .doc files and warn about limitations
            doc_files_legacy = [f for f in doc_files if f.suffix.lower() == '.doc']
            if doc_files_legacy:
                if 'warnings' not in validation:
                    validation['warnings'] = []
                validation['warnings'].append(f'Found {len(doc_files_legacy)} .doc file(s) - these cannot be filled automatically. Convert to .docx for full functionality.')
            
            # Check for .docx files
            docx_files = [f for f in doc_files if f.suffix.lower() == '.docx']
            if not docx_files:
                validation['errors'].append('No .docx files found - at least one .docx file is required for document filling')
            
            # Update validation status based on errors
            validation['valid'] = len(validation['errors']) == 0
            
            # Ensure all values are serializable
            return {
                'valid': bool(validation['valid']),
                'errors': [str(e) for e in validation['errors']],
                'warnings': [str(w) for w in validation.get('warnings', [])]
            }
        
        except Exception as e:
            return {
                'valid': False,
                'errors': [str(f'Error validating template: {str(e)}')]
            }
    
    def get_template_fields(self, template_name):
        """
        Get fields from Excel config file for a specific template
        
        Returns:
            List of field dictionaries
        """
        try:
            # First validate the template
            validation = self.validate_template(template_name)
            
            if not validation['valid']:
                # Template is invalid, raise an exception with error details
                error_message = "Template validation failed:\n" + "\n".join(validation['errors'])
                if validation.get('warnings'):
                    error_message += "\n\nWarnings:\n" + "\n".join(validation['warnings'])
                raise Exception(error_message)
            
            template_path = Path(self.templates_dir) / template_name
            config_file = find_config_file(template_path)
            
            if not config_file:
                raise Exception("Config file not found")
            
            reader = ExcelConfigReader(config_file)
            fields = reader.read_fields()
            
            # Ensure all field values are serializable
            serializable_fields = []
            for field in fields:
                serializable_field = {}
                for key, value in field.items():
                    if isinstance(value, (str, int, float, bool, type(None))):
                        serializable_field[key] = value
                    else:
                        serializable_field[key] = str(value)
                serializable_fields.append(serializable_field)
            
            return serializable_fields
        
        except Exception as e:
            print(f"Error reading template fields: {e}")
            raise e
    
    def fill_documents(self, template_name, form_data):
        """
        Fill all documents in a template with form data
        
        Args:
            template_name: Name of the template folder
            form_data: Dictionary mapping field keys to values
            
        Returns:
            Dictionary with results
        """
        try:
            template_path = Path(self.templates_dir) / template_name
            
            if not template_path.exists():
                return {
                    'success': False,
                    'message': 'Template folder not found'
                }
            
            # Find all Word documents
            docx_files = [
                f.name for f in template_path.glob('*.docx')
                if not f.name.startswith('~$')
            ]
            doc_files = [
                f.name for f in template_path.glob('*.doc')
                if not f.name.startswith('~$')
            ]
            
            all_doc_files = docx_files + doc_files
            
            if not all_doc_files:
                return {
                    'success': False,
                    'message': 'No Word documents found in template folder'
                }
            
            # Generate timestamp for output files
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Fill all documents
            result = self.document_filler.fill_multiple_documents(
                template_dir=template_path,
                output_dir=Path(self.output_dir),
                docx_files=all_doc_files,
                data=form_data,
                timestamp=timestamp,
                template_name=template_name
            )
            
            # Add warnings for .doc files
            doc_files = [f for f in all_doc_files if f.endswith('.doc')]
            if doc_files:
                if 'warnings' not in result:
                    result['warnings'] = []
                result['warnings'].extend([
                    f"Note: {f} is a .doc file and cannot be filled automatically. "
                    f"Please convert to .docx format for full functionality."
                    for f in doc_files
                ])
            
            if result['success']:
                message = f"Successfully filled {len(result['filled_files'])} document(s)"
                if result['errors']:
                    message += f" with {len(result['errors'])} error(s)"
                
                # Add output folder info
                output_folder = result.get('output_folder', '')
                if output_folder:
                    folder_name = str(Path(output_folder).name)
                    message += f"<br><br>📁 Saved to: <strong>{folder_name}</strong>"
                
                return {
                    'success': True,
                    'message': str(message),
                    'files': [str(f) for f in result['filled_files']],
                    'errors': [str(e) for e in result['errors']],
                    'warnings': [str(w) for w in result.get('warnings', [])],
                    'output_folder': str(output_folder)
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to fill documents',
                    'errors': [str(e) for e in result['errors']]
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': str(f'Error filling documents: {str(e)}')
            }
    
    def open_folder(self, folder_type):
        """Open templates or output folder in file explorer"""
        try:
            if folder_type == 'templates':
                folder_path = Path(self.templates_dir)
            elif folder_type == 'output':
                folder_path = Path(self.output_dir)
            else:
                return {'success': False, 'message': 'Invalid folder type'}
            
            # Create folder if it doesn't exist
            folder_path.mkdir(exist_ok=True)
            
            # Open folder in file explorer
            if os.name == 'nt':  # Windows
                os.startfile(str(folder_path))
            elif os.name == 'posix':  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    os.system(f'open "{folder_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{folder_path}"')
            
            return {'success': True, 'message': str(f'Opened {folder_type} folder')}
        
        except Exception as e:
            return {'success': False, 'message': str(f'Error opening folder: {str(e)}')}
    
    def open_template_folder(self, template_name):
        """Open specific template folder in file explorer"""
        try:
            template_path = Path(self.templates_dir) / template_name
            
            if not template_path.exists():
                return {'success': False, 'message': f'Template folder not found: {template_name}'}
            
            # Open folder in file explorer
            if os.name == 'nt':  # Windows
                os.startfile(str(template_path))
            elif os.name == 'posix':  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    os.system(f'open "{template_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{template_path}"')
            
            return {'success': True, 'message': f'Opened template folder: {template_name}'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error opening template folder: {str(e)}'}
    
    def open_output_folder(self, folder_name):
        """Open specific output folder in file explorer"""
        try:
            output_folder_path = Path(self.output_dir) / folder_name
            
            if not output_folder_path.exists():
                return {'success': False, 'message': f'Output folder not found: {folder_name}'}
            
            # Open folder in file explorer
            if os.name == 'nt':  # Windows
                os.startfile(str(output_folder_path))
            elif os.name == 'posix':  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    os.system(f'open "{output_folder_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{output_folder_path}"')
            
            return {'success': True, 'message': f'Opened output folder: {folder_name}'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error opening output folder: {str(e)}'}
    
    def get_output_folders(self):
        """Get list of output folders with creation dates, sorted by newest first"""
        try:
            output_dir = Path(self.output_dir)
            
            if not output_dir.exists():
                return []
            
            folders = []
            for item in output_dir.iterdir():
                if item.is_dir():
                    # Get creation time
                    stat = item.stat()
                    created_at = stat.st_ctime
                    
                    folders.append({
                        'name': item.name,
                        'created_at': created_at,
                        'path': str(item)
                    })
            
            # Sort by creation time, newest first
            folders.sort(key=lambda x: x['created_at'], reverse=True)
            
            return folders
        
        except Exception as e:
            print(f"Error getting output folders: {e}")
            return []
    
    def get_latest_output_folders(self, limit=10):
        """Get the latest output folders, limited to specified count"""
        try:
            folders = self.get_output_folders()
            
            # Limit to the specified number
            limited_folders = folders[:limit]
            
            # Format the data for display
            formatted_folders = []
            for folder in limited_folders:
                # Parse timestamp from folder name (format: YYYY-MM-DD_HH-MM-SS_Template-Name)
                folder_name = folder['name']
                parts = folder_name.split('_', 2)  # Split into max 3 parts
                
                if len(parts) >= 2:
                    date_part = parts[0]  # YYYY-MM-DD
                    time_part = parts[1]  # HH-MM-SS
                    template_name = parts[2] if len(parts) > 2 else 'Unknown Template'
                    
                    # Format the timestamp for display
                    try:
                        # Parse the timestamp
                        timestamp_str = f"{date_part} {time_part.replace('-', ':')}"
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                        formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        formatted_date = folder_name
                else:
                    template_name = folder_name
                    formatted_date = "Unknown Date"
                
                formatted_folders.append({
                    'name': folder_name,
                    'template_name': template_name,
                    'created_date': formatted_date,
                    'path': folder['path']
                })
            
            return formatted_folders
        
        except Exception as e:
            print(f"Error getting latest output folders: {e}")
            return []


def main():
    """Main application entry point"""
    # Create API instance
    api = DocuFillAPI()
    
    # Get the path to the HTML file
    html_file = Path(__file__).parent / 'src' / 'ui' / 'index.html'
    
    # Create webview window
    window = webview.create_window(
        'DocuFill - Document Template Filler',
        str(html_file),
        width=1400,
        height=900,
        min_size=(1000, 700),
        js_api=api
    )
    
    # Start the application
    webview.start(debug=True)


if __name__ == '__main__':
    main()

