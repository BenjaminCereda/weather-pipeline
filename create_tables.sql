PRAGMA foreign_keys = ON;

-- DROP TABLE IF EXISTS hourly_forecast;
-- DROP TABLE IF EXISTS daily_forecast;
-- DROP TABLE IF EXISTS forecast_fetches;
-- DROP TABLE IF EXISTS cities;

CREATE TABLE IF NOT EXISTS cities (
    
    city_id INTEGER PRIMARY KEY,
    city_name TEXT NOT NULL,
    region TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,

    UNIQUE (city_name, region, latitude, longitude)

);

CREATE TABLE IF NOT EXISTS forecast_fetches (

    fetch_id INTEGER PRIMARY KEY,
    pipeline_run_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    fetch_date TEXT NOT NULL,
    raw_response TEXT NOT NULL,

    UNIQUE (fetch_id, pipeline_run_id, city_id),

    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE IF NOT EXISTS hourly_forecast (

    time_id INTEGER PRIMARY KEY,
    fetch_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    day_time TEXT NOT NULL,
    hour_time TEXT NOT NULL,
    temperature_2m REAL,
    visibility REAL,
    relative_humidity_2m REAL,
    precipitation_probability REAL,
    wind_speed_10m REAL,
    
    CHECK (temperature_2m BETWEEN -100 AND 70),
    CHECK (visibility BETWEEN 0 AND 100000),
    CHECK (precipitation_probability BETWEEN 0 AND 100),
    CHECK (relative_humidity_2m BETWEEN 0 AND 100),
    CHECK (wind_speed_10m >= 0),

    UNIQUE (fetch_id, city_id, day_time, hour_time),

    FOREIGN KEY (fetch_id, city_id) REFERENCES forecast_fetches(fetch_id, city_id)
);

CREATE TABLE IF NOT EXISTS daily_forecast (

    date_id INTEGER PRIMARY KEY,
    city_id INTEGER NOT NULL,
    fetch_id INTEGER NOT NULL,
    day_time TEXT NOT NULL,
    temperature_2m REAL,
    visibility REAL,
    relative_humidity_2m REAL,
    precipitation_probability REAL,
    wind_speed_10m REAL,
    
    CHECK (temperature_2m BETWEEN -100 AND 70),
    CHECK (visibility BETWEEN 0 AND 100000),
    CHECK (precipitation_probability BETWEEN 0 AND 100),
    CHECK (relative_humidity_2m BETWEEN 0 AND 100),
    CHECK (wind_speed_10m >= 0),

    UNIQUE (fetch_id, city_id, day_time),

    FOREIGN KEY (fetch_id, city_id) REFERENCES forecast_fetches(fetch_id, city_id)
);
