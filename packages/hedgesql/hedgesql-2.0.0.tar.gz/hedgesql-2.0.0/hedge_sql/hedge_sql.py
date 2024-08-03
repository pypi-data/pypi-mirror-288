import aiosqlite
import sqlite3
from typing import Dict, Union, Tuple, List, Optional


class DataTypes:
    class OrderBy:
        @staticmethod
        def desc(column: str) -> str:
            return f'{column} DESC'

        @staticmethod
        def asc(column: str) -> str:
            return f'{column} ASC'

    class Limit:
        @staticmethod
        def offset(count: int, offset: int) -> str:
            return f'{count} OFFSET {offset}'

    class Fetch:
        FETCHONE = 'fetchone'
        FETCHALL = 'fetchall'

    class Collation:
        BINARY = 'BINARY'
        NOCASE = 'NOCASE'
        RTRIM = 'RTRIM'
        UTF16 = 'UTF16'
        UTF16CI = 'UTF16CI'

    class ColumnTypes:
        @staticmethod
        def integer(not_null: bool = False,
                    primary_key: bool = False,
                    autoincrement: bool = False,
                    unique: bool = False,
                    default: Union[str, int, float] = None,
                    check: Union[str, int, float] = None,
                    collation: Union['DataTypes.Collation', str] = None) -> str:
            type_str = 'INTEGER'
            if primary_key:
                type_str += ' PRIMARY KEY'
                if autoincrement:
                    type_str += ' AUTOINCREMENT'
            if not_null:
                type_str += ' NOT NULL'
            if unique:
                type_str += ' UNIQUE'
            if default is not None:
                type_str += f" DEFAULT {default}"
            if check is not None:
                type_str += f" CHECK ({check})"
            if collation is not None:
                type_str += f" COLLATE {collation}"
            return type_str

        @staticmethod
        def real(not_null: bool = False,
                 primary_key: bool = False,
                 unique: bool = False,
                 default: Union[str, int, float] = None,
                 check: Union[str, int, float] = None,
                 collation: Union['DataTypes.Collation', str] = None) -> str:
            type_str = 'REAL'
            if primary_key:
                type_str += ' PRIMARY KEY'
            if not_null:
                type_str += ' NOT NULL'
            if unique:
                type_str += ' UNIQUE'
            if default is not None:
                type_str += f" DEFAULT {default}"
            if check is not None:
                type_str += f" CHECK ({check})"
            if collation is not None:
                type_str += f" COLLATE {collation}"
            return type_str

        @staticmethod
        def text(not_null: bool = False,
                 primary_key: bool = False,
                 unique: bool = False,
                 default: Union[str, int, float] = None,
                 check: Union[str, int, float] = None,
                 collation: Union['DataTypes.Collation', str] = None) -> str:
            type_str = 'TEXT'
            if primary_key:
                type_str += ' PRIMARY KEY'
            if not_null:
                type_str += ' NOT NULL'
            if unique:
                type_str += ' UNIQUE'
            if default is not None:
                type_str += f" DEFAULT {default}"
            if check is not None:
                type_str += f" CHECK ({check})"
            if collation is not None:
                type_str += f" COLLATE {collation}"
            return type_str

        @staticmethod
        def blob(not_null: bool = False,
                 primary_key: bool = False,
                 unique: bool = False,
                 default: Union[str, int, float] = None,
                 check: Union[str, int, float] = None,
                 collation: Union['DataTypes.Collation', str] = None) -> str:
            type_str = 'BLOB'
            if primary_key:
                type_str += ' PRIMARY KEY'
            if not_null:
                type_str += ' NOT NULL'
            if unique:
                type_str += ' UNIQUE'
            if default is not None:
                type_str += f" DEFAULT {default}"
            if check is not None:
                type_str += f" CHECK ({check})"
            if collation is not None:
                type_str += f" COLLATE {collation}"
            return type_str

        @staticmethod
        def numeric(not_null: bool = False,
                    primary_key: bool = False,
                    unique: bool = False,
                    default: Union[str, int, float] = None,
                    check: Union[str, int, float] = None,
                    collation: Union['DataTypes.Collation', str] = None) -> str:
            type_str = 'NUMERIC'
            if primary_key:
                type_str += ' PRIMARY KEY'
            if not_null:
                type_str += ' NOT NULL'
            if unique:
                type_str += ' UNIQUE'
            if default is not None:
                type_str += f" DEFAULT {default}"
            if check is not None:
                type_str += f" CHECK ({check})"
            if collation is not None:
                type_str += f" COLLATE {collation}"
            return type_str


