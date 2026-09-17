import pandas as pd
import sqlite3
import datetime
from pathlib import Path
import os

def main():

    checks = Path("./data_quality")

    with sqlite3.connect("./data/weather.db") as conn:

        for check in checks.glob("*.sql"):

            stmt = open(check, "r").read()

            df = pd.read_sql_query(stmt, conn)
            
            if not df.empty:
                raise ValueError(f"Query {os.path.basename(check)} returned the following faulty rows:\n {df}")
            else:
                print(f"✓ {os.path.basename(check)}")

if __name__ == "__main__":
    
    main()