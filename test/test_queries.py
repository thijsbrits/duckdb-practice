import pytest
import os

from queries import (
    count_cars_per_city,
    find_top3_popular_ev,
    find_popular_ev_postal_code,
    count_ev_by_model_year_as_parquet,
)
from test.conftest import conn
import duckdb

@pytest.fixture
def populated_db(conn):
    conn = duckdb.connect(database=':memory:')

    conn.execute("""
    CREATE TABLE electricvehicles (
        make VARCHAR,
        model VARCHAR,
        model_year INTEGER,
        city VARCHAR,
        postal_code VARCHAR
    )
    """)

    # Insert sample data
    sample_data = [
        ('Tesla', 'Model S', 2020, 'San Francisco', '90001'),
        ('Tesla', 'Model 3', 2021, 'San Francisco', '90001'),
        ('Nissan', 'Leaf', 2019, 'San Jose', '90001'),
        ('Chevrolet', 'Bolt', 2020, 'San Jose', '90002'),
        ('Tesla', 'Model S', 2021, 'Los Angeles', '90001'),
        ('Tesla', 'Model 3', 2020, 'Los Angeles', '90002'),
        ('Nissan', 'Leaf', 2021, 'San Francisco', '90002'),
        ('Tesla', 'Model S', 2021, 'San Francisco', '90002'),
        ('Ford', 'Mustang Mach-E', 2021, 'Los Angeles', '90002'),
        ('Chevrolet', 'Bolt', 2021, 'San Jose', '90002'),
    ]
    conn.executemany("""
    INSERT INTO electricvehicles (make, model, model_year, city, postal_code)
    VALUES (?, ?, ?, ?, ?)
    """, sample_data)
    conn.commit()
    yield conn
    conn.close()

def test_count_cars_per_city(populated_db):
    result = count_cars_per_city(populated_db)
    expected = [('Los Angeles', 3), ('San Francisco', 4), ('San Jose', 3)]
    assert sorted(result) == sorted(expected)

def test_find_top3_popular_ev(populated_db):
    result = find_top3_popular_ev(populated_db)
    expected = [('Nissan', 'Leaf', 2), ('Chevrolet', 'Bolt', 2), ('Tesla', 'Model S', 3), ('Tesla', 'Model 3', 2)]
    assert sorted(result) == sorted(expected)

def test_find_popular_ev_postal_code(populated_db):
    result = find_popular_ev_postal_code(populated_db)
    expected = [
        ('90001', 'Tesla', 'Model S', 2),
        ('90002', 'Chevrolet', 'Bolt', 2),
    ]
    assert sorted(result) == sorted(expected)

def test_count_ev_by_model_year_as_parquet(populated_db, tmpdir):
    # Change to temporary directory to avoid filesystem issues
    os.chdir(tmpdir)
    count_ev_by_model_year_as_parquet(populated_db)

    result = populated_db.execute("SELECT * FROM model_year_vehicle_count").fetchall()
    expected = [
        (2019, 1),
        (2020, 3),
        (2021, 6),
    ]
    assert sorted(result) == sorted(expected)

    assert os.path.exists('model_year_vehicle_count.parquet')

