from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from database_helper.database.utilities import construct_connection_string
from database_helper.database.constants_conn import MAX_CONNECTIONS, MIN_CONNECTIONS
from functools import lru_cache


class AdvanceSyncDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AdvanceSyncDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_type=None, config_obj=None, pool_size=MIN_CONNECTIONS, max_overflow=MAX_CONNECTIONS,
                 use_multiple_databases=False):
        if not hasattr(self, "initialized"):
            self.connection_string = None
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.engine: Engine = None
            self.Session = None
            self.tables = {}
            self.use_multiple_databases = use_multiple_databases
            self.db_type = db_type
            self.config_obj = config_obj
            self.initialized = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disconnect()

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            print('Database disconnected')

    @lru_cache(maxsize=10)  # Cache up to 10 engines
    def get_engine_for_db(self, db_name):
        connection_string = construct_connection_string(self.config_obj, self.db_type, db_name=db_name)
        engine = create_engine(
            connection_string,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow
        )
        return engine

    def connect(self, db_name):
        try:
            self.engine = self.get_engine_for_db(db_name)
            self.Session = sessionmaker(bind=self.engine)
            print(f'Database {db_name} connected')
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def initialize_tables(self, table_names, db_name):
        try:
            engine = self.get_engine_for_db(db_name)
            if not engine:
                self.connect(db_name)
            metadata = MetaData()
            if db_name not in self.tables:
                self.tables[db_name] = {}
            for table_name in table_names:
                if table_name not in self.tables[db_name]:
                    metadata.reflect(bind=engine, only=[table_name], views=True)
                    self.tables[db_name][table_name] = metadata.tables[table_name]
        except Exception as e:
            raise Exception(f"Error in initialize tables: {e}")

    def execute_query(self, query, db_name=None):
        engine = self.get_engine_for_db(db_name)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        try:
            result = session.execute(query)
            if query.is_update or query.is_insert or query.is_delete:
                session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise Exception(f"Error in query execution: {e}")
        # finally:
        #     session.close()
