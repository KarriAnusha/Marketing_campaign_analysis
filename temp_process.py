import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('marketing_data.csv')
dictionary = pd.read_csv('marketing_data_dictionary.csv')

# Clean data
clean = df.copy()
clean['Dt_Customer'] = pd.to_datetime(clean['Dt_Customer'], errors='coerce')
clean['Income'] = clean['Income'].replace(0, np.nan).fillna(clean['Income'].median())
clean['Age'] = 2015 - clean['Year_Birth']
clean.loc[clean['Age'] < 18, 'Age'] = np.nan
clean.loc[clean['Age'] > 100, 'Age'] = np.nan
clean['Age'] = clean['Age'].fillna(clean['Age'].median()).astype(int)

# Derive metrics
clean['Total_Spend'] = clean[['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].sum(axis=1)
clean['Total_Purchases'] = clean[['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']].sum(axis=1)
clean['Children'] = clean['Kidhome'] + clean['Teenhome']

# Segmentation
p90_spend = clean['Total_Spend'].quantile(0.9)
conditions = [
    clean['Income'] > 75000,
    clean['Age'] < 30,
    clean['Response'] == 1,
    clean['NumWebVisitsMonth'] > 5,
    clean['Children'] > 0,
    clean['Total_Spend'] > p90_spend,
]
choices = [
    'High Income',
    'Young Customer',
    'Campaign Responder',
    'High Web Engagement',
    'Family Customer',
    'High Spender',
]
clean['Primary_Segment'] = np.select(conditions, choices, default='Regular')

# Export
clean.to_csv('cleaned_marketing_data.csv', index=False)
print('Cleaned data exported to cleaned_marketing_data.csv')
print('Shape:', clean.shape)
print('Segments:', clean['Primary_Segment'].value_counts().to_dict())