import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import shap

def load_data_from_3nf():
    print("--- Extracting Data from 3NF MySQL Database ---")
    
    
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
    
   
    df = pd.read_sql(query, con=engine)
    print(f"Successfully extracted {len(df)} joined rows from MySQL.")
    return df

def train_and_explain_model():
   
    df = load_data_from_3nf()
   
    features_df = df.drop(columns=['property_id', 'county', 'monthly_rent_kes', 'purchase_price_kes', 'calculated_rental_yield_pct'])
    
  
    X = pd.get_dummies(features_df, drop_first=True)
    y = df['purchase_price_kes']
    
   
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training model on {len(X_train)} properties...")
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    

    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    
    print(f"Model Evaluation -> R² Score: {r2:.4f} | Mean Absolute Error: KES {mae:,.2f}")
    
    
    print("--- Generating SHAP Model Explanations ---")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    print("SHAP analysis generated successfully. Feature impact calculations complete.")

if __name__ == "__main__":
    train_and_explain_model()