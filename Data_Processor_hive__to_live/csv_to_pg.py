import pandas as pd
from sqlalchemy import create_engine
import os


DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "postgres_db"
DB_PORT = "5432"

TABLE_NAME = "test_transactions" 

def use_to_sql_for_import(CSV_FILE_PATH):
    print("CSV NAME: ", CSV_FILE_PATH)
    try:
        if not os.path.exists(CSV_FILE_PATH):
            print(f"[CSV TO PG] Error: CSV file not found at '{CSV_FILE_PATH}'. Please update the path.")
            return

        df = pd.read_csv(CSV_FILE_PATH)
        df.columns = [i.split(".")[1] for i in df.columns]
        print("[CSV TO PG] CSV loaded into pandas DataFrame.")
        
        
        engine_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(engine_url)
        
        with engine.connect() as connection:
            print(f"[CSV TO PG] Successfully connected to PostgreSQL using SQLAlchemy.")

        df.to_sql(
            name=TABLE_NAME, 
            con=engine, 
            #if_exists='replace', # Options: 'fail', 'replace', 'append'
            if_exists="append",
            index=False,         
            chunksize=10000     
        )

        print(f"\n[CSV TO PG] Successfully created table '{TABLE_NAME}' and inserted {len(df)} rows.")

    except Exception as error:
        print(f"[CSV TO PG] Error during dynamic table creation/import: {error}")

if __name__ == "__main__":
    csv_list = ["transactions_offset_0_size_500000.csv","transactions_offset_500000_size_500000.csv", 
                "transactions_offset_1000000_size_500000.csv", "transactions_offset_1500000_size_500000.csv"
                "transactions_offset_2000000_size_500000.csv", "transactions_offset_2500000_size_500000.csv",
                 "transactions_offset_3000000_size_500000.csv", "transactions_offset_3500000_size_500000.csv" ]
    
    for i in csv_list:
        use_to_sql_for_import(i)


