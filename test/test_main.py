import os
import pytest
import tempfile
import csv
from main import populate_electric_vehicles_from_csv
from test.test_ddl import create_electricvehicles_from_ddl

@pytest.fixture
def electric_vehicle_data():
    return {
        'VIN (1-10)': '5YJ3E1EB4L',
        'County': 'Yakima',
        'City': 'Yakima',
        'State': 'WA',
        'Postal Code': '98908',
        'Model Year': '2020',
        'Make': 'TESLA',
        'Model': 'MODEL 3',
        'Electric Vehicle Type': 'Battery Electric Vehicle (BEV)',
        'Clean Alternative Fuel Vehicle (CAFV) Eligibility': 'Clean Alternative Fuel Vehicle Eligible',
        'Electric Range': '322',
        'Base MSRP': '0',
        'Legislative District': '14',
        'DOL Vehicle ID': '127175366',
        'Vehicle Location': 'POINT (-120.56916 46.58514)',
        'Electric Utility': 'PACIFICORP',
        '2020 Census Tract': '53077000904'
    }


@pytest.fixture
def mock_electric_vehicles_csv(electric_vehicle_data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        # Write some data to the CSV file
        writer = csv.writer(temp_file)

        writer.writerow(list(electric_vehicle_data.keys()))
        writer.writerow(list(electric_vehicle_data.values()))

    # Yield the file path
    yield temp_file.name

    # Clean up the file after the test
    os.unlink(temp_file.name)


def test_populate_electric_vehicles_from_csv(
        conn,
        mock_electric_vehicles_csv,
        electric_vehicle_data,
        create_electricvehicles_from_ddl,
):

    populate_electric_vehicles_from_csv(conn, mock_electric_vehicles_csv)

    result = conn.execute("""SELECT * FROM electricvehicles""").fetchall()

    # mostly to test the whole integration, would to type checking in other unit tests
    assert len(result) == 1
