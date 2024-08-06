import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from functools import lru_cache
from database_helper.database.utilities import construct_connection_string
from database_helper.database.constants_conn import MAX_CONNECTIONS, MIN_CONNECTIONS


class AdvanceAsyncDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AdvanceAsyncDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_type=None, config_obj=None, pool_size=MIN_CONNECTIONS, max_overflow=MAX_CONNECTIONS,
                 use_multiple_databases=False):
        if not hasattr(self, "initialized"):
            self.connection_string = None
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.engine: AsyncEngine = None
            self.Session = None
            self.tables = {}
            self.use_multiple_databases = use_multiple_databases
            self.db_type = db_type
            self.config_obj = config_obj
            self.initialized = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()
            print('Database disconnected')

    @lru_cache(maxsize=10)  # Cache up to 10 engines
    def get_engine_for_db(self, db_name):
        connection_string = construct_connection_string(self.config_obj, self.db_type, db_name=db_name)
        engine = create_async_engine(
            connection_string,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow
        )
        return engine

    async def connect(self, db_name):
        try:
            self.engine = self.get_engine_for_db(db_name)
            self.Session = sessionmaker(
                self.engine, expire_on_commit=False, class_=AsyncSession
            )
            print(f'Database {db_name} connected')
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    async def initialize_tables(self, table_names, db_name=None):
        try:
            engine = self.get_engine_for_db(db_name) if self.use_multiple_databases and db_name else self.engine
            if not engine:
                await self.connect(db_name)
            metadata = MetaData()
            if db_name not in self.tables:
                self.tables[db_name] = {}
            for table_name in table_names:
                if table_name not in self.tables[db_name]:
                    async with engine.connect() as conn:
                        await conn.run_sync(metadata.reflect, only=[table_name])
                        self.tables[db_name][table_name] = metadata.tables[table_name]
        except Exception as e:
            raise Exception(f"Error in initialize tables: {e}")

    async def execute_query(self, query, db_name=None):
        engine = self.get_engine_for_db(db_name) if self.use_multiple_databases and db_name else self.engine
        async with AsyncSession(engine) as session:
            async with session.begin():
                try:
                    result = await session.execute(query)
                    if query.is_update or query.is_insert or query.is_delete:
                        await session.commit()
                    return result
                except Exception as e:
                    await session.rollback()
                    raise Exception(f"Error in query execution: {e}")
