import os

retval = os.getcwd()
path = os.environ['data_path']
os.chdir(path)
retval = os.getcwd()

import pandas as pd

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')

# transactionFrame.columns
tdf1 = transactionFrame[['household_key', 'BASKET_ID']]
basket_behavior = tdf1.groupby(['household_key']).agg({"BASKET_ID": 'count'}).reset_index()
basket_behavior.columns = ['household_key', 'Basket Count']
basket_behavior.head(10)

# cluster_fatures = ['Sale Value','Discount Percentage']
# df_cluster = customer_discount_behaviour[cluster_fatures]
# percentileList = [.01, .02, .03, .05, .10, .20, .25, .30, .40, .50, .60, .70, .75, .80, .90, .95, .97, .98, .99]
# df_cluster.describe(percentiles=percentileList).head(0)
