import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Sample data
item_names = ['KH-1239', 'Cross Knob', 'Tower Bolt', 'Profile Handle', 'Key Stand', 
              'Sofa Leg', 'Main Door Handle', 'Khutti', 'Kadi Deluxe', 'Stainless Steel Knob',
              'Gold Plated Handle', 'Tower Bolt Premium', 'Economy Kadi', 'Antique Handle',
              'Designer Knob', 'Ultra Modern Handle', 'Brass Khutti', 'Decorative Kadi', 'Traditional Handle']

categories = ['Handles', 'Knob', 'Others', 'Accessories', 'Kadi']

suppliers = [
    'Shukla (Gujarat)',
    'Rahul (AP)',
    'Tiwary (Mumbai)',
    'Iyer (Chennai)',
    'Abdul Khan (Hyderabad)',
    'Venkatesh Gopal (Telangana)',
    'Amrit Singh (Punjab)',
    'Rajavardhan (Chennai)',
    'Hameesh (Kerala)',
    'Veeran Gowda (Karnataka)'
]

# Generate 5000 rows of data
n_rows = 5000

# Generate dates between Oct 1, 2024 and Jan 31, 2025
start_date = datetime(2024, 10, 1)
end_date = datetime(2025, 1, 31)
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Create base data
data = {
    'Stock_ID': range(1001, 1001 + n_rows),
    'Item_Name': np.random.choice(item_names, n_rows),
    'Category': np.random.choice(categories, n_rows),
    'Quantity_Available': np.random.randint(0, 1000, n_rows),
    'Restock_Threshold': np.random.choice([5, 10, 15, 20, 30, 50, 100], n_rows),
    'Purchase_Cost': np.random.randint(50, 1000, n_rows),
    'Supplier': np.random.choice(suppliers, n_rows),
    'Defective_Stock': np.random.randint(0, 10, n_rows),
    'Date_Added': np.random.choice(dates, n_rows)
}

df = pd.DataFrame(data)

# Add patterns and issues
# 1. Some items consistently low stock (potential supply chain issues)
low_stock_items = np.random.choice(item_names, 3)
df.loc[df['Item_Name'].isin(low_stock_items), 'Quantity_Available'] = df.loc[df['Item_Name'].isin(low_stock_items), 'Quantity_Available'] // 4

# 2. Some suppliers with higher defect rates
problematic_suppliers = np.random.choice(suppliers, 2)
df.loc[df['Supplier'].isin(problematic_suppliers), 'Defective_Stock'] = df.loc[df['Supplier'].isin(problematic_suppliers), 'Defective_Stock'] * 3

# 3. Seasonal patterns (higher stock levels for certain categories in certain months)
df.loc[(df['Category'] == 'Handles') & (df['Date_Added'] >= '2024-12-01'), 'Quantity_Available'] *= 2

# 4. Add outliers
# Extremely high purchase costs for some items
outlier_indices = np.random.choice(n_rows, 50, replace=False)
df.loc[outlier_indices, 'Purchase_Cost'] *= 5

# Extremely high quantities for some items
quantity_outlier_indices = np.random.choice(n_rows, 30, replace=False)
df.loc[quantity_outlier_indices, 'Quantity_Available'] *= 10

# 5. Add missing values (NaN)
# Randomly select cells to make NaN
for column in ['Quantity_Available', 'Purchase_Cost', 'Restock_Threshold', 'Defective_Stock']:
    mask = np.random.choice([True, False], size=n_rows, p=[0.02, 0.98])  # 2% missing values
    df.loc[mask, column] = np.nan

# 6. Add some incorrect/noise values
# Negative quantities (impossible in real scenario)
noise_indices = np.random.choice(n_rows, 20, replace=False)
df.loc[noise_indices, 'Quantity_Available'] = -df.loc[noise_indices, 'Quantity_Available']

# Some items with selling price lower than purchase cost (pricing errors)
pricing_error_indices = np.random.choice(n_rows, 40, replace=False)
df.loc[pricing_error_indices, 'Purchase_Cost'] = df.loc[pricing_error_indices, 'Purchase_Cost'] * 1.5

# Calculate Selling_Price (Purchase_Cost + random markup between 40% and 100%)
markups = np.random.uniform(1.4, 2.0, n_rows)
df['Selling_Price'] = (df['Purchase_Cost'] * markups).astype(float)  # Changed to float to accommodate NaN values

# Sort by Date_Added
df = df.sort_values('Date_Added')

# Convert date to string format
df['Date_Added'] = df['Date_Added'].dt.strftime('%Y-%m-%d')

# Reorder columns to match the original format
df = df[['Stock_ID', 'Item_Name', 'Category', 'Quantity_Available', 'Restock_Threshold',
         'Purchase_Cost', 'Selling_Price', 'Date_Added', 'Supplier', 'Defective_Stock']]

# Convert DataFrame to list of lists including headers
# Handle NaN values by converting them to empty strings
df = df.replace({np.nan: ''})
table_data = [df.columns.tolist()] + df.values.tolist()

# Convert all values to strings
table_data = [[str(cell) for cell in row] for row in table_data]

table_data

'''
    Built-in Patterns & Issues:

    Missing Values:

    2% missing values in Quantity_Available, Purchase_Cost, Restock_Threshold, and Defective_Stock columns
    Represented as empty cells in the dataset
    Supply Chain Patterns:

    Some items consistently show low stock levels
    Seasonal patterns (higher stock for Handles category during December-January)
    Some suppliers have higher defect rates than others
    Outliers & Errors:

    50 records with extremely high purchase costs (5x normal)
    30 records with unusually high quantities
    20 records with impossible negative quantities
    40 records with pricing inconsistencies (selling price < purchase cost)
    Stock Turnover Issues:

    Varied restock thresholds across products
    Some items showing stock levels below restock thresholds
    Seasonal variations in stock levels
    The data is now in your sheet starting from cell A1. You can proceed with:

    Data preprocessing to handle missing values and outliers
    Analysis of stock turnover patterns
    Supplier performance analysis
    Pricing anomaly detection
'''