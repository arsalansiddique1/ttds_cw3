import psycopg2
import psycopg2.extras
import os
import traceback
import pandas as pd
import time

#DELETE FOR VM
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Connect to PostgreSQL database
DB_NAME = os.getenv("DBNAME")
DB_USER = os.getenv("DBUSER")
DB_PASSWORD = os.getenv("DBPASS")
DB_HOST = os.getenv("DBHOST")

def execute_batch_update_captions(cursor, values):
    psycopg2.extras.execute_batch(cursor, "UPDATE captions2_copy SET pagerank_score = %s WHERE title = %s", values)

try:
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST) as conn:
        with conn.cursor() as cursor:

                cur_row = 0

                for chunk in pd.read_csv('results_file.tsv', header = None, sep = "\t", chunksize=10000):
                    try:

                        #show progress
                        print(f"IDs Range start: {cur_row}")

                        #prepare data
                        #t1 = time.time()
                        data_to_update_caption = [(x[1], x[0]) for x in chunk.values.tolist() if x[0] == x[0] and x[1] == x[1]]
                        #t2 = time.time()
                        #print("Data preparation time:",t2-t1)

                        #update with execute_batch for better performance
                        #t3 = time.time()
                        execute_batch_update_captions(cursor, data_to_update_caption)
                        #t4 = time.time()
                        #print("Data update time:",t4-t3)
                        
                        # Commit after processing each chunk
                        conn.commit()

                        cur_row += 10000
                    
                    except Exception as e:
                        # Log the error along with the range of IDs where the error occurred
                        with open("pagerank_error_log.txt", "a") as error_log_file:
                            error_log_file.write(f"Error: {str(e)}\n")
                            error_log_file.write(f"IDs start range: {cur_row}\n")
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
        conn.close()
    print("Database connection closed.")
    exit()
else:
    conn.commit()
    cursor.close()
    conn.close()
