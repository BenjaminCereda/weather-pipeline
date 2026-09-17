import pandas as pd
import requests
import sqlite3
import datetime
import json
import yaml
import os
import uuid


def fetch_weatherdata(city, latitude, longitude):
    
    url  = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude" : latitude,
        "longitude" : longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation_probability",
            "wind_speed_10m",
            "visibility"
        ],
        "forecast_days": 7,
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params,timeout=180)
        response.raise_for_status()
        data = response.json()
        hourly = data["hourly"]

        df = pd.DataFrame({
            "latitude" : data["latitude"],
            "longitude" : data["longitude"],
            'timezone': data['timezone'],
            "forecast_time": hourly["time"],
            "temperature_2m": hourly["temperature_2m"],
            "visibility": hourly["visibility"],
            "relative_humidity_2m": hourly["relative_humidity_2m"],
            "precipitation_probability": hourly["precipitation_probability"],
            "wind_speed_10m": hourly["wind_speed_10m"],
        })

        df['region'] = df['timezone'].str.split('/', expand=True)[0]
        df['city'] = city
 
        df["forecast_time"] = pd.to_datetime(df["forecast_time"])
        df.loc[:,"day"] = df["forecast_time"].dt.date.astype(str)
        df.loc[:,"time"] = df["forecast_time"].dt.time.astype(str)

        return df, json.dumps(data)

    except Exception as e:
            print(f"Error fetching data: {e}")
            raise

def insert_cities(cur, row):
    
    cur.execute("""SELECT * FROM cities
                WHERE city_name = ?
                AND region = ?
                AND latitude = ?
                AND longitude = ?
                """, row
    )

    result = cur.fetchone()

    if result is not None:
        return result[0]

    cur.execute("""INSERT INTO cities (city_name, region, latitude, longitude)
                VALUES (?,?,?,?)
                """, row
    )

    return cur.lastrowid

def insert_fc_fetch(cur, city_id, raw_text):
    
    date = datetime.datetime.now()

    pipeline_run_id = os.getenv("PIPELINE_RUN_ID")

    #fallback for run_id in case pipeline is triggered manually via python
    if pipeline_run_id is None:
        pipeline_run_id = f"Manual_{str(uuid.uuid4())}"

    cur.execute("""INSERT INTO forecast_fetches (pipeline_run_id, city_id, fetch_date, raw_response)
                VALUES (?,?,?,?)
                """,
                (pipeline_run_id, city_id, date, raw_text)
    )
    return cur.lastrowid

def insert_fc_data(cur, df, city_id, fetch_id):
    
    hf = df[["day", "time", "temperature_2m", "visibility", "relative_humidity_2m", "precipitation_probability", "wind_speed_10m"]]
    hf.insert(0, 'city_id', city_id)
    hf.insert(0, 'fetch_id', fetch_id)

    rows = list(hf.itertuples(index=False, name=None))

    cur.executemany("""INSERT INTO hourly_forecast
                    (fetch_id, city_id, day_time, hour_time, temperature_2m, visibility,
                    relative_humidity_2m, precipitation_probability, wind_speed_10m)
                    VALUES (?,?,?,?,?,?,?,?,?)
                    """, rows
    )

    print(f'Inserted {hf.shape[0]} records into hourly_forecast table')

    df = (hf.drop(columns='time')
          .groupby(["fetch_id", "city_id", "day"], as_index=False)
          .mean()
    )

    rows = list(df.itertuples(index=False, name=None))

    cur.executemany("""INSERT INTO daily_forecast 
                    (fetch_id, city_id, day_time, temperature_2m, visibility,
                    relative_humidity_2m, precipitation_probability, wind_speed_10m)
                    VALUES (?,?,?,?,?,?,?,?)
                    """, rows
    )

    print(f'Inserted {df.shape[0]} records into daily_forecast table')

def main():

    try:
        with sqlite3.connect("./data/weather.db") as conn:
            schema = open("create_tables.sql", "r").read()
            conn.executescript(schema)

            print('Database tables created succesfully')

    except Exception as e:
        print(f"Error creating database tables: {e}")


    with open('config/cities.yaml', 'r') as file:
        data = yaml.safe_load(file)

    cities = data['cities']

    try:
        with sqlite3.connect("./data/weather.db", timeout=10) as con:

            for coord in cities:

                df, raw_text = fetch_weatherdata(*coord)

                cur = con.cursor()

                city = coord[0]

                print(f'Inserting data for {city}...')

                city_id = insert_cities(
                    cur,
                    tuple(df.loc[0,["city", "region", "latitude", "longitude"]])
                )

                fetch_id = insert_fc_fetch(cur, city_id, raw_text)

                insert_fc_data(cur, df, city_id, fetch_id)
                
                print(f'{city} loaded succesfully')

            print('All data loaded succesfully')

    except Exception as e:
        print(f"Error loading data to SQLite: {e}")
        raise

if __name__ == "__main__":
    main()

