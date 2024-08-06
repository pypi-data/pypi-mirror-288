def get_default_db_info():
    return {
        'postgresql': {'driver': 'psycopg2', 'port': '5432', 'extra_params': None},
        'mysql': {'driver': 'pymysql', 'port': '3306', 'extra_params': None},
        'mssql': {
            'driver': 'pyodbc',
            'port': '1433',
            'extra_params': 'driver=ODBC Driver 17 for SQL Server'  # Common default
        },
        'oracle': {'driver': 'cx_oracle', 'port': '1521', 'extra_params': None},
        'sqlite': {'driver': None, 'port': None, 'extra_params': None},  # SQLite does not require a driver or port
        'cockroachdb': {'driver': 'psycopg2', 'port': '26257', 'extra_params': None}
    }

def construct_connection_string(db_info, db_type,db_name = None):
    db_default_info = get_default_db_info().get(db_type, {})
    username = db_info.get('username')
    password = db_info.get('password')
    host = db_info.get('host') or db_default_info.get(f'{db_type}').get('host')
    port = db_info.get('port') or db_default_info.get(f'{db_type}').get('port')
    database = db_name or db_info.get('database') or db_info.get('_extra_properties').get('database') or db_default_info.get(f'{db_type}').get('database')

    if db_type == 'postgresql':
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    elif db_type == 'mysql':
        return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    elif db_type == 'sqlite':
        return f"sqlite:///{database}"
    elif db_type == 'sqlserver':
        return f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    elif db_type == 'oracle':
        return f"oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={database}"
    else:
        raise ValueError(f"Unsupported db_type: {db_type}")
