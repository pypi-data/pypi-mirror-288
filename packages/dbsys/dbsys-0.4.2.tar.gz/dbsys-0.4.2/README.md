# dbsys

dbsys is a comprehensive Python library for managing database operations using SQLAlchemy and pandas. It provides a high-level interface for common database operations, including reading, writing, creating tables, deleting tables, columns, and rows, as well as advanced features like searching, backup, restore functionality, and Redis support.

[![PyPI version](https://badge.fury.io/py/dbsys.svg)](https://badge.fury.io/py/dbsys)
[![Python Versions](https://img.shields.io/pypi/pyversions/dbsys.svg)](https://pypi.org/project/dbsys/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/dbsys.svg)](https://pypi.org/project/dbsys/)

## Features

- Easy-to-use interface for database operations
- Support for multiple database types through SQLAlchemy
- Redis support for pub/sub operations and key-value storage
- Integration with pandas for efficient data handling
- Comprehensive error handling and custom exceptions
- Backup and restore functionality
- Advanced search capabilities
- Deduplication of data
- Custom SQL query execution

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

Here's a comprehensive example of how to use dbsys with SQL databases:

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
result = db.use_table("users").read().results()
print("Original data:")
print(result)

# Deduplicate the data
db.dedup(subset=['name'], keep='first')
result = db.results()
print("\nDeduplicated data:")
print(result)

# Update data in the table
new_data = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie'], 'age': [31, 26, 36]})
db.use_table("users").write(new_data)

# Search for users older than 30
result = db.use_table("users").search({"age": 30}, limit=2).results()
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
result = db.use_table("users").read().results()
print("\nRestored data:")
print(result)

# Execute a custom SQL query
result = db.execute_query("SELECT * FROM users WHERE age > 30").results()
print("\nCustom query result:")
print(result)
```

Example of using dbsys with Redis:

```python
from dbsys import DatabaseManager
import time

# Initialize the DatabaseManager with Redis
db = DatabaseManager("redis://localhost:6379/0")

# Publish a message
db.pub("Hello, Redis!", "test_channel")

# Subscribe to a channel and process messages
def message_handler(channel, message):
    print(f"Received on {channel}: {message}")

db.sub("test_channel", handler=message_handler)

# Publish and subscribe in one operation
db.pubsub("Test message", "pub_channel", "sub_channel", handler=message_handler, wait=5)

# Get stored messages
messages = db.get_stored_messages("sub_channel")
print("Stored messages:", messages)

# Clear stored messages
db.clear_stored_messages()
```

## API Reference

### DatabaseManager

The main class for interacting with the database. It supports both SQL databases and Redis.

#### Constructor

```python
DatabaseManager(connection_string: str)
```

Initialize the DatabaseManager with a database URL.

- `connection_string`: The connection string for the database.
  - For SQL databases, use SQLAlchemy connection strings.
  - For Redis, use the format: "redis://[[username]:[password]]@localhost:6379/0"

#### Methods

- `use_table(table_name: str) -> DatabaseManager`
- `read() -> DatabaseManager`
- `write(data: Optional[pd.DataFrame] = None) -> DatabaseManager`
- `create(data: pd.DataFrame) -> DatabaseManager`
- `delete_table() -> DatabaseManager`
- `delete_column(column_name: str) -> DatabaseManager`
- `delete_row(row_identifier: Dict[str, Any]) -> DatabaseManager`
- `search(conditions: Union[Dict[str, Any], str], limit: Optional[int] = None, case_sensitive: bool = False) -> DatabaseManager`
- `backup(file_path: str, columns: Optional[List[str]] = None) -> DatabaseManager`
- `restore(file_path: str, mode: str = 'replace') -> DatabaseManager`
- `results() -> Optional[pd.DataFrame]`
- `dedup(subset: Optional[List[str]] = None, keep: str = 'first') -> DatabaseManager`
- `execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> DatabaseManager`
- `pub(message: str, channel: str) -> DatabaseManager`
- `sub(channel: str, handler: Optional[Callable[[str, str], None]] = None, exiton: str = "") -> DatabaseManager`
- `pubsub(pub_message: str, pub_channel: str, sub_channel: str, handler: Optional[Callable[[str, str], None]] = None, exiton: str = "CLOSE", wait: Optional[int] = None) -> DatabaseManager`
- `unsub(channel: Optional[str] = None) -> DatabaseManager`
- `get_stored_messages(channel: str) -> List[str]`
- `clear_stored_messages(channel: Optional[str] = None) -> DatabaseManager`

For detailed usage of each method, including all parameters and return values, please refer to the docstrings in the source code.

## Error Handling

dbsys provides custom exceptions for better error handling:

- `DatabaseError`: Base exception for database operations.
- `TableNotFoundError`: Raised when a specified table is not found in the database.
- `ColumnNotFoundError`: Raised when a specified column is not found in the table.
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

### 0.4.2
- Prepared for PyPI update
- Reviewed codebase for corrections
- Updated documentation and README
- Incremented version number

### 0.4.1
- Removed deprecated `manage_db` method
- Updated documentation and README
- Minor code improvements and bug fixes

### 0.4.0
- Prepared for PyPI update
- Reviewed codebase for corrections
- Updated documentation and README
- Incremented version number
- Improved error handling in delete_row method
- Enhanced search functionality with case-sensitive option

(... previous changelog entries ...)
