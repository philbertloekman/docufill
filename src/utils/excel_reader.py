"""
Excel Configuration Reader for DocuFill
Reads and parses Excel configuration files for document templates
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional

from constants.excel_constants import (
    EXCEL_COLUMNS,
    EXCEL_REQUIRED_COLUMNS,
    EXCEL_MULTIPLE_COLUMNS,
    EXCEL_BOOLEAN_MAPPING,
    DEFAULT_CONFIG_EXCEL_FILENAME
)


class ExcelConfigReader:
    """Read and parse Excel configuration files for templates"""
    
    def __init__(self, file_path: str | Path):
        """
        Initialize the Excel configuration reader
        
        Args:
            file_path: Path to the Excel configuration file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid Excel file
        """
        self.file_path = Path(file_path)
        self._validate_file()
    
    def _validate_file(self) -> None:
        """Validate that the file exists and is an Excel file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel configuration file not found: {self.file_path}")
        
        if self.file_path.suffix not in ['.xlsx', '.xls']:
            raise ValueError(f"File must be Excel format (.xlsx or .xls): {self.file_path}")
    
    def read_fields(self) -> List[Dict]:
        """
        Read template fields from Excel configuration file
        
        Returns:
            List of field dictionaries with keys: label, key, multiple, note
            
        Raises:
            ValueError: If required columns are missing or file is invalid
            
        Example:
            >>> reader = ExcelConfigReader('templates/my_template/config.xlsx')
            >>> fields = reader.read_fields()
            >>> for field in fields:
            ...     print(f"{field['label']}: {field['key']}")
        """
        try:
            df = pd.read_excel(self.file_path)
            return self._parse_dataframe(df)
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {e}")
    
    def _parse_dataframe(self, df: pd.DataFrame) -> List[Dict]:
        """
        Parse DataFrame into field list
        
        Args:
            df: Pandas DataFrame from Excel file
            
        Returns:
            List of field dictionaries
            
        Raises:
            ValueError: If required columns are missing
        """
        # Validate required columns exist
        self._validate_columns(df)
        
        fields = []
        
        for index, row in df.iterrows():
            # Extract key and skip if empty
            key = str(row.get(EXCEL_COLUMNS['KEY'], '')).strip()
            
            if not key or key.lower() == 'nan':
                continue
            
            # Build field dictionary
            field = {
                'label': str(row.get(EXCEL_COLUMNS['LABEL'], key)),
                'key': key,
                'multiple': self._get_multiple_value(row),
                'note': str(row.get(EXCEL_COLUMNS['NOTE'], ''))
            }
            
            fields.append(field)
        
        return fields
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        """
        Validate that DataFrame has all required columns
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValueError: If required columns are missing
        """
        missing_columns = [col for col in EXCEL_REQUIRED_COLUMNS if col not in df.columns]
        
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_columns)}\n"
                f"Required columns: {', '.join(EXCEL_REQUIRED_COLUMNS)}\n"
                f"Found columns: {', '.join(df.columns)}"
            )
    
    def _get_multiple_value(self, row) -> bool:
        """
        Get the multiple value from row, checking both 'multiple' and 'type' columns
        
        Args:
            row: Pandas Series row from DataFrame
            
        Returns:
            Boolean value indicating if field accepts multiple values
        """
        # Check each possible column for multiple value indicator
        for col in EXCEL_MULTIPLE_COLUMNS:
            if col in row.index:
                value = row.get(col)
                if value is not None and str(value).strip().lower() not in ['nan', '']:
                    # Auto-capitalize the value for consistency
                    if isinstance(value, str):
                        value_upper = value.strip().upper()
                        # Update the DataFrame with the capitalized value
                        row[col] = value_upper
                    return self._parse_boolean(value)
        
        # Default to False if no multiple column found
        return False
    
    def _parse_boolean(self, value) -> bool:
        """
        Parse various boolean representations from Excel
        
        Args:
            value: Value to parse (can be bool, string, number, etc.)
            
        Returns:
            Boolean value
            
        Examples:
            >>> reader._parse_boolean('TRUE')
            True
            >>> reader._parse_boolean('false')
            False
            >>> reader._parse_boolean(1)
            True
            >>> reader._parse_boolean('YES')
            True
        """
        # Handle actual boolean
        if isinstance(value, bool):
            return value
        
        # Handle string values
        if isinstance(value, str):
            value_upper = value.strip().upper()
            
            # Check against mapping
            if value_upper in EXCEL_BOOLEAN_MAPPING:
                return EXCEL_BOOLEAN_MAPPING[value_upper]
            
            # Additional common true values
            if value_upper in ['YES', 'Y', '1']:
                return True
            
            # Additional common false values
            if value_upper in ['NO', 'N', '0', '']:
                return False
        
        # Handle numeric values
        if isinstance(value, (int, float)):
            return bool(value)
        
        # Default to False for None or unknown values
        return False
    
    def _validate_multiple_column(self, df: pd.DataFrame) -> List[str]:
        """
        Validate that the multiple column contains only TRUE/FALSE values
        
        Args:
            df: DataFrame to validate
            
        Returns:
            List of error messages for invalid multiple column values
        """
        errors = []
        
        # Check if multiple column exists
        if 'multiple' not in df.columns:
            return errors  # No multiple column, no validation needed
        
        # Check each row in the multiple column
        for idx, value in df['multiple'].items():
            if pd.isna(value) or str(value).strip() == '':
                continue  # Skip empty values
            
            # Convert to string and check if it's a valid boolean
            value_str = str(value).strip().upper()
            
            # Only allow TRUE/FALSE values
            if value_str not in ['TRUE', 'FALSE']:
                errors.append(f"Row {idx + 2}: Invalid 'multiple' value '{value}'. Must be TRUE or FALSE.")
        
        return errors
    
    def get_field_keys(self) -> List[str]:
        """
        Get list of all field keys from the configuration
        
        Returns:
            List of field key strings
            
        Example:
            >>> reader = ExcelConfigReader('config.xlsx')
            >>> keys = reader.get_field_keys()
            >>> print(keys)
            ['client_name', 'project_name', 'start_date']
        """
        fields = self.read_fields()
        return [field['key'] for field in fields]
    
    def get_field_by_key(self, key: str) -> Optional[Dict]:
        """
        Get a specific field by its key
        
        Args:
            key: The field key to search for
            
        Returns:
            Field dictionary if found, None otherwise
            
        Example:
            >>> reader = ExcelConfigReader('config.xlsx')
            >>> field = reader.get_field_by_key('client_name')
            >>> print(field['label'])
            'Client Name'
        """
        fields = self.read_fields()
        for field in fields:
            if field['key'] == key:
                return field
        return None
    
    def get_multiple_value_fields(self) -> List[Dict]:
        """
        Get all fields that accept multiple values
        
        Returns:
            List of field dictionaries where multiple=True
            
        Example:
            >>> reader = ExcelConfigReader('config.xlsx')
            >>> multi_fields = reader.get_multiple_value_fields()
            >>> for field in multi_fields:
            ...     print(field['label'])
        """
        fields = self.read_fields()
        return [field for field in fields if field['multiple']]
    
    def get_single_value_fields(self) -> List[Dict]:
        """
        Get all fields that accept only single values
        
        Returns:
            List of field dictionaries where multiple=False
            
        Example:
            >>> reader = ExcelConfigReader('config.xlsx')
            >>> single_fields = reader.get_single_value_fields()
            >>> for field in single_fields:
            ...     print(field['label'])
        """
        fields = self.read_fields()
        return [field for field in fields if not field['multiple']]
    
    def validate_config(self) -> Dict[str, any]:
        """
        Validate the configuration file for common issues
        
        Returns:
            Dictionary with validation results:
            - 'valid': bool
            - 'errors': list of error messages
            - 'warnings': list of warning messages
            
        Example:
            >>> reader = ExcelConfigReader('config.xlsx')
            >>> result = reader.validate_config()
            >>> if not result['valid']:
            ...     print(result['errors'])
        """
        errors = []
        warnings = []
        
        try:
            # Read the raw DataFrame for validation
            df = pd.read_excel(self.file_path)
            
            # Validate multiple column
            multiple_errors = self._validate_multiple_column(df)
            errors.extend(multiple_errors)
            
            # Read fields for other validations
            fields = self.read_fields()
            
            if len(fields) == 0:
                errors.append("No valid fields found in configuration")
            
            # Check for duplicate keys
            keys = [field['key'] for field in fields]
            duplicates = [key for key in keys if keys.count(key) > 1]
            if duplicates:
                errors.append(f"Duplicate field keys found: {', '.join(set(duplicates))}")
            
            # Check for empty labels
            empty_labels = [field['key'] for field in fields if not field['label'].strip()]
            if empty_labels:
                warnings.append(f"Fields with empty labels: {', '.join(empty_labels)}")
            
            # Check for invalid key characters
            import re
            for field in fields:
                if not re.match(r'^[a-zA-Z0-9_]+$', field['key']):
                    errors.append(f"Invalid key format '{field['key']}' - use only letters, numbers, and underscores")
        
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def read_config(file_path: str | Path) -> List[Dict]:
    """
    Convenience function to read template configuration
    
    Args:
        file_path: Path to Excel configuration file
        
    Returns:
        List of field dictionaries
        
    Example:
        >>> from utils.excel_reader import read_config
        >>> fields = read_config('templates/my_template/config.xlsx')
        >>> print(f"Found {len(fields)} fields")
    """
    reader = ExcelConfigReader(file_path)
    return reader.read_fields()


