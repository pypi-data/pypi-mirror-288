from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from database_helper.database.utilities import construct_connection_string
from database_helper.database.constants_conn import MAX_CONNECTIONS,MIN_CONNECTIONS
class SyncDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SyncDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, connection_string, db_type = None,  config_obj=None, pool_size=MIN_CONNECTIONS, max_overflow=MAX_CONNECTIONS):
        if not hasattr(self, "initialized"):
            self.connection_string = connection_string or construct_connection_string(config_obj, db_type)
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.engine: Engine = None
            self.Session = None
            self.tables = {}
            self.initialized = True

    def __enter__(self):
        if not self.engine:
            self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disconnect()

    def connect(self):
        try:
            self.engine = create_engine(
                self.connection_string,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow
            )
            self.Session = sessionmaker(bind=self.engine)
            print('Database connected')
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            print('Database disconnected')

    def initialize_tables(self, table_names):
        try:
            if not self.engine:
                self.connect()
            metadata = MetaData()
            for table_name in table_names:
                if table_name not in self.tables:
                    metadata.reflect(bind=self.engine, only=[table_name],views=True)
                    self.tables[table_name] = metadata.tables[table_name]
        except Exception as e:
            raise Exception(f"Error in initialize tables: {e}")

    def execute_query(self, query):
        session = self.Session()
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

