import pandas as pd
import statsmodels.api as sm
from sqlalchemy import create_engine


def run_statistical_diagnostics():
    print("--- Connecting to 3NF Database for statistical Diagnostics ---")


    #connecting to my sql database

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
 
    features_df = df[['bedrooms', 'size_sqm', 'monthly_rent_kes', 'property_type', 'location']]

    x = pd.get_dummies(features_df,drop_first = True)
    x= x.astype(float)

    y = df['purchase_price_kes']

    x_with_const = sm.add_constant(x)

    ols_model = sm.OLS(y, x_with_const).fit()

    print("\n" + "="*80)
    print("OLS REGRESSION & HYPOTHESIS TESTING DIAGNOSTIC REPORT")
    print("="*80)
    print(ols_model.summary())
    print("="*80)
    
if __name__ == "__main__":
    run_statistical_diagnostics()