import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse

def main(params):
    # Extract parameters
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Connect to PostgreSQL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print("Connected to PostgreSQL database.")

    # Read Parquet file from URL in chunks
    print("Reading the Parquet file from URL in chunks...")
    chunk_size = 100000
    row_start = 0

    while True:
        try:
            # Load a chunk of data
            df = pd.read_parquet(url, engine="pyarrow").iloc[row_start:row_start + chunk_size]
            if df.empty:
                print("All chunks have been processed.")
                break

            # Process datetime columns if applicable
            if 'tpep_pickup_datetime' in df.columns and 'tpep_dropoff_datetime' in df.columns:
                df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
                df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

            # Insert data into PostgreSQL
            time_start = time()
            if row_start == 0:  # First chunk creates the table
                print(f"Creating table '{table_name}' and inserting the first chunk...")
                df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            time_end = time()

            print(f"Inserted rows {row_start} to {row_start + len(df)}, took {time_end - time_start:.3f} seconds")
            row_start += chunk_size

        except Exception as e:
            print(f"Error processing chunk: {e}")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet to PostgreSQL')

    parser.add_argument('--user', help='PostgreSQL username', required=True)
    parser.add_argument('--password', help='PostgreSQL password', required=True)
    parser.add_argument('--host', help='PostgreSQL host', required=True)
    parser.add_argument('--port', help='PostgreSQL port', required=True)
    parser.add_argument('--db', help='PostgreSQL database name', required=True)
    parser.add_argument('--table_name', help='Target table name', required=True)
    parser.add_argument('--url', help='Parquet file URL', required=True)

    args = parser.parse_args()
    main(args)
