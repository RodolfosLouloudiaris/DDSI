import oracledb
from config import ORACLE_DSN, ORACLE_USER, ORACLE_PASSWORD

pool = None

def init_pool():
    global pool
    if pool is None:
        pool = oracledb.create_pool(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
            min=1,        # Minimum sessions
            max=3,        # Maximum sessions allowed
            increment=1,  # How many to create when more needed
            homogeneous=True
        )

def get_connection():
    """
    Acquire connection from the Oracle connection pool.
    """
    if pool is None:
        init_pool()

    return pool.acquire()