def find_config_file(directory: str | Path) -> Optional[Path]:
    """
    Find the Excel configuration file in a directory
    
    Args:
        directory: Directory to search
        
    Returns:
        Path to config file if found, None otherwise
        
    Example:
        >>> from utils.excel_reader import find_config_file
        >>> config = find_config_file('templates/my_template')
        >>> if config:
        ...     fields = read_config(config)
    """
    directory = Path(directory)
    
    if not directory.exists() or not directory.is_dir():
        return None
    
    # First, try to find the default config filename
    default_config = directory / DEFAULT_CONFIG_EXCEL_FILENAME
    if default_config.exists():
        return default_config
    
    # Otherwise, look for any Excel file
    for pattern in ['*.xlsx', '*.xls']:
        excel_files = list(directory.glob(pattern))
        if excel_files:
            return excel_files[0]
    
    return None


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    # Example: Read a configuration file
    import sys
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = 'templates/example_business/config.xlsx'
    
    try:
        print(f"Reading configuration from: {config_path}")
        reader = ExcelConfigReader(config_path)
        
        # Validate first
        validation = reader.validate_config()
        if not validation['valid']:
            print("\n❌ Validation failed:")
            for error in validation['errors']:
                print(f"  - {error}")
            sys.exit(1)
        
        if validation['warnings']:
            print("\n⚠️  Warnings:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
        # Read fields
        fields = reader.read_fields()
        
        print(f"\n✅ Found {len(fields)} fields:")
        for field in fields:
            multiple_indicator = "📝 (multiple)" if field['multiple'] else "📄 (single)"
            print(f"\n  {multiple_indicator} {field['label']}")
            print(f"    Key: {{{field['key']}}}")
            if field['note']:
                print(f"    Note: {field['note']}")
        
        # Show multiple value fields
        multi_fields = reader.get_multiple_value_fields()
        if multi_fields:
            print(f"\n📝 Fields accepting multiple values: {len(multi_fields)}")
            for field in multi_fields:
                print(f"  - {field['label']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)