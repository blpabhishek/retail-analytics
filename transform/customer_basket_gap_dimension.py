import os

retval = os.getcwd()
path = os.environ['data_path']
os.chdir(path)
retval = os.getcwd()

import pandas as pd

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')

transactionFrame.columns

tdf1 = transactionFrame[['household_key', 'DAY']]
tdf1['Day_Diff'] = tdf1.groupby('household_key')['DAY'].transform(pd.Series.diff).fillna(0)
tdf1.sort_index(inplace=True)
tdf1 = tdf1[tdf1['Day_Diff'] > 0]
basket_gap_behaviour = tdf1.groupby('household_key').agg({"Day_Diff": 'sum', "household_key": 'count'})
basket_gap_behaviour.columns = ['Days_Diff', 'Days_Visit']
basket_gap_behaviour['Avg_Days'] = basket_gap_behaviour['Days_Diff'] / basket_gap_behaviour['Days_Visit']
basket_gap_behaviour = basket_gap_behaviour.reset_index()
basket_gap_behaviour.head(10)

customer_basket_gap_behaviour = pd.merge(basket_gap_behaviour, customerFrame, on='household_key', how='left').fillna(0)
customer_basket_gap_behaviour.head(50)

customer_basket_gap_behaviour.to_csv("bucket_gap.csv")
