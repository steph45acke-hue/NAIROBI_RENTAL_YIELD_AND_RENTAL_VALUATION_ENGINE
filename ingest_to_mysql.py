import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

def migrate_data():
    print("--- Starting 3NF Migration Pipeline ---")

    df = pd.read_csv("raw_nairobi_listings.csv")
    print(f"Loaded {len(df)} rows from raw_nairobi_listings.csv")

   
    engine = create_engine("mysql+mysqlconnector://root:stephen0111301468@localhost/nairobi_real_estate")

    locations_df = df[['location']].drop_duplicates().copy()
    locations_df['county'] = 'Nairobi'
    locations_df.rename(columns={'location': 'sub_county'}, inplace=True)

    locations_df.to_sql('locations', con=engine, if_exists='append', index=False)
    print("Locations table populated successfully.")

    loc_mapping_df = pd.read_sql("SELECT location_id, sub_county FROM locations", con=engine)
    df = df.merge(loc_mapping_df, left_on='location', right_on='sub_county', how='inner')

    properties_df = df[['property_id', 'location_id', 'property_type', 'bedrooms', 'size_sqm']].copy()
    properties_df.to_sql('properties', con=engine, if_exists='append', index=False)
    print("Properties table populated successfully.")

    valuations_df = df[['property_id', 'monthly_rent_kes', 'purchase_price_kes', 'calculated_rental_yield_pct']].copy()
    valuations_df.to_sql('valuations', con=engine, if_exists='append', index=False)
    print("Valuations table populated successfully.")

    print("--- Migration to 3NF MySQL Database Completed Successfully ---")

if __name__ == "__main__":
    migrate_data()