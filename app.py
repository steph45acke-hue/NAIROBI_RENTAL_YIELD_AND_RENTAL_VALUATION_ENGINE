import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------
#  PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nairobi Real Estate Valuation & Analytics",
    page_icon="🏠",
    layout="wide"
)

# ---------------------------------------------------------
#  DATABASE CONNECTION & DATA LOADING
# ---------------------------------------------------------
@st.cache_resource
def get_db_engine():
    
    return create_engine("mysql+mysqlconnector://root:stephen0111301468@localhost/nairobi_real_estate")

@st.cache_data
def load_data():
    try:
        engine = get_db_engine()
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
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return pd.DataFrame()

# Load data first so it exists in memory
df = load_data()

# ---------------------------------------------------------
# 3. TRAIN ML MODEL CACHE FUNCTION
# ---------------------------------------------------------
@st.cache_resource
def train_model(data):
    if data.empty:
        return None, None
    
    # Clean data
    model_df = data.dropna(subset=['purchase_price_kes', 'size_sqm', 'bedrooms']).copy()
    model_df['monthly_rent_kes'] = model_df['monthly_rent_kes'].fillna(
        model_df.groupby(['location', 'property_type'])['monthly_rent_kes'].transform('median')
    )
    model_df['monthly_rent_kes'] = model_df['monthly_rent_kes'].fillna(model_df['monthly_rent_kes'].median())

    features_df = model_df[['bedrooms', 'size_sqm', 'monthly_rent_kes', 'property_type', 'location']]
    X = pd.get_dummies(features_df, drop_first=True).astype(float)
    y = model_df['purchase_price_kes']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    return rf_model, X.columns

# Train model using loaded dataframe df
model, model_columns = train_model(df)

# ---------------------------------------------------------
#  MAIN APP LAYOUT & NAVIGATION
# ---------------------------------------------------------
st.title("🏡 Nairobi Real Estate Valuation & Analytics Platform")
st.markdown("End-to-end data science system featuring a 3NF MySQL backend, Random Forest valuation engine, and interactive market analytics.")

tab1, tab2 = st.tabs(["📊 Market Analytics Dashboard", "🤖 AI Property Valuation Tool"])

# ---------------------------------------------------------
# TAB 1: PLOTLY MARKET ANALYTICS DASHBOARD
# ---------------------------------------------------------
with tab1:
    st.subheader("Interactive Nairobi Real Estate Market Insights")
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Properties Analyzed", f"{len(df):,}")
        col2.metric("Average Purchase Price", f"KES {df['purchase_price_kes'].mean():,.0f}")
        col3.metric("Average Monthly Rent", f"KES {df['monthly_rent_kes'].mean():,.0f}")
        
        st.markdown("---")
        
        # Interactive Scatter Plot: Size vs Price
        fig_scatter = px.scatter(
            df,
            x="size_sqm",
            y="purchase_price_kes",
            color="location",
            symbol="property_type",
            hover_data=["bedrooms", "monthly_rent_kes"],
            labels={
                "size_sqm": "Size (Square Meters)",
                "purchase_price_kes": "Purchase Price (KES)",
                "location": "Sub-County",
                "property_type": "Property Type"
            },
            title="Property Size vs. Purchase Price by Location"
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Bar Chart: Average Price by Location
        avg_price_loc = df.groupby("location")["purchase_price_kes"].mean().reset_index()
        fig_bar = px.bar(
            avg_price_loc,
            x="location",
            y="purchase_price_kes",
            color="location",
            title="Average Purchase Price Across Nairobi Sub-Counties",
            labels={"location": "Sub-County", "purchase_price_kes": "Average Price (KES)"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No data found. Please check your MySQL database connection.")

# ---------------------------------------------------------
# TAB 2: AI PROPERTY VALUATION TOOL
# ---------------------------------------------------------
with tab2:
    st.subheader("Predict Property Purchase Price")
    st.markdown("Use our trained Random Forest machine learning model to estimate property values based on structural specifications.")

    if model is not None and not df.empty:
        col_in1, col_in2 = st.columns(2)
        
        with col_in1:
            input_location = st.selectbox("Sub-County / Location", options=df['location'].unique())
            input_property_type = st.selectbox("Property Type", options=df['property_type'].unique())
            input_bedrooms = st.slider("Bedrooms", min_value=1, max_value=6, value=3)

        with col_in2:
            input_size = st.number_input("Size (Square Meters)", min_value=20.0, max_value=1000.0, value=120.0, step=5.0)
            input_rent = st.number_input("Estimated Monthly Rent (KES)", min_value=10000.0, max_value=1000000.0, value=75000.0, step=5000.0)

        if st.button("Calculate Estimated Valuation", type="primary"):
            input_data = pd.DataFrame(0, index=[0], columns=model_columns)
            
            if 'bedrooms' in input_data.columns: input_data['bedrooms'] = input_bedrooms
            if 'size_sqm' in input_data.columns: input_data['size_sqm'] = input_size
            if 'monthly_rent_kes' in input_data.columns: input_data['monthly_rent_kes'] = input_rent
            
            loc_col = f"location_{input_location}"
            if loc_col in input_data.columns:
                input_data[loc_col] = 1
                
            type_col = f"property_type_{input_property_type}"
            if type_col in input_data.columns:
                input_data[type_col] = 1

            predicted_price = model.predict(input_data)[0]
            
            st.success("Valuation Successful!")
            st.metric(label="Estimated Market Purchase Price", value=f"KES {predicted_price:,.2f}")
            
            implied_yield = (input_rent * 12) / predicted_price * 100
            st.info(f"**Implied Annual Rental Yield:** {implied_yield:.2f}%")
    else:
        st.warning("Model could not be trained due to missing data or database connectivity.")