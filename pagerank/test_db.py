import connect_connector
import sqlalchemy

db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()

with db.connect() as conn:
    stmt = sqlalchemy.text(
        "INSERT INTO test VALUES (1, 'Joe')"
    )
    conn.execute(stmt)


