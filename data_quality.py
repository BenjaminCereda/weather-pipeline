import pandas as pd
import sqlite3
import datetime
from pathlib import Path
import os
from db_con import get_connection

def main():

    checks = Path("./data_quality")

    with get_connection() as conn:

        with conn.cursor() as cur:

            for check in checks.glob("*.sql"):

                stmt = open(check, "r").read()

                cur.execute(stmt)

                result = cur.fetchall()

                if result:
                    raise ValueError(f"Query {os.path.basename(check)} returned the following faulty rows:\n {result}")
                else:
                    print(f"✓ {os.path.basename(check)}")

if __name__ == "__main__":
    
    main()