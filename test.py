import psycopg2

conn_params = {
    'dbname': 'FinalProject',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost'
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()
conn.autocommit = True

cursor.execute(open(r"--Data Ingestion--.sql", "r").read())