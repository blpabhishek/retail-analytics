import os

import pandas as pd

from transform.utils import popularCommodity, invalidProducts

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')
os.chdir(path)

productFrame = productFrame[-productFrame['PRODUCT_ID'].isin(invalidProducts)]
productFrame = productFrame[productFrame['COMMODITY_DESC'].isin(popularCommodity)]

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'COMMODITY_DESC']]
pdf.columns = ['PRODUCT_ID', 'COMMODITY']

commodity_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID', how='left')[
    ['household_key', 'COMMODITY', 'SALES_VALUE']].groupby(['household_key', 'COMMODITY']).agg(
    {"SALES_VALUE": 'sum'}).unstack()
commodity_purchase_behaviour = commodity_purchase_behaviour.reset_index().fillna(0)
commodity_purchase_behaviour = commodity_purchase_behaviour.set_index('household_key')
commodity_purchase_behaviour = commodity_purchase_behaviour['SALES_VALUE']
commodity_purchase_behaviour['Total Sale'] = commodity_purchase_behaviour.sum(axis=1)
commodity_purchase_behaviour = commodity_purchase_behaviour.div(commodity_purchase_behaviour['Total Sale'], axis=0)
commodity_purchase_behaviour.drop('Total Sale', axis=1, inplace=True)
commodity_purchase_behaviour.rename(columns={'(CORP USE ONLY)': 'CORP USE ONLY'}, inplace=True)
commodity_purchase_behaviour.rename(columns=lambda x: "Commodity_" + x, inplace=True)
commodity_purchase_behaviour.reset_index(inplace=True)

print commodity_purchase_behaviour.head(10)
