import pandas as pd
import numpy as np
import random

def generate_nairobi_valuation_dataset(num_records=250):
    """
    Generates a realistic synthetic dataset mirroring Nairobi real estate 
    market dynamics (Rent, Price, Yield) for data science modeling.
    """
    print("--- Initializing Nairobi Real Estate Valuation Data Generator ---")
    
    random.seed(42)
    np.random.seed(42)
    
    locations = ['Kilimani', 'Westlands', 'Kileleshwa', 'Lavington', 'Karen', 'Langata', 'Parklands', 'South B']
    property_types = ['Apartment', 'Townhouse', 'Bungalow', 'Studio']
    
    data = []
    for i in range(num_records):
        loc = random.choice(locations)
        p_type = random.choice(property_types)
        
        # Base pricing logic mapped to Nairobi zones
        base_multiplier = {'Karen': 2.5, 'Lavington': 2.2, 'Westlands': 2.0, 'Kileleshwa': 1.8, 
                           'Kilimani': 1.7, 'Parklands': 1.4, 'Langata': 1.2, 'South B': 1.0}[loc]
        
        bedrooms = int(random.randint(1, 4)) if p_type != 'Studio' else 1
        sq_m = int(bedrooms * 35 + np.random.normal(10, 5))
        
        # Monthly rent in KES
        monthly_rent = int(sq_m * 70 * base_multiplier + np.random.normal(0, 5000))
        monthly_rent = max(25000, monthly_rent)
        
        # Market purchase price in KES (implied rental yield 6% - 10%)
        annual_yield_target = random.uniform(0.06, 0.095)
        purchase_price = int((monthly_rent * 12) / annual_yield_target)
        
        data.append({
            "property_id": f"NRB_PROP_{1000 + i}",
            "location": loc,
            "property_type": p_type,
            "bedrooms": bedrooms,
            "size_sqm": sq_m,
            "monthly_rent_kes": monthly_rent,
            "purchase_price_kes": purchase_price,
            "calculated_rental_yield_pct": round(((monthly_rent * 12) / purchase_price) * 100, 2)
        })

    df = pd.DataFrame(data)
    output_filename = "raw_nairobi_listings.csv"
    df.to_csv(output_filename, index=False)
    print(f"Successfully generated {num_records} structured real estate records in '{output_filename}'!")
    print("\nSample Data Preview:")
    print(df.head())
    return df

if __name__ == "__main__":
    generate_nairobi_valuation_dataset()