import pandas as pd
import requests
import sqlite3
import datetime
import json
from pathlib import Path
from db_con import get_connection

def run_query(filepath):

    with get_connection() as conn:
        query = Path(filepath).read_text()
        df = pd.read_sql_query(query, conn)

    return df