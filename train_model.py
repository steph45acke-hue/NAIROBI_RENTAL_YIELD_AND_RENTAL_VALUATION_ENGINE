import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

def train_property_price_model():
    print("---Connecting to 3NF Database for Machine Learning Training ---")

    engine = create_engine("mysql+mysqlconnector://root:stephen0111301468@localhost/nairobi_real_estate")

    query = """
        SELECT
            p.property_id,
            l.sub_county AS location
            p.property_type
            p.bedrooms,
            p.size_sqm,
            v.monthly_rent_kes,
            v.purchase_price_kes
        FROM properties p
        JOIN locations l ON p.location_id = l.location_id
        JOIN valuations v ON p.property_id = v.property;
        """


    df = pd.read_sql(query,con=engine)

    print(f"Loaded {len(df)} records for machine learning.")

    df = df.dropna(subset=['purchase_price_kes','size_sqm','bedrooms'])
    
