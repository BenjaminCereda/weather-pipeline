import pandas as pd
import sqlite3
import datetime
import fetch_weather_data
import data_quality

if __name__ == "__main__":

    print("Starting pipeline...")

    print("1. Fetching weather data")

    fetch_weather_data.main()

    print("2. Running data quality checks")

    data_quality.main()

    print("Pipeline completed succesfully")



