import os

import pandas as pd

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
transactionFrame = pd.read_csv('transaction_data.csv')
os.chdir(path)

product_and_sales = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
product_and_sales.columns = ['household_key', 'PRODUCT Count', 'Sales']
product_brand = productFrame[['PRODUCT_ID', 'BRAND']]
product_brand.columns = ['PRODUCT Count', 'BRAND']

product_sales_brand = pd.merge(product_and_sales, product_brand, on='PRODUCT Count').groupby(
    ['household_key', 'BRAND']).agg({"PRODUCT Count": 'count', "Sales": 'sum'}).unstack().reset_index()

brand_purchase_behaviour = product_sales_brand[['PRODUCT Count', 'Sales', 'household_key']]
brand_purchase_behaviour['Total Product Count'] = brand_purchase_behaviour['PRODUCT Count', 'National'] + \
                                                  brand_purchase_behaviour['PRODUCT Count', 'Private']
brand_purchase_behaviour['Total Product Sales'] = brand_purchase_behaviour['Sales', 'National'] + \
                                                  brand_purchase_behaviour['Sales', 'Private']

brand_purchase_behaviour['PRODUCT Count', 'National %'] = brand_purchase_behaviour['PRODUCT Count', 'National'] / \
                                                          brand_purchase_behaviour['Total Product Count']
brand_purchase_behaviour['PRODUCT Count', 'Private %'] = brand_purchase_behaviour['PRODUCT Count', 'Private'] / \
                                                         brand_purchase_behaviour['Total Product Count']
brand_purchase_behaviour['Sales', 'National %'] = brand_purchase_behaviour['Sales', 'National'] / \
                                                  brand_purchase_behaviour['Total Product Sales']
brand_purchase_behaviour['Sales', 'Private %'] = brand_purchase_behaviour['Sales', 'Private'] / \
                                                 brand_purchase_behaviour['Total Product Sales']
brand_purchase_behaviour['Average Product Price'] = brand_purchase_behaviour['Total Product Sales'] / \
                                                    brand_purchase_behaviour['Total Product Count']

brand_purchase_behaviour.columns = ['National Count', 'Private Count', 'National Sales', 'Private Sales',
                                    'household_key', 'Total Count', 'Total Sales', 'National Count %',
                                    'Private Count %', 'National Sales %', 'Private Sales %', 'Average Price']

brand_purchase_behaviour = brand_purchase_behaviour[
    ['household_key', 'National Count', 'National Count %', 'Private Count', 'Private Count %', 'Total Count',
     'National Sales', 'National Sales %', 'Private Sales', 'Private Sales %', 'Total Sales', 'Average Price']]

brand_purchase_behaviour.head()
