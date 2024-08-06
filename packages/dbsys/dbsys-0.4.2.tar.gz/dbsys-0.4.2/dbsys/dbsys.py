import logging
import pandas as pd
import json
from typing import Dict, Any, Optional, Union, List, Callable
from sqlalchemy import create_engine, text, MetaData, Table, Column, exc as sa_exc
from sqlalchemy.engine import Engine
from pathlib import Path
import redis
from urllib.parse import urlparse
import threading
from collections import defaultdict
import time

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

class DatabaseManager:
    """
    A versatile database management class that supports both SQL databases and Redis.

    This class provides a high-level interface for common database operations,
    including reading, writing, creating tables, deleting tables, columns, and rows,
    as well as advanced features like searching, backup, and restore functionality.

    Attributes:
        _connection_string (str): The connection string for the database.
        _table_name (str): The name of the currently selected table.
        _data (pd.DataFrame): The data currently loaded in memory.
        _message (str): The message to be published (for Redis).
        _channel (str): The channel for publishing/subscribing (for Redis).
        _pubsub (redis.client.PubSub): The PubSub object for Redis operations.
        _subscriber_thread (threading.Thread): The thread for handling subscriptions.
        _close_flag (threading.Event): An event flag for closing operations.
        _close_message (str): The message that signals to close the connection.
        _message_history (defaultdict): A dictionary to store message history.
        _base (str): The type of database ('redis' or 'sql').
        _redis_client (redis.Redis): The Redis client (for Redis operations).
        _engine (sqlalchemy.engine.Engine): The SQLAlchemy engine (for SQL operations).

    Args:
        connection_string (str): The connection string for the database.
            For SQL databases, use SQLAlchemy connection strings.
            For Redis, use the format: "redis://[[username]:[password]]@localhost:6379/0"

    Raises:
        ValueError: If an unsupported database type is specified in the connection string.

    Example:
        >>> db = DatabaseManager("sqlite:///example.db")
        >>> db.use_table("users").create(pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]}))
        >>> result = db.read().results()
        >>> print(result)
    """

    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._table_name = None
        self._data = None
        self._message = None
        self._channel = None
        self._pubsub = None
        self._subscriber_thread = None
        self._close_flag = threading.Event()
        self._close_message = None
        self._message_history = defaultdict(list)

        # Infer the database type from the connection string
        parsed_url = urlparse(connection_string)
        if parsed_url.scheme == 'redis':
            self._base = 'redis'
            self._redis_client = redis.Redis.from_url(connection_string)
            self._engine = None
        elif parsed_url.scheme in ['postgresql', 'mysql', 'sqlite']:
            self._base = 'sql'
            self._engine = create_engine(connection_string)
            self._redis_client = None
        else:
            raise ValueError(f"Unsupported database type: {parsed_url.scheme}")

    def table(self, table_name: str) -> 'DatabaseManager':
        """
        Set the table to be used for subsequent operations.

        Args:
            table_name (str): The name of the table to use.

        Returns:
            DatabaseManager: The current instance, allowing for method chaining.

        Example:
            >>> db.use_table("users").read().results()
        """
        self._table_name = table_name
        return self

    def message_handler(self, channel: str, message: str):
        """
        Default message handler for received messages.

        Args:
            channel (str): The channel on which the message was received.
            message (str): The received message.
        """
        logger.info(f"Received message on channel {channel}: {message}")

    def _message_handler_wrapper(self, user_handler: Optional[Callable[[str, str], None]], exiton: str) -> Callable[[dict], None]:
        def wrapper(message):
            if message['type'] == 'message':
                channel = message['channel'].decode('utf-8')
                data = message['data'].decode('utf-8')
                # Store the message in history
                self._message_history[channel].append(data)
                if data == exiton:
                    logger.info(f"Received close message: {exiton}")
                    self._close_flag.set()
                else:
                    if user_handler:
                        user_handler(channel, data)
                    else:
                        self.message_handler(channel, data)
        return wrapper

    def sub_and_store(self, channel: str, handler: Optional[Callable[[str, str], None]] = None, exiton: str = "") -> 'DatabaseManager':
        """
        Subscribe to a channel and store all received messages.

        Args:
            channel (str): The channel to subscribe to.
            handler (Optional[Callable[[str, str], None]]): Optional custom message handler.
            exiton (str): Message that signals to close the connection.

        Returns:
            DatabaseManager: The current instance, allowing for method chaining.
        """
        if self._base != 'redis':
            raise ValueError("sub_and_store method is only available for Redis")

        self._message_history[channel] = []  # Initialize empty list for this channel
        return self.sub(channel, handler, exiton)

    def get_stored_messages(self, channel: str) -> List[str]:
        """
        Retrieve stored messages for a specific channel.

        Args:
            channel (str): The channel to get messages from.

        Returns:
            List[str]: List of stored messages for the channel.
        """
        return self._message_history.get(channel, [])

    def clear_stored_messages(self, channel: Optional[str] = None) -> 'DatabaseManager':
        """
        Clear stored messages for a specific channel or all channels.

        Args:
            channel (Optional[str]): The channel to clear messages from. If None, clear all channels.

        Returns:
            DatabaseManager: The current instance, allowing for method chaining.
        """
        if channel:
            self._message_history[channel] = []
        else:
            self._message_history.clear()
        return self


    def sub(self, channel: str, handler: Optional[Callable[[str, str], None]] = None, exiton: str = "") -> 'DatabaseManager':
        if self._base != 'redis':
            raise ValueError("sub method is only available for Redis")

        if self._pubsub is None:
            self._pubsub = self._redis_client.pubsub()

        wrapped_handler = self._message_handler_wrapper(handler, exiton)
        self._pubsub.subscribe(**{channel: wrapped_handler})
        
        if self._subscriber_thread is None or not self._subscriber_thread.is_alive():
            self._subscriber_thread = threading.Thread(target=self._message_handler_loop, daemon=True)
            self._subscriber_thread.start()

        return self

    def _message_handler_loop(self):
        for message in self._pubsub.listen():
            if self._close_flag.is_set():
                logger.info("Closing message handler loop")
                break

    def pubsub(self, pub_message: str, pub_channel: str, sub_channel: str, 
                               handler: Optional[Callable[[str, str], None]] = None, 
                               exiton: str = "CLOSE", 
                               wait: Optional[int] = None) -> 'DatabaseManager':
        """
        Publish a message, subscribe to a channel, store messages, and wait for a specified time or close message.

        Args:
            pub_message (str): The message to publish.
            pub_channel (str): The channel to publish the message to.
            sub_channel (str): The channel to subscribe to.
            handler (Optional[Callable[[str, str], None]]): Optional custom message handler.
            exiton (str): Message that signals to close the connection.
            wait (Optional[int]): Time in seconds to wait. If None, wait indefinitely.

        Returns:
            DatabaseManager: The current instance, allowing for method chaining.
        """
        if self._base != 'redis':
            raise ValueError("pubsub method is only available for Redis")

        self._close_flag.clear()
        self._close_message = exiton

        # Subscribe to the channel and start storing messages
        self.sub_and_store(sub_channel, handler, exiton)

        # Publish the message
        publish_result = self.pub(pub_message, pub_channel).results()
        logger.info(f"Published message to {publish_result} subscribers")

        if wait is not None:
            logger.info(f"Waiting for {wait} seconds or until '{exiton}' is received.")
            self._close_flag.wait(timeout=wait)
        else:
            logger.info(f"Waiting indefinitely. Send '{exiton}' to close the connection.")
            self._close_flag.wait()

        # Unsubscribe from the channel
        self.unsub(sub_channel)

        return self

    def pub(self, message: str, channel: str) -> 'DatabaseManager':
        if self._base != 'redis':
            raise ValueError("pub method is only available for Redis")
        self._message = message
        self._channel = channel
        return self

    def unsub(self, channel: Optional[str] = None) -> 'DatabaseManager':
        if self._base != 'redis':
            raise ValueError("unsub method is only available for Redis")

        if self._pubsub is not None:
            if channel:
                self._pubsub.unsubscribe(channel)
            else:
                self._pubsub.unsubscribe()

            if not self._pubsub.channels:
                self._subscriber_thread = None

        self._close_flag.clear()
        return self

    def results(self) -> Any:
        if self._base == 'redis':
            if self._message and self._channel:
                return self._redis_client.publish(self._channel, self._message)
            else:
                raise ValueError("Message and channel must be set for Redis pub operation")
        elif self._base == 'sql':
            return self._data
        else:
            raise ValueError("Unsupported database type")

    def read(self) -> 'DatabaseManager':
        """
        Read the entire contents of the currently selected table into memory.

        This method reads all data from the current table and stores it in the
        _data attribute as a pandas DataFrame.

        Returns:
            DatabaseManager: The current instance, allowing for method chaining.

        Raises:
            ValueError: If no table has been selected.
            TableNotFoundError: If the specified table doesn't exist in the database.
            DatabaseError: For any other database-related errors.
            NotImplementedError: If called on a Redis database.

        Example:
            >>> db.use_table("users").read().results()
        """
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")
            try:
                self._data = pd.read_sql_table(self._table_name, self._engine)
            except ValueError as ve:
                if "Table not found" in str(ve):
                    raise TableNotFoundError(f"Table '{self._table_name}' not found in the database.")
                raise DatabaseError(f"Error reading table: {str(ve)}")
            except sa_exc.SQLAlchemyError as e:
                raise DatabaseError(f"Database operation failed: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Read operation not implemented for Redis")
        return self

    def dedup(self, subset: Optional[List[str]] = None, keep: str = 'first') -> 'DatabaseManager':
        if self._data is None:
            raise ValueError("No data to deduplicate. Use .read() first.")
        
        self._data = self._data.drop_duplicates(subset=subset, keep=keep)
        return self

    def write(self, data: Optional[pd.DataFrame] = None) -> 'DatabaseManager':
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")
            if data is None and self._data is None:
                raise ValueError("No data to write. Provide data or use .read() first.")
            try:
                (data if data is not None else self._data).to_sql(self._table_name, self._engine, if_exists='replace', index=False)
            except sa_exc.SQLAlchemyError as e:
                raise DatabaseError(f"Failed to write to table: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Write operation not implemented for Redis")
        return self

    def create(self, data: pd.DataFrame) -> 'DatabaseManager':
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")
            try:
                data.to_sql(self._table_name, self._engine, if_exists='fail', index=False)
                self._data = data
            except sa_exc.SQLAlchemyError as e:
                raise DatabaseError(f"Failed to create table: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Create operation not implemented for Redis")
        return self

    def delete_table(self) -> 'DatabaseManager':
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")
            try:
                with self._engine.connect() as connection:
                    connection.execute(text(f"DROP TABLE IF EXISTS {self._table_name}"))
                self._data = None
            except sa_exc.SQLAlchemyError as e:
                raise DatabaseError(f"Failed to delete table: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Delete table operation not implemented for Redis")
        return self

    def delete_column(self, column_name: str) -> 'DatabaseManager':
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")
            if not column_name:
                raise ValueError("Column name must be provided for delete column operation")
            try:
                with self._engine.connect() as connection:
                    connection.execute(text(f"ALTER TABLE {self._table_name} DROP COLUMN IF EXISTS {column_name}"))
                if self._data is not None and column_name in self._data.columns:
                    self._data = self._data.drop(column_name, axis=1)
            except sa_exc.SQLAlchemyError as e:
                raise DatabaseError(f"Failed to delete column: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Delete column operation not implemented for Redis")
        return self

    def delete_row(self, row_identifier: Dict[str, Any]) -> 'DatabaseManager':
        if self._base == 'sql':
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
                
                with self._engine.connect() as connection:
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
        elif self._base == 'redis':
            raise NotImplementedError("Delete row operation not implemented for Redis")
        return self

    def search(self, conditions: Union[Dict[str, Any], str], limit: Optional[int] = None, case_sensitive: bool = False) -> 'DatabaseManager':
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")
            
            try:
                metadata = MetaData()
                table = Table(self._table_name, metadata, autoload_with=self._engine)
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
                
                with self._engine.connect() as connection:
                    result = connection.execute(text(query), search_conditions)
                    self._data = pd.DataFrame(result.fetchall(), columns=result.keys())
                return self
            except sa_exc.SQLAlchemyError as e:
                raise DatabaseError(f"Search operation failed: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Search operation not implemented for Redis")
        return self

    def backup(self, file_path: str, columns: Optional[List[str]] = None) -> 'DatabaseManager':
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")

            try:
                if self._data is None:
                    self.read()

                if columns:
                    missing_columns = set(columns) - set(self._data.columns)
                    if missing_columns:
                        raise ValueError(f"Columns not found in table: {', '.join(missing_columns)}")
                    data_to_backup = self._data[columns]
                else:
                    data_to_backup = self._data

                json_data = data_to_backup.to_json(orient='records', date_format='iso')

                Path(file_path).parent.mkdir(parents=True, exist_ok=True)

                with open(file_path, 'w') as f:
                    f.write(json_data)

                logger.info(f"{self._table_name}: Backup created successfully at {file_path}")
                return self

            except (sa_exc.SQLAlchemyError, IOError) as e:
                raise DatabaseError(f"Failed to create backup: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Backup operation not implemented for Redis")
        return self

    def restore(self, file_path: str, mode: str = 'replace') -> 'DatabaseManager':
        if self._base == 'sql':
            if not self._table_name:
                raise ValueError("Table name not set. Use .use_table() first.")

            if not Path(file_path).exists():
                raise ValueError(f"File not found: {file_path}")

            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)

                df = pd.DataFrame(json_data)

                if mode == 'replace':
                    df.to_sql(self._table_name, self._engine, if_exists='replace', index=False)
                elif mode == 'append':
                    df.to_sql(self._table_name, self._engine, if_exists='append', index=False)
                elif mode == 'upsert':
                    metadata = MetaData()
                    table = Table(self._table_name, metadata, autoload_with=self._engine)
                    pk_columns = [key.name for key in table.primary_key]

                    if not pk_columns:
                        raise ValueError("Cannot perform upsert without primary key")

                    for _, row in df.iterrows():
                        query = f"""
                        INSERT INTO {self._table_name} ({', '.join(df.columns)})
                        VALUES ({', '.join([':' + col for col in df.columns])})
                        ON CONFLICT ({', '.join(pk_columns)})
                        DO UPDATE SET {', '.join([f"{col} = excluded.{col}" for col in df.columns if col not in pk_columns])}
                        """
                        with self._engine.connect() as conn:
                            conn.execute(text(query), row.to_dict())
                            conn.commit()
                else:
                    raise ValueError("Invalid mode. Use 'replace', 'append', or 'upsert'.")

                self._data = df

                logger.info(f"Data restored successfully from {file_path}")
                return self

            except (sa_exc.SQLAlchemyError, IOError, json.JSONDecodeError) as e:
                raise DatabaseError(f"Failed to restore from backup: {str(e)}")
        elif self._base == 'redis':
            raise NotImplementedError("Restore operation not implemented for Redis")
        return self

    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Get the current data stored in the DatabaseManager.

        Returns:
            Optional[pd.DataFrame]: The current data, or None if no data has been loaded or queried.
        """
        return self._data

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> 'DatabaseManager':
        """
        Execute a custom SQL query.

        Args:
            query (str): The SQL query to execute.
            params (Optional[Dict[str, Any]]): Parameters to be used in the query.

        Returns:
            DatabaseManager: The current instance, allowing for method chaining.

        Raises:
            ValueError: If the base is not set to a SQL database.
            DatabaseError: If there's an error during the database operation.
        """
        if self._base == 'sql':
            try:
                with self._engine.connect() as connection:
                    result = connection.execute(text(query), params or {})
                    if query.strip().upper().startswith('SELECT'):
                        self._data = pd.DataFrame(result.fetchall(), columns=result.keys())
                    else:
                        connection.commit()
                return self
            except sa_exc.SQLAlchemyError as e:
                raise DatabaseError(f"Query execution failed: {str(e)}")
        else:
            raise ValueError("execute_query method is only available for SQL databases")

    def __str__(self) -> str:
        base_type = self._base
        table_name = self._table_name or "Not set"
        data_shape = self._data.shape if self._data is not None else "No data loaded"
        redis_info = f", subscribed channels: {list(self._pubsub.channels) if self._pubsub else None}" if self._base == 'redis' else ""
        return f"DatabaseManager(base={base_type}, table={table_name}, data_shape={data_shape}{redis_info})"
