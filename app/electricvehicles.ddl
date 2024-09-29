CREATE TABLE IF NOT EXISTS electricvehicles (
    vin_first10 VARCHAR CHECK (length(vin_first10) <= 10), -- val has a maximum length of 10
    county VARCHAR,
    city VARCHAR,
    state VARCHAR(2) CHECK (length(state) <= 2),
    postal_code VARCHAR(10),
    model_year INTEGER,
    make VARCHAR,
    model VARCHAR,
    electric_vehicle_type VARCHAR,
    cafv_eligibility VARCHAR,
    electric_range INTEGER,
    base_msrp INTEGER,
    legislative_district INTEGER,
    dol_vehicle_id BIGINT,
    vehicle_location GEOMETRY,
    electric_utility VARCHAR,
    census_tract VARCHAR(11)
);