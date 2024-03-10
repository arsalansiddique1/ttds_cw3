import sys
import re
import connect_connector
import sqlalchemy

db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()

with db.connect() as conn:

    stmt = sqlalchemy.text(
        "SELECT * FROM captions2 WHERE id=1;"
    )
    conn.execute(stmt)
