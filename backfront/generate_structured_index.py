import connect_connector
import sqlalchemy

db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()


with db.connect() as conn1, db.connect() as conn2:
    sql = """
    SELECT term FROM terms ORDER BY term;
    """
    stmt = sqlalchemy.text(sql)
    result = conn1.execute(stmt)
    while True:
        rows = result.fetchmany(10)
        print(rows)
        if not rows:
            print("lalalal")
            break

        terms = [row[0] for row in rows]
        print(terms)
        sql =f"""
        SELECT term,
            json_object_agg(id, tf) AS id_positions
        FROM (
            SELECT term,
                id,
                COUNT(position) AS tf
            FROM middle
            WHERE term = ANY(:terms)
            GROUP BY term, id
        ) AS subquery
        GROUP BY term;
        """

        stmt = sqlalchemy.text(sql)
        # Bind the term parameter to the statement
        stmt = stmt.bindparams(terms=terms)
        result = conn2.execute(stmt)

        matching_rows = result.fetchall()
        #print(matching_rows)
        for term, positions in matching_rows:
            print(term, str(positions))
            #print(positions)