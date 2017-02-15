import os

import pandas as pd

from transform.utils import validDepartment, invalidProducts

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')
os.chdir(path)

productFrame = productFrame[-productFrame['PRODUCT_ID'].isin(invalidProducts)]
productFrame = productFrame[productFrame['DEPARTMENT'].isin(validDepartment)]
tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'DEPARTMENT']]

department_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID', how='left')[
    ['household_key', 'DEPARTMENT', 'SALES_VALUE']].groupby(['household_key', 'DEPARTMENT']).sum().unstack()
department_purchase_behaviour = department_purchase_behaviour.reset_index().fillna(0)
department_purchase_behaviour['SALES_VALUE', 'Total Sale'] = department_purchase_behaviour['SALES_VALUE'].sum(axis=1)
department_purchase_behaviour.set_index('household_key', inplace=True)
department_purchase_behaviour = department_purchase_behaviour['SALES_VALUE']
department_purchase_behaviour.rename(columns=lambda x: "Department_" + x, inplace=True)
department_purchase_behaviour = department_purchase_behaviour.div(
    department_purchase_behaviour['Department_Total Sale'], axis=0)
department_purchase_behaviour.reset_index(inplace=True)
department_purchase_behaviour.drop('Department_Total Sale', axis=1, inplace=True)

department_purchase_behaviour.head(10)

# features_to_use = department_purchase_behaviour.columns
# df_cluster = customer_department_purchase_behaviour[features_to_use]
# df_cluster.drop([df_cluster.columns[0]], axis=1, inplace=True)

# percentileList = [.01, .02, .03, .05, .10, .20, .25, .30, .40, .50, .60, .70, .75, .80, .90, .95, .97, .98, .99]
# df_cluster.describe(percentiles=percentileList).transpose().to_csv('out1.csv')
