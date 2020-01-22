from pyhive import hive

# Connect to database
conn = hive.Connection(
    host='cmp-19nr03.uea.ac.uk',
    port='10000',
    auth='NOSASL',
    database='perfdata',
)

cursor = conn.cursor()

cursor.execute('SHOW TABLES')

for table in cursor.fetchall():
    print(table)
