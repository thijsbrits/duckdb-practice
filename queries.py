def count_cars_per_city(conn):
    """Count the number of electric cars per city."""
    result = conn.execute("""SELECT city, COUNT(*) AS cars_in_city FROM electricvehicles GROUP BY city""").fetchall()
    return result


def find_top3_popular_ev(conn):
    """Find the top 3 most popular electric vehicles."""

    result = conn.execute(
    """
WITH vehiclecounts AS (
  SELECT 
    make,
    model,
    COUNT(*) AS model_count
  FROM electricvehicles
  GROUP BY make, model
),
ranked_vehicles AS (
  SELECT 
    make,
    model,
    model_count,
    RANK() OVER (ORDER BY model_count DESC) as rank
  FROM vehiclecounts
)
SELECT make, model, model_count
FROM ranked_vehicles
WHERE rank <= 3
ORDER BY rank, make, model;""").fetchall()
    return result


def find_popular_ev_postal_code(conn):
    """Find the most popular electric vehicle in each postal code."""
    result = conn.execute("""
WITH popular_vehicles AS (
    SELECT postal_code, make, model, COUNT(*) AS popularity
    FROM electricvehicles
    GROUP BY postal_code, make, model
),
ranked_vehicles AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY postal_code ORDER BY popularity DESC) AS rank
    FROM popular_vehicles
)
SELECT postal_code, make, model, popularity
FROM ranked_vehicles
WHERE rank = 1;
""").fetchall()
    return result


def count_ev_by_model_year_as_parquet(conn):
    """Count the number of electric cars by model year. Write out the answer as parquet files partitioned by year."""
    conn.execute("""
CREATE TABLE IF NOT EXISTS model_year_vehicle_count AS
SELECT model_year, COUNT(*) AS vehicle_count
FROM electricvehicles
GROUP BY model_year""")

    conn.execute("""COPY model_year_vehicle_count TO 'model_year_vehicle_count.parquet' (FORMAT PARQUET, PARTITION_BY model_year, OVERWRITE_OR_IGNORE);""")
