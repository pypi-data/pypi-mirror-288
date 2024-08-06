from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.sql import Select
from database_helper.database.constants_conn import MAX_CONNECTIONS,MIN_CONNECTIONS
from database_helper.database.utilities import construct_connection_string


class AsyncDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AsyncDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, connection_string,db_type=None,  config_obj=None, pool_size=MIN_CONNECTIONS, max_overflow=MAX_CONNECTIONS):
        if not hasattr(self, "initialized"):
            self.connection_string = connection_string or construct_connection_string(config_obj, db_type)
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.engine: AsyncEngine = None
            self.tables = {}
            self.is_connected = False
            self.initialized = True

    async def connect(self):
        if not self.is_connected:
            self.engine = create_async_engine(
                self.connection_string,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow
            )
            print('Database connected')
            self.is_connected = True

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()
            print('Database disconnected')
            self.is_connected = False

    async def initialize_tables(self, table_names):
        try:
            if not self.is_connected:
                await self.connect()
            metadata = MetaData()
            async with self.engine.connect() as connection:
                for table_name in table_names:
                    if table_name not in self.tables:
                        await connection.run_sync(metadata.reflect, only=[table_name],views = True)
                        self.tables[table_name] = metadata.tables[table_name]
        except Exception as e:
            raise Exception(f"Error in initialize tables : {e}")

        print("Tables initialized:", list(self.tables.keys()))

    async def execute_query(self, query):
        try:
            if not self.is_connected:
                await self.connect()
            async with self.engine.connect() as connection:
                result = await connection.execute(query)  # Commit for update/insert/delete queries
                if isinstance(query, Select):
                    return result.fetchall()  # Return all rows for select queries asynchronously
                else:
                    await connection.commit()
                    return result.rowcount  # Return the number of rows affected for update/insert/delete queries
        except Exception as e:
            raise Exception(f"Error in query execution : {e}")

    async def __aenter__(self):
        if not self.is_connected:
            await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # Do not disconnect on exit to keep the connection open
        pass

