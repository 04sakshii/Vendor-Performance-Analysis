!pip install sqlalchemy
import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time
logging.basicConfig(
    filename="logs/ingestion_db.log",  # Added folder path and file extension
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
engine = create_engine('sqlite:///inventory_v2.db')
def ingest_db(df, table_name, engine):
    # chunksize=10000 tells Python to upload 10,000 rows at a time so SQLite doesn't crash
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=10000)
def load_raw_data():
    start= time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv('data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
        end = time.time()
        total_time = (end - start)/60
        logging.info('----------------Ingestion Complete----------')
            
    logging.info(f'\nTotal Time Taken:  {total_time} minutes')
    

if __name__ == '__main__':
    load_raw_data()