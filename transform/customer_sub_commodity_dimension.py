import os

import pandas as pd

from transform.utils import invalidProducts, invalidDepartment

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')
os.chdir(path)

productFrame = productFrame[-productFrame['PRODUCT_ID'].isin(invalidProducts)]
productFrame = productFrame[-productFrame['DEPARTMENT'].isin(invalidDepartment)]

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'SUB_COMMODITY_DESC']]
pdf.columns = ['PRODUCT_ID', 'SUB_COMMODITY']

sub_commodity_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID', how='left')[
    ['household_key', 'SUB_COMMODITY', 'SALES_VALUE']].groupby(['household_key', 'SUB_COMMODITY']).agg(
    {"SALES_VALUE": 'sum'}).unstack()
sub_commodity_purchase_behaviour = sub_commodity_purchase_behaviour.reset_index().fillna(0)
sub_commodity_purchase_behaviour = sub_commodity_purchase_behaviour.set_index('household_key')
sub_commodity_purchase_behaviour = sub_commodity_purchase_behaviour['SALES_VALUE']
sub_commodity_purchase_behaviour.rename(columns=lambda x: "Sub_Commodity_" + x, inplace=True)
sub_commodity_purchase_behaviour.reset_index(inplace=True)

sub_commodity_purchase_behaviour.head(10)

# df_cluster = sub_commodity_purchase_behaviour['SALES_VALUE']
# percentileList = [.01, .02, .03, .05, .10, .20, .25, .30, .40, .50, .60, .70, .75, .80, .90, .95, .97, .98, .99]
# df_cluster.describe(percentiles=percentileList).head(10)
# df_cluster.describe(percentiles=percentileList).to_csv('out1.csv')
