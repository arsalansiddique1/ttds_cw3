import connect_connector
import sqlalchemy

db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()

with db.connect() as conn:
    ids = ['8558487', '8558735']

    ids_str = ', '.join(ids)

    sql = f"SELECT DISTINCT ON (title, caption) * FROM captions2 WHERE id IN ({ids_str});"

    stmt = sqlalchemy.text(sql)
    result = conn.execute(stmt)

    matching_rows = result.fetchall()

    # Fetch all rows
    output_dict = dict()
    columns = [desc[0] for desc in matching_rows]  # Get column names
    output_dict = {row[0]: dict(zip(columns, row)) for row in matching_rows}

    print(output_dict)

# with db.connect() as conn:
#     terms = ['cat', 'dog']
#     sql =f"""
#     SELECT term,
#         json_object_agg(id, positions) AS id_positions
#     FROM (
#         SELECT term,
#             id,
#             ARRAY_AGG(position ORDER BY position) AS positions
#         FROM middle
#         WHERE term = ANY(:terms)
#         GROUP BY term, id
#     ) AS subquery
#     GROUP BY term;
#     """

#     print(sql)

#     stmt = sqlalchemy.text(sql)
#     # Bind the term parameter to the statement
#     stmt = stmt.bindparams(terms=terms)
#     result = conn.execute(stmt)

#     matching_rows = result.fetchall()

#     print(matching_rows)

#     print(matching_rows[0])
#     print(matching_rows[1])