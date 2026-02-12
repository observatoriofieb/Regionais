# import pyodbc
import sqlalchemy

def pega_engine():
    servername = r'fbd101-001\HML'
    dbname = 'DB_OBSERVATORIO'
    engine = sqlalchemy.create_engine('mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server', fast_executemany=True)
    return engine

def pega_engine_proteus():
    servername = r'fbp101-113'
    dbname = 'DB_DW_FIEB'
    engine = sqlalchemy.create_engine('mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server', fast_executemany=True)
    return engine

def pega_engine_guia():
    servername = r'fbp101-053'
    dbname = 'DB_GUIA_INDUSTRIAL'
    engine = sqlalchemy.create_engine('mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server', fast_executemany=True)
    return engine

def pega_engine_sfieb():
    servername = r'fbp101-113'
    dbname = 'DB_OBSERVATORIO_SFIEB'
    engine = sqlalchemy.create_engine('mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server', fast_executemany=True)
    return engine

def pega_engine_interno():
    servername = r'fbp101-024\sfieb01'
    dbname = 'DB_OBSERVATORIO_INTERNO'
    engine = sqlalchemy.create_engine('mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server', fast_executemany=True)
    return engine
