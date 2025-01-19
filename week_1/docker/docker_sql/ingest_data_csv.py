import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = "output.csv"  # Define the file name for the downloaded CSV


    #download the data
    os.system('wget {url} -O {csv_name} url')


    engine  = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{table_name}')
                            
    df_iter = pd.read_csv(csv_name, iterator=True , chunksize=100000)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists = 'replace')
    df.to_sql(name=table_name, con=engine, if_exists = 'append')

       while True:
        try:
            time_start = time()
            df = next(df_iter)

            # Processing the dataframe
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists = 'append')

            time_end = time()
        
            print('inserted new chunk....,took %.3f second' %(time_end-time_start))

        except StopIteration:
            print("All chunks have been processed.")
            break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV to postgres')

    parser.add_argument('--user', help='user name of postgres')
    parser.add_argument('--password', help='password of postgres')
    parser.add_argument('--host', help='host of postgres')
    parser.add_argument('--port', help='port of postgres')
    parser.add_argument('--db', help='database name of postgres')
    parser.add_argument('--table_name', help='table name of where we will write our results')
    parser.add_argument('--url', help='url of the csv file')


    args=parser.parse_args()
    
    main(args)





 