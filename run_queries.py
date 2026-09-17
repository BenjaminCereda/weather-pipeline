import pandas as pd
import requests
import sqlite3
import datetime
import json
from pathlib import Path

def run_query(filepath):

    with sqlite3.connect("./data/weather.db") as conn:
        query = Path(filepath).read_text()
        df = pd.read_sql_query(query, conn)

    return df