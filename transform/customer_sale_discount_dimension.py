import os

import pandas as pd

retval = os.getcwd()
path = os.environ['data_path']
os.chdir(path)
retval = os.getcwd()

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE', 'RETAIL_DISC', 'COUPON_MATCH_DISC']]

discount_behaviour = transactionFrame.groupby(['household_key']).agg(
    {"SALES_VALUE": 'sum', "RETAIL_DISC": 'sum', "COUPON_MATCH_DISC": 'sum'})
discount_behaviour = discount_behaviour.reset_index().fillna(0)
discount_behaviour['TOTAL_DISC'] = discount_behaviour['RETAIL_DISC'] + discount_behaviour['COUPON_MATCH_DISC']
discount_behaviour['PERCENT_DISC'] = abs(discount_behaviour['TOTAL_DISC'] / discount_behaviour['SALES_VALUE'])
discount_behaviour.columns = ['household_key', 'Retail Discount', 'Sale Value', 'Coupon Discount', 'Total Discount',
                              'Discount Percentage']

customer_discount_behaviour = pd.merge(discount_behaviour, customerFrame, on='household_key', how='left').fillna(0)
customer_discount_behaviour.head(10)

customer_discount_behaviour.to_csv("discount.csv")

# cluster_fatures = ['Sale Value','Discount Percentage']
# df_cluster = customer_discount_behaviour[cluster_fatures]
# percentileList = [.01, .02, .03, .05, .10, .20, .25, .30, .40, .50, .60, .70, .75, .80, .90, .95, .97, .98, .99]
# df_cluster.describe(percentiles=percentileList).head(0)
