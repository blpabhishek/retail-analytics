import os

import pandas as pd

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

productFrame = productFrame[-productFrame['PRODUCT_ID'].isin(invalidProducts)]
productFrame = productFrame[-productFrame['DEPARTMENT'].isin(invalidDepartment)]

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'QUANTITY', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'COMMODITY_DESC']]
pdf.columns = ['PRODUCT_ID', 'COMMODITY']

commodity_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID', how='left').groupby(
    ['household_key', 'COMMODITY']).agg({"SALES_VALUE": 'sum', "QUANTITY": 'sum'}).unstack()
commodity_purchase_behaviour = commodity_purchase_behaviour.reset_index().fillna(0)
commodity_purchase_behaviour = commodity_purchase_behaviour.set_index('household_key')
commodity_purchase_behaviour.head(10)

commodity_purchase_behaviour['QUANTITY', 'BABY FOODS'] = commodity_purchase_behaviour['QUANTITY', 'BABY FOODS'] + \
                                                         commodity_purchase_behaviour['QUANTITY', 'BABYFOOD']
commodity_purchase_behaviour['SALES_VALUE', 'BABY FOODS'] = commodity_purchase_behaviour['SALES_VALUE', 'BABY FOODS'] + \
                                                            commodity_purchase_behaviour['SALES_VALUE', 'BABYFOOD']
tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'COMMODITY_DESC']]
pdf.columns = ['PRODUCT_ID', 'COMMODITY']

commodity_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID', how='left')[
    ['household_key', 'COMMODITY', 'SALES_VALUE']].groupby(['household_key', 'COMMODITY']).agg(
    {"SALES_VALUE": 'sum'}).unstack()
commodity_purchase_behaviour = commodity_purchase_behaviour.reset_index().fillna(0)
commodity_purchase_behaviour = commodity_purchase_behaviour.set_index('household_key')
commodity_purchase_behaviour = commodity_purchase_behaviour['SALES_VALUE']
commodity_purchase_behaviour['BABY FOODS'] = commodity_purchase_behaviour['BABY FOODS'] + commodity_purchase_behaviour[
    'BABYFOOD']
commodity_purchase_behaviour.rename(columns={'(CORP USE ONLY)': 'CORP USE ONLY'}, inplace=True)
commodity_purchase_behaviour.rename(columns=lambda x: "Commodity_" + x, inplace=True)
commodity_purchase_behaviour.reset_index(inplace=True)


