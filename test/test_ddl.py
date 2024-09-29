import duckdb
import pytest
from pathlib import Path

from test.conftest import conn


@pytest.fixture(scope="session")
def create_electricvehicles_from_ddl(conn):
    create_table_query = Path("electricvehicles.ddl").read_text()
    conn.execute(create_table_query)


@pytest.fixture(scope="session")
def electricvehicle():
    return "'5YJ3E1EB4L', 'Yakima', 'Yakima', 'WA', '98908', 2020, 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 322, 0, 14, 127175366, 'POINT (-120.56916 46.58514)', 'PACIFICORP', 53077000904"


@pytest.fixture(scope="session")
def corrupted_vin_electricvehicle():
    return "'5YJ3E1EB4L__', 'Yakima', 'Yakima', 'WA', '98908', 2020, 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 322, 0, 14, 127175366, 'POINT (-120.56916 46.58514)', 'PACIFICORP', 53077000904"


@pytest.fixture(scope="session")
def corrupted_model_year_empty_string_electricvehicle():
    return "'5YJ3E1EB4L', 'Yakima', 'Yakima', 'WA', '98908', '', 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 322, 0, 14, 127175366, 'POINT (-120.56916 46.58514)', 'PACIFICORP', 53077000904"


@pytest.fixture(scope="session")
def insert_electric_vehicle(conn, create_electricvehicles_from_ddl, electricvehicle):
    insert_query = f"INSERT INTO electricvehicles VALUES ({electricvehicle})"
    conn.execute(insert_query)


def test_create_table(conn, create_electricvehicles_from_ddl):
    result = conn.execute("SHOW TABLES;").fetchone()
    assert result[0] == "electricvehicles"


def test_insert_data_to_electricvehicles(conn, insert_electric_vehicle):
    result = conn.execute("SELECT * FROM electricvehicles").fetchall()
    assert len(result) == 1


def test_spatial_query(conn, insert_electric_vehicle):
    result = conn.execute("""SELECT ST_AsText(vehicle_location) FROM electricvehicles;""").fetchone()
    assert result[0] == 'POINT (-120.56916 46.58514)'

    result = conn.execute("""
SELECT ST_AsText(vehicle_location) FROM electricvehicles 
WHERE ST_Equals(vehicle_location, ST_GeomFromText('POINT (-120.56916 46.58514)'))
""").fetchall()
    assert len(result) == 1


def test_insert_incorrect_vin(conn, create_electricvehicles_from_ddl, corrupted_vin_electricvehicle):
    insert_query = f"INSERT INTO electricvehicles VALUES ({corrupted_vin_electricvehicle})"

    with pytest.raises(duckdb.ConstraintException):
        conn.execute(insert_query)


def test_insert_incorrect_postal_code(conn, create_electricvehicles_from_ddl, corrupted_model_year_empty_string_electricvehicle):
    insert_query = f"INSERT INTO electricvehicles VALUES ({corrupted_model_year_empty_string_electricvehicle})"

    with pytest.raises(duckdb.ConversionException):
        conn.execute(insert_query)

