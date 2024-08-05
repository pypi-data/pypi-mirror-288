# dbsys

dbsys is a comprehensive Python library for managing database operations using SQLAlchemy and pandas. It provides a high-level interface for common database operations, including reading, writing, creating tables, deleting tables, columns, and rows, as well as advanced features like searching, backup, and restore functionality.

[![PyPI version](https://badge.fury.io/py/dbsys.svg)](https://badge.fury.io/py/dbsys)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/dbsys.svg)](https://pypi.org/project/dbsys/)

## Features

- Easy-to-use interface for database operations
- Support for multiple database types through SQLAlchemy
- Integration with pandas for efficient data handling
- Comprehensive error handling and custom exceptions
- Backup and restore functionality
- Advanced search capabilities
- Deduplication of data

## Installation

You can install the latest version of dbsys using pip:

```bash
pip install --upgrade dbsys
```

For development purposes, you can install the package with extra dependencies:

```bash
pip install dbsys[dev]
```

This will install additional packages useful for development, such as pytest, flake8, and mypy.

## Quick Start

Here's a comprehensive example of how to use dbsys:

```python
from dbsys import DatabaseManager
import pandas as pd

# Initialize the DatabaseManager
db = DatabaseManager("sqlite:///example.db")

# Create a sample DataFrame
data = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie', 'Alice'], 'age': [30, 25, 35, 30]})

# Create a new table and write data
db.use_table("users").create(data)

# Read the table
result = db.use_table("users").read().get_data()
print("Original data:")
print(result)

# Deduplicate the data
db.dedup(subset=['name'], keep='first')
result = db.get_data()
print("\nDeduplicated data:")
print(result)

# Update data in the table
new_data = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie'], 'age': [31, 26, 36]})
db.use_table("users").write(new_data)

# Search for users older than 30
result = db.use_table("users").search({"age": 30}, limit=2).get_data()
print("\nUsers older than 30:")
print(result)

# Delete a specific row
db.use_table("users").delete_row({"name": "Bob"})

# Backup the table
db.use_table("users").backup("users_backup.json")

# Delete the table
db.use_table("users").delete_table()

# Restore the table from backup
db.use_table("users").restore("users_backup.json")

# Verify restored data
result = db.use_table("users").read().get_data()
print("\nRestored data:")
print(result)
```

## API Reference

### DatabaseManager

The main class for interacting with the database.

#### Methods:

- `__init__(database_url: str)`: Initialize the DatabaseManager with a database URL.
- `use_table(table_name: str) -> DatabaseManager`: Set the table to be used for subsequent operations.
- `read() -> DatabaseManager`: Read the entire contents of the currently selected table into memory.
- `write(data: Optional[pd.DataFrame] = None) -> DatabaseManager`: Write data to the currently selected table.
- `create(data: pd.DataFrame) -> DatabaseManager`: Create a new table with the provided data.
- `delete_table() -> DatabaseManager`: Delete the currently selected table.
- `delete_column(column_name: str) -> DatabaseManager`: Delete a specific column from the currently selected table.
- `delete_row(row_identifier: Dict[str, Any]) -> DatabaseManager`: Delete a specific row from the currently selected table.
- `search(conditions: Union[Dict[str, Any], str], limit: Optional[int] = None, case_sensitive: bool = False) -> DatabaseManager`: Search for rows in the current table that match the given conditions.
- `backup(file_path: str, columns: Optional[List[str]] = None) -> DatabaseManager`: Backup the current table or specified columns to a JSON file.
- `restore(file_path: str, mode: str = 'replace') -> DatabaseManager`: Restore data from a JSON file to the current table.
- `get_data() -> Optional[pd.DataFrame]`: Get the current data stored in memory.
- `dedup(subset: Optional[List[str]] = None, keep: str = 'first') -> DatabaseManager`: Deduplicate the current DataFrame based on specified columns.

For detailed usage of each method, please refer to the docstrings in the source code.

## Error Handling

dbsys provides custom exceptions for better error handling:

- `DatabaseError`: Base exception for database operations.
- `TableNotFoundError`: Raised when a specified table is not found in the database.
- `ColumnNotFoun

dError`: Raised when a specified column is not found in the table.
- `InvalidOperationError`: Raised when an invalid operation is attempted.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please [open an issue](https://github.com/lifsys/dbsys/issues) on our GitHub repository.

## About Lifsys, Inc

Lifsys, Inc is an AI company dedicated to developing innovative solutions for data management and analysis. For more information, visit [www.lifsys.com](https://www.lifsys.com).

## Changelog

### 0.3.2
- Prepared for PyPI update
- Reviewed codebase for corrections
- Updated documentation and README
- Incremented version number
- Improved error handling in delete_row method
- Enhanced search functionality with case-sensitive option

### 0.3.1
- Previous update details

### 0.3.0
- Added comprehensive docstrings to all methods
- Updated README with detailed API reference and examples
- Improved error handling and type hints
- Added backup and restore functionality
- Implemented advanced search capabilities
- Added deduplication feature

### 0.2.5
- Prepared for PyPI update
- Reviewed codebase for corrections
- Updated documentation and README
- Incremented version number

(... previous changelog entries ...)
