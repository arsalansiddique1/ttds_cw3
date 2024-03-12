import psycopg2
import psycopg2.extras
import os
import traceback

# Connect to PostgreSQL database
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

try:
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST) as conn:
        with conn.cursor() as cursor:
            with conn.cursor() as cur2:

                # Fetch data from the caption table
                cursor.execute("SELECT term FROM terms ORDER BY term")

                cur_row = 0

                while True:
                    try:
                        rows = cursor.fetchmany(1000)  # Fetch 1000 rows at a time

                        if not rows:
                            break

                        #show progress
                        print(f"IDs Range: {cur_row} - {cur_row+9}")
                        print(f"Terms Range: {rows[0][0]} - {rows[-1][0]}")
                        
                        #run query to insert term, json into the table
                        query_basic = sql = f"""
                        INSERT INTO terms_json (term, json_data)
                        SELECT term,
                            json_object_agg(id, positions) AS json_data
                        FROM (
                            SELECT term,
                                id,
                                ARRAY_AGG(position ORDER BY position) AS positions
                            FROM middle
                            WHERE term = ANY(%s)
                            GROUP BY term, id
                        ) AS subquery
                        GROUP BY term;
                        """

                        # Batch insert into terms table
                        cur2.execute(query_basic, (rows,))

                        # Commit after processing each chunk
                        conn.commit()

                        cur_row += 1000
                    
                    except Exception as e:
                        # Log the error along with the range of IDs where the error occurred
                        with open("json_error_log.txt", "a") as error_log_file:
                            error_log_file.write(f"Error: {str(e)}\n")
                            error_log_file.write(f"IDs Range: {rows[0][0]} - {rows[-1][0]}\n")
                            traceback.print_exc(file=error_log_file)  # Detailed traceback logging
                        #print("Error occurred, check error log for details.")
                        conn.rollback()  # Rollback the transaction to ensure data consistency

except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
    print("Program interrupted by user.")
    # If a KeyboardInterrupt occurs, commit any pending transactions and close the database connection
    if 'conn' in locals():
        conn.commit()
        cursor.close()
        cur2.close()
        conn.close()
    print("Database connection closed.")
    exit()
except Exception as e:
    # Handle other exceptions
    print(f"Error: {str(e)}")
    # If an exception occurs, commit any pending transactions and close the database connection
    if 'conn' in locals():
        conn.commit()
        cursor.close()
        cur2.close()
        conn.close()
    print("Database connection closed.")
    exit()
else:
    conn.commit()
    cursor.close()
    cur2.close()
    conn.close()
