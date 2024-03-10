import os
import psycopg2

# Read database credentials from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

print("xxxx")
print(DB_NAME)
print(DB_USER)
print(DB_PASSWORD)
print(DB_HOST)

MAX_NUM_RESULTS = 500

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cursor = conn.cursor()
sql = "SELECT * FROM captions2 WHERE id=1;"

# Execute the query with the list of terms as a parameter
cursor.execute(sql)

# Fetch all rows
matching_rows = cursor.fetchall()

# Close connection
conn.close()

for row in matching_rows:
    print(row)
