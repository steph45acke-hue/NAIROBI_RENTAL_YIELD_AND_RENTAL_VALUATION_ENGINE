import pandas as pd
from sqlalchemy import create_engine
import mysql.connector


def load_data_from_3nf():
    print("---Extracting data from 3NF MySQL Database---")

    engine = create_engine("mysql+mysqlconnector://root:stephen0111301468@localhost/nairobi_real_estate")
    
    query = """
            SELECT
                p.property_id,
                l.sub_county AS location,
                l.county,
                p.property_type,
                p.bedrooms,
                p.size_sqm,
                v.monthly_rent_kes,
                v.purchase_price_kes,
                v.calculated_rental_yield_pct
                FROM properties p
                JOIN locations l ON p.location_id = l.location_id
                JOIN valuations v ON p.property_id = v.property_id;
                """
    

    df = pd.read_sql(query,con=engine)
    print(f"Successfully extracted {len(df)} joined rows from MySQL.")
    return df
if __name__ == "__main__":
    df = load_data_from_3nf()
    print(df.head())

