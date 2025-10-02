EXCEL_COLUMNS = {
    'LABEL': 'label',      # Display name shown to user in form
    'KEY': 'key',          # Placeholder key used in Word documents
    'MULTIPLE': 'multiple', # Whether field accepts multiple values (TRUE/FALSE)
    'TYPE': 'type',        # Alternative column name for multiple (TRUE/FALSE)
    'NOTE': 'note',        # Help text/instructions for the user
}

EXCEL_REQUIRED_COLUMNS = [
    EXCEL_COLUMNS['LABEL'],
    EXCEL_COLUMNS['KEY']
]

# Optional columns that can be used for multiple values
EXCEL_MULTIPLE_COLUMNS = [
    EXCEL_COLUMNS['MULTIPLE'],
    EXCEL_COLUMNS['TYPE']
]

EXCEL_BOOLEAN_MAPPING = {
    'TRUE': True,
    'FALSE': False
}

DEFAULT_CONFIG_EXCEL_FILENAME = 'config.xlsx'