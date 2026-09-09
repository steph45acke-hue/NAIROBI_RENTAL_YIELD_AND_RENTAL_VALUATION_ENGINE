import pandas as pd
import statsmodels.api as sm
from sqlalchemy import create_engine


def run_statistical_diagnostics():
    print("--- Connecting to 3NF Database for statistical Diagnostics ---")

    engine = create_engine("mysql+mysqlconnector://root:stephen0111301468@localhost/nairobi_real_estate")

    query = """
             SELECT
                p.property_id,
                l.sub_county AS location,
                p.property_type,
                p.bedrooms,
                p.size_sqm,
                v.monthly_rent_kes,
                v.purchase_price_kes
                FROM properties p
                JOIN locations  l ON p.location_id = l.location_id
                JOIN valuations v ON p.property_id = v.property_id;
                """
    df = pd.read_sql(query,con = engine)
    print(f"Loaded {len(df)} records for regression analysis.")
    
