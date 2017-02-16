import os

import pandas as pd

from transform.utils import validDepartment, invalidProducts

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
transactionFrame = pd.read_csv('transaction_data.csv')

os.chdir(path)

valid_products = productFrame[-productFrame['PRODUCT_ID'].isin(invalidProducts)]
valid_products_in_valid_dept = valid_products[valid_products['DEPARTMENT'].isin(validDepartment)]

product_sales = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
product_department = valid_products_in_valid_dept[['PRODUCT_ID', 'DEPARTMENT']]

department_purchase_behaviour = pd.merge(product_sales, product_department, on='PRODUCT_ID', how='left')[
    ['household_key', 'DEPARTMENT', 'SALES_VALUE']].groupby(
    ['household_key', 'DEPARTMENT']).sum().unstack().reset_index().fillna(0)

department_purchase_behaviour['SALES_VALUE', 'Total Sale'] = department_purchase_behaviour['SALES_VALUE'].sum(axis=1)
department_purchase_behaviour = department_purchase_behaviour.set_index('household_key')['SALES_VALUE']
department_purchase_behaviour.rename(columns=lambda x: "Department_" + x, inplace=True)
department_purchase_behaviour = department_purchase_behaviour.div(
    department_purchase_behaviour['Department_Total Sale'], axis=0)
department_purchase_behaviour = department_purchase_behaviour.reset_index()
department_purchase_behaviour.drop('Department_Total Sale', axis=1, inplace=True)

print department_purchase_behaviour.head(10)
