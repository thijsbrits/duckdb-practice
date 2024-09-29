import duckdb
from dataclasses import astuple
import argparse

from database import init_db
from models import ElectricVehicle
from utils import load_csv_rows, create_placeholder_str
import logging
from queries import (
    count_cars_per_city,
    find_top3_popular_ev,
    find_popular_ev_postal_code,
    count_ev_by_model_year_as_parquet
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_electric_vehicles_from_csv(conn, csv_path):
    """Populate the electricvehicles table from a CSV file."""

    table_name = "electricvehicles"
    field_names = ElectricVehicle.field_names()
    columns_str = ", ".join(field_names)
    placeholders_str = create_placeholder_str(field_names)
    insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders_str})"

    logger.info("Starting insertion into electricvehicles from CSV file.")

    # Collect all records to be inserted
    records_to_insert = []
    for row in load_csv_rows(csv_path):
        electric_vehicle = ElectricVehicle.from_dict(row)
        records_to_insert.append(astuple(electric_vehicle))

    total_records = len(records_to_insert)

    try:
        conn.executemany(insert_query, records_to_insert)

        # Verify the number of records inserted
        db_record_count = conn.execute('SELECT COUNT(*) FROM electricvehicles').fetchone()[0]
        assert total_records == db_record_count, (
            f"Mismatch in record counts: expected {total_records}, "
            f"found {db_record_count}"
        )

        logger.info(f"Insertion successful. Total records inserted: {total_records}")
    except Exception as e:
        logger.error(f"An error occurred during insertion: {e}")
        raise



def main(csv_path, ddl_path, db_path):
    with duckdb.connect(db_path) as conn:
        init_db(conn, ddl_path)
        populate_electric_vehicles_from_csv(conn, csv_path)

        # Chose to just print the outputs.
        # Wasn't really clear how to report the output of the query
        print(count_cars_per_city(conn))
        print(find_top3_popular_ev(conn))
        print(find_popular_ev_postal_code(conn))

        count_ev_by_model_year_as_parquet(conn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process electric vehicle data.')
    parser.add_argument('--csv-path', default='data/Electric_Vehicle_Population_Data.csv')
    parser.add_argument('--ddl-path', default='electricvehicles.ddl')
    parser.add_argument('--db-path', default='electric-cars.db')
    args = parser.parse_args()

    main(**vars(args))
