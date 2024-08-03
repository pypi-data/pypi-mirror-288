"""
A library for managing database operations using SQLAlchemy and pandas.
"""

from typing import Dict, Any, Optional
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy import create_engine, exc as sa_exc
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

class DatabaseError(Exception):
    """Base exception for database operations."""
    pass

class TableNotFoundError(DatabaseError):
    """Raised when a specified table is not found in the database."""
    pass

class ColumnNotFoundError(DatabaseError):
    """Raised when a specified column is not found in the table."""
    pass

# Ensure TableNotFoundError is included in __all__
__all__ = ['DatabaseError', 'TableNotFoundError', 'ColumnNotFoundError', 'manage_db', 'DatabaseManager']

def manage_db(database_url: str, table_name: str, operation: str, data: Optional[pd.DataFrame] = None, column_name: Optional[str] = None, row_identifier: Optional[Dict[str, Any]] = None) -> Optional[pd.DataFrame]:
    """
    Manage database tables using pandas dataframes and SQLAlchemy.

    This function provides a high-level interface for common database operations,
    including reading, writing, creating tables, deleting tables, deleting columns, and deleting rows.

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
            raise ValueError("Invalid operation. Use 'r' for read, 'w' for write, 'c' for create, 'dt' for delete table, 'dc' for delete column, or 'dr' for delete row.")
        
        result = operations[operation]()
        
        try:
            return pd.read_sql_table(table_name, engine) if operation not in ['dt', 'dc', 'dr'] else None
        except ValueError as ve:
            if "Table lifsysdb not found" in str(ve):
                raise TableNotFoundError(f"Table '{table_name}' not found in the database.")
            raise
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")

def delete_table(engine, table_name: str) -> None:
    """Delete a table from the database."""
    try:
        with engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            connection.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(f"Error deleting table {table_name}: {str(e)}")

def delete_row(engine, table_name: str, row_identifier: Dict[str, Any]) -> None:
    """Delete a specific row from a table."""
    try:
        with engine.connect() as connection:
            where_clause = " AND ".join([f"{col} = :{col}" for col in row_identifier.keys()])
            connection.execute(text(f"DELETE FROM {table_name} WHERE {where_clause}"), row_identifier)
            connection.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(f"Error deleting row from table {table_name}: {str(e)}")

def delete_column(engine, table_name: str, column_name: str) -> None:
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

    def read_db(self, table_name: str) -> pd.DataFrame:
        """
        Read the entire table from the database.

        Args:
            table_name (str): Name of the table to read.

        Returns:
            pd.DataFrame: DataFrame containing the table data.

        Raises:
            TableNotFoundError: If the specified table is not found in the database.
            DatabaseError: If there's an error during the database operation.
        """
        try:
            return pd.read_sql_table(table_name, self.engine)
        except ValueError as ve:
            if "Table not found" in str(ve):
                raise TableNotFoundError(f"Table '{table_name}' not found in the database.")
            raise DatabaseError(f"Error reading table: {str(ve)}")
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Database operation failed: {str(e)}")

    def write_db(self, table_name: str, data: pd.DataFrame) -> None:
        """
        Write data to a table in the database, replacing existing data.

        Args:
            table_name (str): Name of the table to write to.
            data (pd.DataFrame): DataFrame containing the data to write.

        Raises:
            ValueError: If the provided data is None or not a DataFrame.
            DatabaseError: If there's an error during the database operation.
        """
        if data is None or not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be provided and must be a pandas DataFrame")
        
        try:
            data.to_sql(table_name, self.engine, if_exists='replace', index=False)
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to write to table: {str(e)}")

    def create_db(self, table_name: str, data: pd.DataFrame) -> None:
        """
        Create a new table in the database.

        Args:
            table_name (str): Name of the new table to create.
            data (pd.DataFrame): DataFrame containing the data for the new table.

        Raises:
            ValueError: If the provided data is None or not a DataFrame.
            DatabaseError: If there's an error during the database operation.
        """
        if data is None or not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be provided and must be a pandas DataFrame")
        
        try:
            data.to_sql(table_name, self.engine, if_exists='fail', index=False)
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to create table: {str(e)}")

    def delete_table(self, table_name: str) -> None:
        """
        Delete a table from the database.

        Args:
            table_name (str): Name of the table to delete.

        Raises:
            DatabaseError: If there's an error during the database operation.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(f"DROP TABLE IF EXISTS {table_name}")
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to delete table: {str(e)}")

    def delete_column(self, table_name: str, column_name: str) -> None:
        """
        Delete a column from a table in the database.

        Args:
            table_name (str): Name of the table.
            column_name (str): Name of the column to delete.

        Raises:
            ValueError: If the column name is not provided.
            DatabaseError: If there's an error during the database operation.
        """
        if not column_name:
            raise ValueError("Column name must be provided for delete column operation")
        
        try:
            with self.engine.connect() as connection:
                connection.execute(f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {column_name}")
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to delete column: {str(e)}")

    def delete_row(self, table_name: str, row_identifier: Dict[str, Any]) -> None:
        """
        Delete a row from a table in the database.

        Args:
            table_name (str): Name of the table.
            row_identifier (Dict[str, Any]): Dictionary containing column:value pair to identify the row to delete.

        Raises:
            ValueError: If the row identifier is not provided.
            DatabaseError: If there's an error during the database operation.
        """
        if not row_identifier:
            raise ValueError("Row identifier must be provided for delete row operation")
        
        try:
            conditions = " AND ".join([f"{key} = '{value}'" for key, value in row_identifier.items()])
            with self.engine.connect() as connection:
                connection.execute(f"DELETE FROM {table_name} WHERE {conditions}")
        except sa_exc.SQLAlchemyError as e:
            raise DatabaseError(f"Failed to delete row: {str(e)}")

# Ensure all exceptions are included in __all__
__all__ = ['DatabaseError', 'TableNotFoundError', 'ColumnNotFoundError', 'DatabaseManager']
