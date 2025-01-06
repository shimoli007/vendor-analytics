import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data
num_records = 1000

# Create vendor IDs (assuming 100 different vendors)
vendor_ids = [f'V{str(i).zfill(3)}' for i in range(1, 101)]

# Create product data
products = {
    'Maize': {'min_price': 45, 'max_price': 55},
    'Potatoes': {'min_price': 30, 'max_price': 40},
    'Tomatoes': {'min_price': 80, 'max_price': 100},
    'Onions': {'min_price': 60, 'max_price': 75},
    'Bananas': {'min_price': 25, 'max_price': 35},
    'Cabbage': {'min_price': 40, 'max_price': 50},
    'Rice': {'min_price': 110, 'max_price': 130}
}

# Create location data (common areas in Kenya)
locations = [
    'Nairobi CBD', 'Westlands', 'Kasarani', 'Kibera',
    'Eastleigh', 'Karen', 'Githurai', 'Zimmerman'
]

# Payment methods
payment_methods = ['Soko Loan', 'M-PESA', 'Cash', 'Bank Transfer']

# Generate random dates for the past 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
dates = [start_date + timedelta(days=x) for x in range(31)]

# Generate the data
data = {
    'vendor_id': np.random.choice(vendor_ids, num_records),
    'order_date': np.random.choice(dates, num_records),
    'product_name': np.random.choice(list(products.keys()), num_records),
    'quantity': np.random.randint(5, 100, num_records),
    'delivery_location': np.random.choice(locations, num_records),
    'payment_method': np.random.choice(payment_methods, num_records, 
                                     p=[0.3, 0.4, 0.2, 0.1])  # Weighted probabilities
}

# Calculate prices based on product
data['price'] = [np.random.uniform(products[product]['min_price'], 
                                 products[product]['max_price']) 
                 for product in data['product_name']]

# Create DataFrame
df = pd.DataFrame(data)

# Sort by date and vendor_id
df = df.sort_values(['order_date', 'vendor_id'])

# Save to CSV
df.to_csv('data/vendor_orders.csv', index=False)

print("Sample data has been generated and saved to 'data/vendor_orders.csv'")
print("\nFirst few records:")
print(df.head().to_string())

print("\nData Summary:")
print(f"Total Records: {len(df)}")
print(f"Unique Vendors: {df['vendor_id'].nunique()}")
print(f"Date Range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")