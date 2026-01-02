from db import get_connection

def execute_sql_script(path: str):
    """
    Read sql file and execute statements one after another
    """
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    statements = [s.strip() for s in sql.split(";") if s.strip()]

    conn = get_connection()
    cur = conn.cursor()

    try:
        for stmt in statements:
            cur.execute(stmt)
        conn.commit()
    finally:
        cur.close()
        conn.close()

def drop_all_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Get list of all user tables
    cur.execute("SELECT table_name FROM user_tables")
    tables = [row[0] for row in cur.fetchall()]

    for table in tables:
        try:
            cur.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
        except:
            pass

    conn.commit()
    cur.close()
    conn.close()

def init_database():
    drop_all_tables()
    execute_sql_script("sql-stuff/sql_schema.sql")
    execute_sql_script("sql-stuff/seed.sql")
