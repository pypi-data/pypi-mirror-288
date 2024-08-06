# import urllib
#
# import pytest
# from sqlalchemy import text
#
# from database_helper.database.sync_db import SyncDatabase  # Adjust the import path as necessary
#
# username = "admin"
# password = "Mysql@12345"
# host = "43.205.214.5"
# database = "test"
#
# encoded_password = urllib.parse.quote(password)
#
# # Constants for database connection - replace with your details
# CONNECTION_STRING = f"mysql+mysqlconnector://{username}:{encoded_password}@{host}/{database}"
#
# @pytest.fixture
# def db_instance():
#     db = SyncDatabase(CONNECTION_STRING)
#     with db as instance:
#         yield instance
#     # db.close()
#
#
# def test_execute_query(db_instance):
#     # This should be a query that fetches data. Adjust the SQL to match your schema.
#     query = text("SELECT * FROM mstBrands WHERE BrandID = 12163")
#     result = db_instance.execute_query(query)
#     assert result is not None
#     assert len(result) > 0  # Adjust based on expected results
#
#
# def test_query_dataframe(db_instance):
#     # This assumes that pandas is installed and the table has at least one row
#     query = text("SELECT * FROM mstBrands WHERE BrandID = 12163")
#     df = db_instance.query_dataframe(query)
#     assert not df.empty  # This checks that the dataframe is not empty
#     assert 'BrandID' in df.columns
from sqlalchemy import select

# Example usage for multiple databases
# from sqlalchemy import select

# from database_helper.database.sync_db import SyncDatabase
from database_helper.database.sync_db_advance import AdvanceSyncDatabase

config = {'host': '43.205.214.5', 'port': '1433', 'username': 'sa', 'password': 'Mssql1%401234'}

# Initialize SyncDatabase for multiple databases
db_multi = AdvanceSyncDatabase(config_obj=config, db_type='sqlserver', use_multiple_databases=True)

# Query on db1
db_name1 = 'db1'
with db_multi:
    db_multi.initialize_tables(['table1'], db_name=db_name1)
    table = db_multi.tables[db_name1]['table1']
    result = db_multi.execute_query(select(table), db_name=db_name1).fetchall()
    print(result)
    # for row in result:
    #     print(f"Result from {db_name1}: {row}")

# Query on db2
db_name2 = 'db2'
with db_multi:
    db_multi.initialize_tables(['table2'], db_name=db_name2)
    table = db_multi.tables[db_name2]['table2']
    result = db_multi.execute_query(select(table), db_name=db_name2)
    print(result)
    # for row in result:
    #     print(f"Result from {db_name2}: {row}")
