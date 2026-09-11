import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

#  Page Title
st.title("Nairobi Real Estate Valuation & Analytics")
st.write("Explore property prices, sizes, and market distributions across Nairobi.")

#  Connect to Database and Load Data
@st.cache_data
def load_data():
    try:
        
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
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        st.error(f"Error connecting to database or running query: {e}")
        return pd.DataFrame()

df = load_data()

#  Display Debug Status & Render Chart if Data Exists
st.write(f"**Debug Status:** Loaded **{len(df)}** records from database.")

if not df.empty:
    st.subheader("Property Size vs. Purchase Price")

    fig = px.scatter(
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
        title="Interactive Price vs. Size Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("The DataFrame is empty. Please check if your MySQL tables (`properties`, `locations`, `valuations`) contain data.")