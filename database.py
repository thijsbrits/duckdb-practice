import sys
from pathlib import Path

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(conn, ddl_path):
    install_spatial(conn)
    # for repeated running, would not do this in prod normally ofcourse
    conn.execute('DROP TABLE IF EXISTS electricvehicles')
    cars_ddl = Path(ddl_path).read_text()
    conn.execute(cars_ddl)


def install_spatial(conn):
    try:
        logger.info("Installing spatial for duckdb")
        conn.execute("INSTALL spatial")
        conn.execute("LOAD spatial")
        logger.info("Spatial installed")
    except Exception as e:
        logger.error(f"Failed to install/load spatial extension: {e}")
        sys.exit(1)
