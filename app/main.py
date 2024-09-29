import duckdb
from dataclasses import astuple
import argparse

from app.database import init_db
from app.models import ElectricVehicle
from app.utils import load_csv_rows, create_placeholder_str
import logging
from app.queries import (
    count_cars_per_city,
    find_top3_popular_ev,
    find_popular_ev_postal_code,
    count_ev_by_model_year_as_parquet
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_electric_vehicles_from_csv(conn, csv_path):
    field_names = ElectricVehicle.field_names()
    columns_str = ", ".join(field_names)
    placeholders_str = create_placeholder_str(field_names)
    insert_query = f'''INSERT INTO electricvehicles ({columns_str}) VALUES ({placeholders_str})'''

    conn.execute("BEGIN TRANSACTION")

    for row in load_csv_rows(csv_path):
        electric_vehicle = ElectricVehicle.from_dict(row)
        conn.execute(insert_query, astuple(electric_vehicle))

    conn.execute("COMMIT")


def main(csv_path, ddl_path, db_path):
    with duckdb.connect(db_path) as conn:
        init_db(conn, ddl_path)

        populate_electric_vehicles_from_csv(conn, csv_path)

        count_cars_per_city(conn)
        find_top3_popular_ev(conn)
        find_popular_ev_postal_code(conn)
        count_ev_by_model_year_as_parquet(conn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process electric vehicle data.')
    parser.add_argument('--csv-path', default='data/Electric_Vehicle_Population_Data.csv')
    parser.add_argument('--ddl-path', default='electricvehicles.ddl')
    parser.add_argument('--db-path', default='electric-cars.db')
    args = parser.parse_args()

    main(**vars(args))
