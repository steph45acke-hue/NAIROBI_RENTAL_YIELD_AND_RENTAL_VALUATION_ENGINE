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
            l.sub_county AS location,
            p.property_type,
            p.bedrooms,
            p.size_sqm,
            v.monthly_rent_kes,
            v.purchase_price_kes
        FROM properties p
        JOIN locations l ON p.location_id = l.location_id
        JOIN valuations v ON p.property_id = v.property_id;
"""


    df = pd.read_sql(query,con=engine)

    print(f"Loaded {len(df)} records for machine learning.")

    df = df.dropna(subset=['purchase_price_kes','size_sqm','bedrooms'])

    df['monthly_rent_kes'] = df['monthly_rent_kes'].fillna(
        df.groupby(['location','property_type'])['monthly_rent_kes'].transform('median')
    )


    df['monthly_rent_kes'] = df['monthly_rent_kes'].fillna(df['monthly_rent_kes'].median())


    features_df = df[['bedrooms','size_sqm','monthly_rent_kes','property_type','location']]

    x = pd.get_dummies(features_df,drop_first = True)

    x= x.astype(float)

    y = df['purchase_price_kes']

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 42)

    print(f"Training set: {len(x_train)} properties | Testing set:{len(x_test)}")
    print("Training Random Forest Regressor...")


    rf_model = RandomForestRegressor(n_estimators = 100,random_state = 42)
    rf_model.fit(x_train,y_train)

    y_pred = rf_model.predict(x_test)

    r2 = r2_score(y_test,y_pred)

    mae = mean_absolute_error(y_test,y_pred)

    rmse = np.sqrt(mean_squared_error(y_test,y_pred))
    

    print("\n" + "="*80)
    print("RANDOM FOREST MODEL PERFORMANCE EVALUATION")
    print("="*80)


    print(f"R-Squared (Accuracy Score): {r2:.4f}")
    print(f"Mean Absolute Error (MAE):  KES {mae:,.2f}")
    print(f"Root Mean Squared Error:    KES {rmse:,.2f}")


    importances = rf_model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': x.columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)


    print("\nTop 5 Price-Driving Features:")
    print(feature_importance_df.head(5).to_string(index=False))
    print("="*80)

if __name__ == "__main__":
    train_property_price_model()

