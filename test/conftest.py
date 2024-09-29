import duckdb
import pytest
from database import install_spatial


@pytest.fixture(scope="session")
def conn():
    # make an in memory database for testing purposes
    conn = duckdb.connect(database=':memory:')
    install_spatial(conn)
    yield conn
    conn.close()