class Sqlite:

    def __init__(self,
                 db_name: str) -> None:
        self._db_name = db_name
        self._conn = None
        self._cursor = None

    def open_conn(self) -> None:
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_name)
            self._cursor = self._conn.cursor()

    def __enter__(self) -> 'Sqlite':
        self.open_conn()
        return self

    def create_table(self,
                     table_name: str,
                     columns: Dict[str, Union['DataTypes.ColumnTypes', str]]) -> None:
        columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        self._cursor.execute(query)
        self._conn.commit()

    def insert_data(self,
                    table_name: str,
                    data: Dict[str, Union[str, int, float]]) -> None:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self._cursor.execute(query, values)
        self._conn.commit()

    def select_data(self,
                    table_name: str,
                    columns: Union[List[str], str] = '*',
                    where: Optional[List[Dict[str, Union[str, int, float]]]] = None,
                    order_by: Optional[Union['DataTypes.OrderBy', str]] = None,
                    limit: Optional[Union['DataTypes.Limit', int]] = None,
                    fetch: Union[str, 'DataTypes.Fetch'] = 'fetchone') -> Union[Tuple, List[Tuple]]:
        if columns != '*':
            columns = ', '.join(columns)
        if where:
            where_clause = ' WHERE ' + ' OR '.join([' AND '.join([f'{col}=?' for col in d.keys()]) for d in where])
            values = tuple(value for d in where for value in d.values())
        else:
            where_clause = ''
            values = ()
        if order_by:
            order_by_clause = f"ORDER BY {order_by}"
        else:
            order_by_clause = ''
        if limit:
            limit_clause = f"LIMIT {limit}"
        else:
            limit_clause = ""
        query = f"SELECT {columns} FROM {table_name} {where_clause} {order_by_clause} {limit_clause}"
        self._cursor.execute(query, values)
        if fetch == DataTypes.Fetch.FETCHONE:
            result = self._cursor.fetchone()
        elif fetch == DataTypes.Fetch.FETCHALL:
            result = self._cursor.fetchall()
        return result

    def update_data(self,
                    table_name: str,
                    set_data: Dict[str, Union[str, int, float]],
                    where: Optional[List[Dict[str, Union[str, int, float]]]] = None) -> None:
        values = []
        set_clause_parts = []

        for col, value in set_data.items():
            if (isinstance(value, str) and value.startswith('+')) or (isinstance(value, str) and value.startswith('-')):
                col_name = col
                col_value = value[1:]
                sign = value[0]
                set_clause_parts.append(f"{col_name}={col_name}{sign}?")
                values.append(col_value)
            else:
                set_clause_parts.append(f"{col}=?")
                values.append(value)

        set_clause = ', '.join(set_clause_parts)

        if where:
            where_clause_parts = []

            for condition in where:
                where_condition_parts = []

                for col, value in condition.items():
                    where_condition_parts.append(f"{col}=?")
                    values.append(value)

                where_clause_parts.append(" AND ".join(where_condition_parts))

            where_clause = "WHERE " + " OR ".join(where_clause_parts)
        else:
            where_clause = ''

        query = f"UPDATE {table_name} SET {set_clause} {where_clause}"
        self._cursor.execute(query, tuple(values))
        self._conn.commit()

    def delete_data(self,
                    table_name: str,
                    where: Optional[List[Dict[str, Union[str, int, float]]]] = None) -> None:
        if where:
            where_clause = ' WHERE ' + ' OR '.join([' AND '.join([f'{col}=?' for col in d.keys()]) for d in where])
            values = tuple(value for d in where for value in d.values())
        else:
            where_clause = ''
            values = ()
        query = f"DELETE FROM {table_name} {where_clause}"
        self._cursor.execute(query, values)
        self._conn.commit()

    def close_conn(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            self._cursor = None

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_conn()


class AioSqlite:

    def __init__(self,
                 db_name: str) -> None:
        self._db_name = db_name
        self._conn = None
        self._cursor = None

    async def open_conn(self) -> None:
        if self._conn is None:
            self._conn = await aiosqlite.connect(self._db_name)
            self._cursor = await self._conn.cursor()

    async def __aenter__(self) -> 'AioSqlite':
        await self.open_conn()
        return self

    async def create_table(self,
                           table_name: str,
                           columns: Dict[str, Union['DataTypes.ColumnTypes', str]]) -> None:
        columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        await self._cursor.execute(query)
        await self._conn.commit()

    async def insert_data(self,
                          table_name: str,
                          data: Dict[str, Union[str, int, float]]) -> None:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        await self._cursor.execute(query, values)
        await self._conn.commit()

    async def select_data(self,
                          table_name: str,
                          columns: Union[List[str], str] = '*',
                          where: Optional[List[Dict[str, Union[str, int, float]]]] = None,
                          order_by: Optional[Union['DataTypes.OrderBy', str]] = None,
                          limit: Optional[Union['DataTypes.Limit', int]] = None,
                          fetch: Union[str, 'DataTypes.Fetch'] = 'fetchone') -> Union[Tuple, List[Tuple]]:
        if columns != '*':
            columns = ', '.join(columns)
        if where:
            where_clause = ' WHERE ' + ' OR '.join([' AND '.join([f'{col}=?' for col in d.keys()]) for d in where])
            values = tuple(value for d in where for value in d.values())
        else:
            where_clause = ''
            values = ()
        if order_by:
            order_by_clause = f"ORDER BY {order_by}"
        else:
            order_by_clause = ''
        if limit:
            limit_clause = f"LIMIT {limit}"
        else:
            limit_clause = ""
        query = f"SELECT {columns} FROM {table_name} {where_clause} {order_by_clause} {limit_clause}"
        await self._cursor.execute(query, values)
        if fetch == DataTypes.Fetch.FETCHONE:
            result = await self._cursor.fetchone()
        elif fetch == DataTypes.Fetch.FETCHALL:
            result = await self._cursor.fetchall()
        return result

    async def update_data(self,
                          table_name: str,
                          set_data: Dict[str, Union[str, int, float]],
                          where: Optional[List[Dict[str, Union[str, int, float]]]] = None) -> None:
        values = []
        set_clause_parts = []

        for col, value in set_data.items():
            if (isinstance(value, str) and value.startswith('+')) or (isinstance(value, str) and value.startswith('-')):
                col_name = col
                col_value = value[1:]
                sign = value[0]
                set_clause_parts.append(f"{col_name}={col_name}{sign}?")
                values.append(col_value)
            else:
                set_clause_parts.append(f"{col}=?")
                values.append(value)

        set_clause = ', '.join(set_clause_parts)

        if where:
            where_clause_parts = []

            for condition in where:
                where_condition_parts = []

                for col, value in condition.items():
                    where_condition_parts.append(f"{col}=?")
                    values.append(value)

                where_clause_parts.append(" AND ".join(where_condition_parts))

            where_clause = "WHERE " + " OR ".join(where_clause_parts)
        else:
            where_clause = ''

        query = f"UPDATE {table_name} SET {set_clause} {where_clause}"
        await self._cursor.execute(query, tuple(values))
        await self._conn.commit()

    async def delete_data(self,
                          table_name: str,
                          where: Optional[List[Dict[str, Union[str, int, float]]]] = None) -> None:
        if where:
            where_clause = ' WHERE ' + ' OR '.join([' AND '.join([f'{col}=?' for col in d.keys()]) for d in where])
            values = tuple(value for d in where for value in d.values())
        else:
            where_clause = ''
            values = ()
        query = f"DELETE FROM {table_name} {where_clause}"
        await self._cursor.execute(query, values)
        await self._conn.commit()

    async def close_conn(self) -> None:
        if self._conn is not None:
            await self._conn.close()
            self._conn = None
            self._cursor = None

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close_conn()
