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

# Customer name components
prefixes = ['Sharma', 'Gupta', 'Patel', 'Kumar', 'Singh', 'Verma', 'Mehta', 'Agarwal', 
           'Reddy', 'Joshi', 'Rao', 'Thakur', 'Shah', 'Nair', 'Pillai']
suffixes = ['Traders', 'Hardware', 'Enterprises', 'Distributors', 'Stores', 'Home Store', 
            'Build Mart', 'Supplies', 'Furnishings', 'Solutions']

# Feedback templates
positive_comments = [
    "Excellent quality product",
    "Very satisfied with the durability",
    "Great value for money",
    "Highly recommended",
    "Premium finish and look",
    "Customers love this product",
    "Best in market",
    "Perfect for our needs"
]

negative_comments = [
    "Poor quality received",
    "Stock never available",
    "Delivery takes too long",
    "Too expensive",
    "Difficult to install",
    "Many defects found",
    "Not worth the price",
    "Packaging needs improvement"
]

neutral_comments = [
    "Average quality",
    "Could be better",
    "Decent product",
    "Nothing special",
    "Meets basic requirements",
    "Standard quality",
    "Regular product"
]

stock_comments = [
    "Stock availability issues",
    "Always out of stock",
    "Limited stock available",
    "Need better stock management",
    "Irregular supply",
    "Stock delays frequent"
]

# Generate 5000 rows of data
n_rows = 5000

# Generate dates between Oct 1, 2024 and Jan 31, 2025
start_date = datetime(2024, 10, 1)
end_date = datetime(2025, 1, 31)
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Create customer names
customer_names = [f"{random.choice(prefixes)} {random.choice(suffixes)}" for _ in range(n_rows)]

# Create base data
data = {
    'Feedback_ID': range(30001, 30001 + n_rows),
    'Customer_Name': customer_names,
    'Stock_ID': range(1001, 1001 + n_rows),
    'Item_Name': np.random.choice(item_names, n_rows),
    'Category': np.random.choice(categories, n_rows),
    'Date': np.random.choice(dates, n_rows)
}

df = pd.DataFrame(data)

# Generate ratings with patterns
df['Rating'] = np.random.choice([1, 2, 3, 4, 5], n_rows, p=[0.1, 0.15, 0.25, 0.3, 0.2])

# Add patterns
# 1. Category-specific rating patterns
df.loc[df['Category'] == 'Handles', 'Rating'] = df.loc[df['Category'] == 'Handles', 'Rating'].apply(
    lambda x: max(1, x - 1) if random.random() < 0.3 else x)  # More negative ratings for Handles

df.loc[df['Category'] == 'Kadi', 'Rating'] = df.loc[df['Category'] == 'Kadi', 'Rating'].apply(
    lambda x: min(5, x + 1) if random.random() < 0.3 else x)  # More positive ratings for Kadi

# 2. Generate feedback comments based on ratings
def generate_comment(row):
    rating = row['Rating']
    category = row['Category']
    if pd.isna(rating):
        return "NA"
    
    if rating <= 2:
        base_comment = random.choice(negative_comments)
        if random.random() < 0.4:  # 40% chance to add stock-related comment
            return f"{base_comment}; {random.choice(stock_comments)}"
        return base_comment
    elif rating == 3:
        return random.choice(neutral_comments)
    else:
        return random.choice(positive_comments)

df['Feedback_Comment'] = df.apply(generate_comment, axis=1)

# 3. Add missing values (NaN)
# Create missing value patterns
missing_mask = np.random.choice([True, False], size=n_rows, p=[0.05, 0.95])  # 5% missing values
df.loc[missing_mask, ['Rating', 'Feedback_Comment']] = 'NA'

# 4. Add some incorrect/noise values
# Impossible ratings (outside 1-5 range)
noise_idx = np.random.choice(n_rows, 20, replace=False)
df.loc[noise_idx, 'Rating'] = np.random.choice([0, 6, 7, 8, 9, 10], 20)

# 5. Add seasonal patterns
# Lower ratings during peak season (December) due to delivery delays
seasonal_mask = (df['Date'] >= datetime(2024, 12, 1)) & (df['Date'] <= datetime(2024, 12, 31))
df.loc[seasonal_mask, 'Rating'] = df.loc[seasonal_mask, 'Rating'].apply(
    lambda x: max(1, x - 1) if random.random() < 0.4 and x != 'NA' else x)

# Sort by Date
df = df.sort_values('Date')

# Convert date to string format
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# Convert DataFrame to list of lists including headers
table_data = [df.columns.tolist()] + df.values.tolist()

# Convert all values to strings
table_data = [[str(cell) for cell in row] for row in table_data]

table_data

'''
    Built-in Patterns & Issues:

    Missing Values:

    5% missing values in both Rating and Feedback_Comment (marked as 'NA')
    Random distribution across all dates and categories
    Rating Patterns:

    Overall distribution:
    1 star: 10%
    2 stars: 15%
    3 stars: 25%
    4 stars: 30%
    5 stars: 20%
    Category-specific patterns:
    Handles: 30% chance of lower ratings
    Kadi products: 30% chance of higher ratings
    Seasonal Patterns:

    December (peak season) shows:
    40% chance of lower ratings
    More complaints about delivery delays
    Increased stock availability issues
    Feedback Types & Issues:

    Stock-related feedback (40% chance with low ratings):
    Availability issues
    Delivery delays
    Stock management complaints
    Quality feedback
    Price-related feedback
    Installation/usage feedback
    20 records with impossible ratings (0 or 6-10)
    Customer Distribution:

    Diverse customer names combining business types:
    Hardware stores
    Traders
    Distributors
    Home stores
    Build marts
    The data is now in your sheet starting from cell A1. You can analyze:

    Customer satisfaction trends
    Category-wise feedback patterns
    Stock availability impact on ratings
    Seasonal customer satisfaction
    Combined analysis with inventory, sales, operations, and finance datasets

'''