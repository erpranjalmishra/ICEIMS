"""
Utility functions for parsing Excel and CSV files into table data
"""
import pandas as pd
import json
from pathlib import Path


def parse_excel_to_json(file_path, has_header=True, sheet_name=0):
    """
    Parse Excel file to JSON table data
    
    Args:
        file_path: Path to Excel file (.xlsx, .xls)
        has_header: Whether first row contains headers
        sheet_name: Sheet name or index to read (default: first sheet)
    
    Returns:
        dict: Table data in format {'headers': [...], 'rows': [[...]]}
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0 if has_header else None)
        
        # Convert to JSON-friendly format
        if has_header:
            headers = df.columns.tolist()
            rows = df.values.tolist()
        else:
            headers = [f"Column {i+1}" for i in range(len(df.columns))]
            rows = df.values.tolist()
        
        # Clean data (convert NaN to empty string)
        clean_rows = []
        for row in rows:
            clean_row = [str(cell) if pd.notna(cell) else '' for cell in row]
            clean_rows.append(clean_row)
        
        return {
            'headers': headers,
            'rows': clean_rows,
            'total_rows': len(clean_rows),
            'total_columns': len(headers)
        }
    
    except Exception as e:
        raise ValueError(f"Error parsing Excel file: {str(e)}")


def parse_csv_to_json(file_path, has_header=True, delimiter=','):
    """
    Parse CSV file to JSON table data
    
    Args:
        file_path: Path to CSV file
        has_header: Whether first row contains headers
        delimiter: CSV delimiter (default: comma)
    
    Returns:
        dict: Table data in format {'headers': [...], 'rows': [[...]]}
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path, header=0 if has_header else None, delimiter=delimiter)
        
        # Convert to JSON-friendly format
        if has_header:
            headers = df.columns.tolist()
            rows = df.values.tolist()
        else:
            headers = [f"Column {i+1}" for i in range(len(df.columns))]
            rows = df.values.tolist()
        
        # Clean data (convert NaN to empty string)
        clean_rows = []
        for row in rows:
            clean_row = [str(cell) if pd.notna(cell) else '' for cell in row]
            clean_rows.append(clean_row)
        
        return {
            'headers': headers,
            'rows': clean_rows,
            'total_rows': len(clean_rows),
            'total_columns': len(headers)
        }
    
    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")


def parse_table_file(file_path, has_header=True):
    """
    Auto-detect file type and parse to JSON table data
    
    Args:
        file_path: Path to table file (Excel or CSV)
        has_header: Whether first row contains headers
    
    Returns:
        dict: Table data in format {'headers': [...], 'rows': [[...]]}
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    if extension in ['.xlsx', '.xls']:
        return parse_excel_to_json(file_path, has_header)
    elif extension == '.csv':
        return parse_csv_to_json(file_path, has_header)
    else:
        raise ValueError(f"Unsupported file type: {extension}. Only .xlsx, .xls, and .csv are supported.")


def validate_table_data(table_data):
    """
    Validate table data structure
    
    Args:
        table_data: dict with 'headers' and 'rows'
    
    Returns:
        bool: True if valid, raises ValueError if invalid
    """
    if not isinstance(table_data, dict):
        raise ValueError("Table data must be a dictionary")
    
    if 'headers' not in table_data or 'rows' not in table_data:
        raise ValueError("Table data must contain 'headers' and 'rows' keys")
    
    if not isinstance(table_data['headers'], list):
        raise ValueError("Headers must be a list")
    
    if not isinstance(table_data['rows'], list):
        raise ValueError("Rows must be a list")
    
    # Check all rows have same length as headers
    header_count = len(table_data['headers'])
    for i, row in enumerate(table_data['rows']):
        if not isinstance(row, list):
            raise ValueError(f"Row {i} must be a list")
        if len(row) != header_count:
            raise ValueError(f"Row {i} has {len(row)} columns, expected {header_count}")
    
    return True


def get_table_stats(table_data):
    """
    Get statistics about table data
    
    Args:
        table_data: dict with 'headers' and 'rows'
    
    Returns:
        dict: Statistics about the table
    """
    if not table_data:
        return {
            'total_rows': 0,
            'total_columns': 0,
            'has_data': False
        }
    
    return {
        'total_rows': len(table_data.get('rows', [])),
        'total_columns': len(table_data.get('headers', [])),
        'has_data': len(table_data.get('rows', [])) > 0
    }
