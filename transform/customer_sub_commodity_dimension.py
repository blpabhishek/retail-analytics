import os

import pandas as pd

retval = os.getcwd()
path = os.environ['data_path']
os.chdir(path)
retval = os.getcwd()

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')

invalidProducts = [5126106, 5993055, 5978657, 5126087, 5993051, 5978650, 5978659, 6693056, 5993054, 5126088, 5126107,
                   5978649, 5977100, 5978656, 5978648]

invalidDepartment = ['CHARITABLE CONT', 'CNTRL/STORE SUP', 'DELI/SNACK BAR', 'ELECT &PLUMBING', 'GRO BAKERY', 'HBC',
                     'HOUSEWARES', 'MEAT-WHSE', 'PHARMACY SUPPLY', 'PHOTO', 'PORK', 'POSTAL CENTER', 'PROD-WHS',
                     'SALES', 'RX', 'TOYS', 'VIDEO', 'VIDEO RENTAL', 'AUTOMOTIVE', 'DAIRY DELI', 'GM MERCH EXP',
                     'PROD-WHS SALES']

productFrame = productFrame[-productFrame['PRODUCT_ID'].isin(invalidProducts)]
productFrame = productFrame[-productFrame['DEPARTMENT'].isin(invalidDepartment)]

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'SUB_COMMODITY_DESC']]
pdf.columns = ['PRODUCT_ID', 'SUB_COMMODITY']

sub_commodity_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID').groupby(['household_key', 'SUB_COMMODITY']).agg(
    {"SALES_VALUE": 'sum'}).unstack()
sub_commodity_purchase_behaviour = sub_commodity_purchase_behaviour.reset_index().fillna(0)
sub_commodity_purchase_behaviour.head(10)

# df_cluster = sub_commodity_purchase_behaviour['SALES_VALUE']
# percentileList = [.01, .02, .03, .05, .10, .20, .25, .30, .40, .50, .60, .70, .75, .80, .90, .95, .97, .98, .99]
# df_cluster.describe(percentiles=percentileList).head(10)
# df_cluster.describe(percentiles=percentileList).to_csv('out1.csv')
