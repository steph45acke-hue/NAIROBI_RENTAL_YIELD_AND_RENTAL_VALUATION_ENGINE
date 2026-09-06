import pandas as pd
from sqlalchemy import create_engine
import mysql.connector


def migrate_data():
    print("---Starting 3NF Migration Pipeline ---")


    df = pd.read_csv("raw_nairobi_listings.csv")
    print(f"Loaded {len)df)} rows from raw_nairobi_listings.csv")


engine = create_engine("mysql+mysqlconnector://root:your_password@stephen0111301468/nairobi_real_estate")

locations_df = df[['location']].drop_duplicates().copy()
locations_df['county'] = df['county'] = 'Nairobi'
locations_df.rename(columns={'location':'sub_county'},inplace=True)


