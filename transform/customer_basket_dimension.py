import os

import pandas as pd

from transform.utils import invalidProducts

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')
os.chdir(path)

transactionFrame = transactionFrame[-transactionFrame['PRODUCT_ID'].isin(invalidProducts)]

tdf1 = transactionFrame[['household_key', 'BASKET_ID', 'PRODUCT_ID']]

basket_behavior = tdf1.groupby(['household_key', 'BASKET_ID']).agg({"PRODUCT_ID": 'count'})
basket_behavior.columns = ['Item_Count']
basket_behavior.reset_index(inplace=True)

basket_behavior = basket_behavior.groupby(['household_key']).agg(
    {"BASKET_ID": 'count', "Item_Count": 'sum'}).reset_index()
basket_behavior.rename(columns={'BASKET_ID': 'Basket_Count'}, inplace=True)
basket_behavior['Avg_Basket_Items'] = basket_behavior['Item_Count'] / basket_behavior['Basket_Count']
basket_behavior.head(10)
