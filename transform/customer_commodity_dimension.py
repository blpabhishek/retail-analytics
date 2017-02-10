import os

import pandas as pd

from transform.utils import validCommodity

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')
os.chdir(path)

invalidProducts = [5126106, 5993055, 5978657, 5126087, 5993051, 5978650, 5978659, 6693056, 5993054, 5126088, 5126107,
                   5978649, 5977100, 5978656, 5978648]

invalidDepartment = ['CHARITABLE CONT', 'CNTRL/STORE SUP', 'DELI/SNACK BAR', 'ELECT &PLUMBING', 'GRO BAKERY', 'HBC',
                     'HOUSEWARES', 'MEAT-WHSE', 'PHARMACY SUPPLY', 'PHOTO', 'PORK', 'POSTAL CENTER', 'PROD-WHS',
                     'SALES', 'RX', 'TOYS', 'VIDEO', 'VIDEO RENTAL', 'AUTOMOTIVE', 'DAIRY DELI', 'GM MERCH EXP',
                     'PROD-WHS SALES']

validDepartment = ['DRUG GM', 'GROCERY', 'KIOSK-GAS', 'MEAT', 'MEAT-PCKGD', 'PRODUCE']
# validDepartment = ['PRODUCE']

productFrame = productFrame[-productFrame['PRODUCT_ID'].isin(invalidProducts)]
productFrame = productFrame[productFrame['COMMODITY_DESC'].isin(validCommodity)]

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'COMMODITY_DESC', 'DEPARTMENT']]
pdf.columns = ['PRODUCT_ID', 'COMMODITY', 'DEPARTMENT']

commodity_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID')[
    ['household_key', 'DEPARTMENT', 'COMMODITY', 'SALES_VALUE']].groupby(
    ['household_key', 'DEPARTMENT', 'COMMODITY']).agg(
    {"SALES_VALUE": 'sum'}).unstack()

commodity_purchase_behaviour = commodity_purchase_behaviour.fillna(0)
commodity_purchase_behaviour['Department_Total_Sale'] = commodity_purchase_behaviour.sum(axis=1)
commodity_purchase_behaviour = commodity_purchase_behaviour.div(commodity_purchase_behaviour['Department_Total_Sale'],
                                                                axis=0)
commodity_purchase_behaviour = commodity_purchase_behaviour['SALES_VALUE']
commodity_purchase_behaviour.rename(columns={'(CORP USE ONLY)': 'CORP USE ONLY'}, inplace=True)
commodity_purchase_behaviour.rename(columns=lambda x: "Commodity_" + x, inplace=True)

commodity_purchase_behaviour.reset_index(inplace=True)
commodity_purchase_behaviour.drop('DEPARTMENT', axis=1, inplace=True)

commodity_purchase_behaviour = commodity_purchase_behaviour.groupby('household_key').sum().reset_index()
print commodity_purchase_behaviour.shape

# print commodity_purchase_behaviour.head(10)
