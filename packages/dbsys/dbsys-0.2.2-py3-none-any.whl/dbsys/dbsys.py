"""
A library for managing database operations using SQLAlchemy and pandas.
"""

from typing import Dict, Any, Optional, Union, List
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column
from sqlalchemy import create_engine, exc as sa_exc
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy.engine import Engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base exception for database operations."""
    pass

class TableNotFoundError(DatabaseError):
    """Raised when a specified table is not found in the database."""
    pass

class ColumnNotFoundError(DatabaseError):
    """Raised when a specified column is not found in the table."""
    pass

class InvalidOperationError(DatabaseError):
    """Raised when an invalid operation is attempted."""
    pass

# Ensure all classes and functions are included in __all__
__all__ = ['DatabaseError', 'TableNotFoundError', 'ColumnNotFoundError', 'InvalidOperationError', 'manage_db', 'DatabaseManager']

def manage_db(database_url: str, table_name: str, operation: str, data: Optional[pd.DataFrame] = None, column_name: Optional[str] = None, row_identifier: Optional[Dict[str, Any]] = None) -> Optional[pd.DataFrame]:
    """
    Manage database tables using pandas dataframes and SQLAlchemy.

    Args:
        database_url (str): URL of the database to connect to.
        table_name (str): Name of the table to operate on.
        operation (str): Operation to perform ('r', 'w', 'c', 'dt', 'dc', 'dr').
        data (Optional[pd.DataFrame]): DataFrame to write or create table with.
        column_name (Optional[str]): Name of the column to delete.
        row_identifier (Optional[Dict[str, Any]]): Dictionary to identify the row to delete.

    Returns:
        Optional[pd.DataFrame]: DataFrame representing the current state of the table
        after the operation, or None for delete operations.

    Raises:
        InvalidOperationError: If an invalid operation is specified.
        ValueError: If required parameters are missing for certain operations.
        DatabaseError: If there's an error during database operations.
        TableNotFoundError: If the specified table is not found in the database.
        ColumnNotFoundError: If the specified column is not found in the table.
    """
    """
    Manage database tables using pandas dataframes and SQLAlchemy.

    This function provides a high-level interface for common database operations,
    including reading, writing, creating tables, deleting tables, deleting columns, and deleting rows.

    Example:
    DatabaseManager(get_api("lifsysdb", "lifsysdb")).read_db("contract_requirements").to_dict(orient='records')

    Args:
        database_url (str): URL of the database to connect to.
        table_name (str): Name of the table to operate on.
        operation (str): Operation to perform. Valid options are:
            - 'r' or 'read': Read the entire table.
            - 'w' or 'write': Write data to the table, replacing existing data.
            - 'c' or 'create': Create a new table with the provided data.
            - 'dt' or 'delete table': Delete the entire table.
            - 'dc' or 'delete column': Delete a specific column from the table.
            - 'dr' or 'delete row': Delete a specific row from the table.
        data (Optional[pd.DataFrame]): DataFrame to write or create table with.
            Required for 'w' and 'c' operations. Defaults to None.
        column_name (Optional[str]): Name of the column to delete.
            Required for 'dc' operation. Defaults to None.
        row_identifier (Optional[Dict[str, Any]]): Dictionary containing column:value pair to identify the row to delete.
            Required for 'dr' operation. Defaults to None.

    Returns:
        Optional[pd.DataFrame]: DataFrame representing the current state of the table
        after the operation, or None for delete operations.

    Raises:
        ValueError: If an invalid operation is specified or if required parameters
                    are missing for certain operations.
        DatabaseError: If there's an error during database operations.
        TableNotFoundError: If the specified table is not found in the database.
        ColumnNotFoundError: If the specified column is not found in the table.
    """
    try:
        engine = create_engine(database_url)
        
        operations = {
            'r': lambda: pd.read_sql_table(table_name, engine),
            'w': lambda: data.to_sql(table_name, engine, if_exists='replace', index=False) if data is not None else ValueError("Data must be provided for write operation"),
            'c': lambda: data.to_sql(table_name, engine, if_exists='fail', index=False) if data is not None else ValueError("Data must be provided for create operation"),
            'dt': lambda: delete_table(engine, table_name),
            'dc': lambda: delete_column(engine, table_name, column_name) if column_name else ValueError("Column name must be provided for delete column operation"),
            'dr': lambda: delete_row(engine, table_name, row_identifier) if row_identifier else ValueError("Row identifier must be provided for delete row operation")
        }
        
        operation = operation.lower()
        if operation not in operations:
            raise InvalidOperationError("Invalid operation. Use 'r' for read, 'w' for write, 'c' for create, 'dt' for delete table, 'dc' for delete column, or 'dr' for delete row.")
        
        result = operations[operation]()
        
        if isinstance(result, ValueError):
            raise result
        
        if operation not in ['dt', 'dc', 'dr']:
            try:
                return pd.read_sql_table(table_name, engine)
            except ValueError as ve:
                if "Table not found" in str(ve):
                    raise TableNotFoundError(f"Table '{table_name}' not found in the database.")
                raise
        return None
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")

def delete_table(engine: Engine, table_name: str) -> None:
    """Delete a table from the database."""
    try:
        with engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            connection.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(f"Error deleting table {table_name}: {str(e)}")

def delete_row(engine: Engine, table_name: str, row_identifier: Dict[str, Any]) -> None:
    """Delete a specific row from a table."""
    try:
        with engine.connect() as connection:
            where_clause = " AND ".join([f"{col} = :{col}" for col in row_identifier.keys()])
            connection.execute(text(f"DELETE FROM {table_name} WHERE {where_clause}"), row_identifier)
            connection.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(f"Error deleting row from table {table_name}: {str(e)}")

def delete_column(engine: Engine, table_name: str, column_name: str) -> None:
    """Delete a specific column from a table."""
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        table = Table(table_name, metadata, autoload_with=engine)
        
        if column_name not in table.columns:
            raise ColumnNotFoundError(f"Column {column_name} does not exist in table {table_name}")
        
        with engine.connect() as connection:
            connection.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {column_name}"))
            connection.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(f"Error deleting column {column_name} from table {table_name}: {str(e)}")


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self._table_name = None
        self._data = None

    def use_table(self, table_name: str) -> 'DatabaseManager':
        self._table_name = table_name
        return self

    def read(self) -> 'DatabaseManager':
        if not self._table_name:
            raise ValueError("Table name not set. Use .use_table() first.")
        try:
            self._data = pd.read_sql_table(self._table_name, self.engine)
        except ValueError as ve:
            if "Table not found" in str(ve):
                raise TableNotFoundError(f"Table '{self._table_name}' not found in the database.")
            raise DatabaseError(f"Error reading table: {str(ve)}")
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Database operation failed: {str(e)}")
        return self

    def dedup(self, subset: Optional[List[str]] = None, keep: str = 'first') -> 'DatabaseManager':
        """
        Deduplicate the current DataFrame based on specified columns or all columns if not specified.
        
        Args:
        subset (List[str] or None): List of column names to consider for deduplication. If None, use all columns.
        keep (str): Which duplicates to keep {'first', 'last', False}. Default is 'first'.
        
        Returns:
        DatabaseManager: The current instance, allowing for method chaining.
        """
        if self._data is None:
            raise ValueError("No data to deduplicate. Use .read() first.")
        
        self._data = self._data.drop_duplicates(subset=subset, keep=keep)
        return self

    def write(self, data: Optional[pd.DataFrame] = None) -> 'DatabaseManager':
        if not self._table_name:
            raise ValueError("Table name not set. Use .use_table() first.")
        if data is None and self._data is None:
            raise ValueError("No data to write. Provide data or use .read() first.")
        try:
            (data if data is not None else self._data).to_sql(self._table_name, self.engine, if_exists='replace', index=False)
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to write to table: {str(e)}")
        return self

    def create(self, data: pd.DataFrame) -> 'DatabaseManager':
        if not self._table_name:
            raise ValueError("Table name not set. Use .use_table() first.")
        try:
            data.to_sql(self._table_name, self.engine, if_exists='fail', index=False)
            self._data = data
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to create table: {str(e)}")
        return self

    def delete_table(self) -> 'DatabaseManager':
        if not self._table_name:
            raise ValueError("Table name not set. Use .use_table() first.")
        try:
            with self.engine.connect() as connection:
                connection.execute(text(f"DROP TABLE IF EXISTS {self._table_name}"))
            self._data = None
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to delete table: {str(e)}")
        return self

    def delete_column(self, column_name: str) -> 'DatabaseManager':
        if not self._table_name:
            raise ValueError("Table name not set. Use .use_table() first.")
        if not column_name:
            raise ValueError("Column name must be provided for delete column operation")
        try:
            with self.engine.connect() as connection:
                connection.execute(text(f"ALTER TABLE {self._table_name} DROP COLUMN IF EXISTS {column_name}"))
            if self._data is not None and column_name in self._data.columns:
                self._data = self._data.drop(column_name, axis=1)
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to delete column: {str(e)}")
        return self

    def delete_row(self, row_identifier: Dict[str, Any]) -> 'DatabaseManager':
        if not self._table_name:
            raise ValueError("Table name not set. Use .use_table() first.")
        if not row_identifier:
            raise ValueError("Row identifier must be provided for delete row operation")
        
        logger.debug(f"Attempting to delete row with identifier: {row_identifier}")
        
        try:
            conditions = []
            for key, value in row_identifier.items():
                if value is None:
                    conditions.append(f'"{key}" IS NULL')
                else:
                    conditions.append(f'"{key}" = :{key}')
            
            where_clause = " AND ".join(conditions)
            query = f"DELETE FROM {self._table_name} WHERE {where_clause}"
            
            logger.debug(f"Executing SQL query: {query}")
            logger.debug(f"With parameters: {row_identifier}")
            
            with self.engine.connect() as connection:
                result = connection.execute(
                    text(query),
                    {k: v for k, v in row_identifier.items() if v is not None}
                )
                connection.commit()
                rows_deleted = result.rowcount
                logger.info(f"{rows_deleted} row(s) deleted.")
            
            if self._data is not None:
                logger.debug("Updating in-memory data")
                original_length = len(self._data)
                mask = pd.Series(True, index=self._data.index)
                for col, val in row_identifier.items():
                    if val is None:
                        mask &= self._data[col].isnull()
                    else:
                        mask &= (self._data[col] != val)
                self._data = self._data[mask]
                new_length = len(self._data)
                logger.debug(f"In-memory data rows reduced from {original_length} to {new_length}")
            
            return self
        except sa_exc.SQLAlchemyError as e:
            logger.error(f"Failed to delete row: {str(e)}")
            raise DatabaseError(f"Failed to delete row: {str(e)}")
        

    def search(self, conditions: Union[Dict[str, Any], str], limit: Optional[int] = None, case_sensitive: bool = False) -> 'DatabaseManager':
        """
        Search for rows in the current table that contain the given conditions.

        Args:
            conditions (Union[Dict[str, Any], str]): 
                If dict: column-value pairs to search for.
                If str: search term to look for in any column.
            limit (Optional[int]): Maximum number of rows to return. If None, returns all matching rows.
            case_sensitive (bool): If True, perform a case-sensitive search. Default is False.

        Returns:
            DatabaseManager: The current instance, allowing for method chaining.

        Raises:
            ValueError: If table name is not set or if conditions are invalid.
            DatabaseError: If there's an error during the database operation.
        """
        if not self._table_name:
            raise ValueError("Table name not set. Use .use_table() first.")
        
        try:
            metadata = MetaData()
            table = Table(self._table_name, metadata, autoload_with=self.engine)
            columns = table.columns.keys()

            if isinstance(conditions, dict):
                if not conditions:
                    raise ValueError("Search conditions dictionary cannot be empty")
                where_clauses = []
                search_conditions = {}
                for i, (col, val) in enumerate(conditions.items()):
                    if val is None:
                        raise ValueError(f"Search value for column '{col}' cannot be None")
                    param_name = f"param_{i}"
                    if case_sensitive:
                        where_clauses.append(f'"{col}" LIKE :{param_name}')
                    else:
                        where_clauses.append(f'LOWER("{col}"::text) LIKE LOWER(:{param_name})')
                    search_conditions[param_name] = f"%{val}%"
                where_clause = " AND ".join(where_clauses)
            elif isinstance(conditions, str):
                if not conditions.strip():
                    raise ValueError("Search string cannot be empty")
                where_clauses = []
                search_conditions = {"search_term": f"%{conditions}%"}
                for col in columns:
                    if case_sensitive:
                        where_clauses.append(f'"{col}"::text LIKE :search_term')
                    else:
                        where_clauses.append(f'LOWER("{col}"::text) LIKE LOWER(:search_term)')
                where_clause = " OR ".join(where_clauses)
            else:
                raise ValueError("conditions must be either a non-empty dictionary or a non-empty string")

            query = f"SELECT * FROM {self._table_name} WHERE {where_clause}"
            if limit is not None:
                query += f" LIMIT {limit}"
            
            with self.engine.connect() as connection:
                result = connection.execute(text(query), search_conditions)
                self._data = pd.DataFrame(result.fetchall(), columns=result.keys())
            return self
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Search operation failed: {str(e)}")

    def get_data(self) -> Optional[pd.DataFrame]:
        return self._data
    
    
