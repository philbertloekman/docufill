"""
Document Filler Utility for DocuFill
Fills Word documents with data from form submissions using docxtpl
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from docx import Document
from docxtpl import DocxTemplate
import subprocess
import tempfile
import shutil


class DocumentFiller:
    """Fill Word documents with form data"""
    
    def __init__(self):
        pass
    
    def fill_document(self, template_path: str | Path, output_path: str | Path, data: Dict[str, Any]) -> bool:
        """
        Fill a Word document with data
        
        Args:
            template_path: Path to the template Word document
            output_path: Path where filled document should be saved
            data: Dictionary mapping field keys to values
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            FileNotFoundError: If template doesn't exist
            Exception: For other errors during processing
        """
        template_path = Path(template_path)
        output_path = Path(output_path)
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template document not found: {template_path}")
        
        try:
            # Handle .doc files by converting to .docx first
            if template_path.suffix.lower() == '.doc':
                return self._fill_doc_file(template_path, output_path, data)
            else:
                return self._fill_docx_file(template_path, output_path, data)
        
        except Exception as e:
            raise Exception(f"Error filling document: {str(e)}")
    
    def _fill_docx_file(self, template_path: Path, output_path: Path, data: Dict[str, Any]) -> bool:
        """Fill a .docx file with data using docxtpl"""
        # Load the document template
        doc = DocxTemplate(str(template_path))
        
        # Prepare data for docxtpl
        context = {}
        for key, value in data.items():
            if isinstance(value, list):
                # For multiple values, keep as list for Jinja2 to handle
                context[key] = [str(item) for item in value if item]
            elif value is None:
                context[key] = ''
            else:
                context[key] = str(value)
        
        # Render the document
        doc.render(context)
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the filled document
        doc.save(str(output_path))
        
        return True
    
    
    def _fill_doc_file(self, template_path: Path, output_path: Path, data: Dict[str, Any]) -> bool:
        """Fill a .doc file by converting to .docx first"""
        # Create a temporary .docx file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_docx_path = Path(temp_file.name)
        
        try:
            # Convert .doc to .docx using LibreOffice
            if self._convert_doc_to_docx(template_path, temp_docx_path):
                # Fill the converted .docx file
                self._fill_docx_file(temp_docx_path, output_path, data)
                return True
            else:
                # Fallback: copy the file and warn user
                print(f"Warning: .doc files cannot be filled automatically. Copying {template_path.name} without filling placeholders.")
                print(f"To fill .doc files, please convert them to .docx format first.")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(template_path, output_path)
                return True
        
        finally:
            # Clean up temporary file
            if temp_docx_path.exists():
                temp_docx_path.unlink()
    
    def _convert_doc_to_docx(self, doc_path: Path, docx_path: Path) -> bool:
        """Convert .doc file to .docx using LibreOffice"""
        try:
            # Try to use LibreOffice to convert
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'docx',
                '--outdir', str(docx_path.parent),
                str(doc_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # LibreOffice creates the file with the same name but .docx extension
                expected_docx = docx_path.parent / f"{doc_path.stem}.docx"
                if expected_docx.exists():
                    expected_docx.rename(docx_path)
                    return True
            
            return False
        
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # LibreOffice not available or conversion failed
            return False
    
    
    
    def fill_multiple_documents(self, template_dir: str | Path, output_dir: str | Path, 
                                docx_files: List[str], data: Dict[str, Any],
                                timestamp: str = None, template_name: str = None) -> Dict[str, Any]:
        """
        Fill multiple Word documents from a template directory
        
        Args:
            template_dir: Directory containing template documents
            output_dir: Directory where filled documents should be saved
            docx_files: List of document filenames to process
            data: Dictionary mapping field keys to values
            timestamp: Optional timestamp string for output filenames
            template_name: Name of the template for folder organization
            
        Returns:
            Dictionary with results:
            - success: bool
            - filled_files: list of filled filenames
            - errors: list of error messages
        """
        template_dir = Path(template_dir)
        output_dir = Path(output_dir)
        
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Create timestamped folder for this template
        if template_name:
            timestamped_folder = f"{timestamp}_{template_name}"
            output_folder = output_dir / timestamped_folder
        else:
            output_folder = output_dir
        
        # Create the output folder
        output_folder.mkdir(parents=True, exist_ok=True)
        
        filled_files = []
        errors = []
        
        for docx_file in docx_files:
            # Skip temporary Word files
            if docx_file.startswith('~$'):
                continue
            
            template_path = template_dir / docx_file
            
            if not template_path.exists():
                errors.append(f"Template not found: {docx_file}")
                continue
            
            try:
                # Create output path in the timestamped folder
                output_path = output_folder / docx_file
                
                # Fill the document
                self.fill_document(template_path, output_path, data)
                
                # Add relative path for display
                if template_name:
                    filled_files.append(f"{timestamped_folder}/{docx_file}")
                else:
                    filled_files.append(docx_file)
            
            except Exception as e:
                errors.append(f"Error filling {docx_file}: {str(e)}")
        
        return {
            'success': len(filled_files) > 0,
            'filled_files': filled_files,
            'errors': errors,
            'output_folder': str(output_folder)
        }


def create_output_filename(original_filename: str, timestamp: str = None) -> str:
    """
    Create an output filename with timestamp
    
    Args:
        original_filename: Original template filename
        timestamp: Optional timestamp string
        
    Returns:
        Filename with timestamp prefix
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    return f"{timestamp}_{original_filename}"

