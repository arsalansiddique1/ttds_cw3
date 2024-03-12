import os
import psycopg2

# Read database credentials from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

print(DB_NAME)
print(DB_USER)
print(DB_PASSWORD)
print(DB_HOST)

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

with conn.cursor() as c:
    sql = "SELECT * FROM captions2 WHERE id=1;"
    c.execute(sql)
    rows = c.fetchall()

    for row in rows:
        print(row)

