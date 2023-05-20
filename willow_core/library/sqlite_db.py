
import logging.config
import sqlite3
from sqlite3 import Connection, Cursor, Error, Row
from typing import Any
from .time_handler import TimeHandler
from .db_types import DeleteDbItemResponse


class SqlLiteDb:
    def __init__(self, logging_object: Any, db_location: str):
        self._logger: logging.Logger = logging_object.getLogger(type(self).__name__)
        self._logger.setLevel(logging.INFO)
        self._db_location: str = db_location

    def _check_table_exists(self, db_cursor: Cursor, table_name: str) -> bool:
        try:
            table_list = db_cursor.execute(
                "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name=?;", [table_name]
            ).fetchall()
            if table_list:
                return True
            return False
        except Error as error:
            self._logger.info(f'Error check if tables exist in DB', error)

    @staticmethod
    def set_row_factory(conn: Connection) -> None:
        conn.row_factory = sqlite3.Row

    @staticmethod
    def _get_time() -> str:
        return TimeHandler.get_standard_utc_time()

    def _db_connect(self) -> Connection:
        try:
            conn: Connection = sqlite3.connect(self._db_location)
            self._logger.debug(f'Opened DB "{self._db_location}" successfully')
            return conn
        except Error as error:
            self._logger.info(f'DB connection failed', error)

    def _db_close(self, live_db_connection: Connection) -> None:
        try:
            live_db_connection.commit()
            live_db_connection.close()
            self._logger.debug(f'Saved and Closed DB "{self._db_location}" successfully')
        except Error as error:
            self._logger.info(f'DB close failed', error)

    def _check_db_state(self, table_names: list[str]) -> bool:
        try:
            conn: Connection = self._db_connect()
            db_cursor: Cursor = conn.cursor()
            db_schema_good: bool = True
            for table_name in table_names:
                db_schema_good = db_schema_good and self._check_table_exists(db_cursor, table_name)
            self._db_close(conn)
            return db_schema_good
        except Error as error:
            self._logger.info(f'Checking DB state failed', error)

    def _query_for_db_rows(self, sqlite_query: str) -> list[Row]:
        try:
            conn: Connection = self._db_connect()
            self.set_row_factory(conn)
            db_cursor: Cursor = conn.cursor()
            db_records_result: list[Row] = db_cursor.execute(sqlite_query).fetchall()
            self._logger.info(f'Retrieved tags from Arcadia_DB successfully')
            self._db_close(conn)
            return db_records_result
        except Error as error:
            self._logger.error(f'Error occurred getting tags from DB: {str(error)}')

    def delete_record(self, data_key: str, key_column: str, table_name: str) -> DeleteDbItemResponse:
        response: DeleteDbItemResponse = {
            'deleted_item': False,
            'reason': 'error',
            'data': []
        }
        try:
            conn: Connection = self._db_connect()
            db_cursor: Cursor = conn.cursor()
            db_cursor.execute(f'DELETE FROM {table_name} WHERE {key_column} = ?;', [data_key])
            self._db_close(conn)
            self._logger.info(f'Deleted record successfully for: {data_key}')
            response['deleted_item'] = True
            response['reason'] = 'item_deleted'
        except Error as error:
            self._logger.error(f'Error occurred deleting record on DB in {table_name} at {data_key}: {str(error)}')
        except Exception as exception:
            self._logger.error(f'Exception was thrown deleting record: {str(exception)}')
            raise
        finally:
            return response
