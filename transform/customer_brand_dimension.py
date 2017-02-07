import os

import pandas as pd
retval = os.getcwd()
path = os.environ['data_path']
os.chdir( path )
retval = os.getcwd()
# read data for product, customer and transaction
productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
tdf1.columns = ['household_key', 'PRODUCT Count', 'Sales']
pdf = productFrame[['PRODUCT_ID', 'BRAND']]
pdf.columns = ['PRODUCT Count', 'BRAND']

brand_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT Count') \
    .groupby(['household_key', 'BRAND']) \
    .agg({"PRODUCT Count": 'count', "Sales": 'sum'}).unstack()
brand_purchase_behaviour = brand_purchase_behaviour.reset_index()
brand_purchase_behaviour = brand_purchase_behaviour[['PRODUCT Count', 'Sales', 'household_key']]
brand_purchase_behaviour['Total Product Count'] = brand_purchase_behaviour['PRODUCT Count', 'National'] + brand_purchase_behaviour['PRODUCT Count', 'Private']
brand_purchase_behaviour['Total Product Sales'] = brand_purchase_behaviour['Sales', 'National'] + brand_purchase_behaviour['Sales', 'Private']

brand_purchase_behaviour['PRODUCT Count', 'National %'] = brand_purchase_behaviour['PRODUCT Count', 'National'] / brand_purchase_behaviour['Total Product Count']
brand_purchase_behaviour['PRODUCT Count', 'Private %'] = brand_purchase_behaviour['PRODUCT Count', 'Private'] / brand_purchase_behaviour['Total Product Count']
brand_purchase_behaviour['Sales', 'National %'] = brand_purchase_behaviour['Sales', 'National'] / brand_purchase_behaviour['Total Product Sales']
brand_purchase_behaviour['Sales', 'Private %'] = brand_purchase_behaviour['Sales', 'Private'] / brand_purchase_behaviour['Total Product Sales']
brand_purchase_behaviour['Average Product Price'] = brand_purchase_behaviour['Total Product Sales'] / brand_purchase_behaviour['Total Product Count']

brand_purchase_behaviour.columns = ['National Count', 'Private Count', 'National Sales', 'Private Sales','household_key', 'Total Count', 'Total Sales','National Count %',
                                    'Private Count %', 'National Sales %', 'Private Sales %','Average Price']

brand_purchase_behaviour = brand_purchase_behaviour[['household_key', 'National Count', 'National Count %','Private Count', 'Private Count %', 'Total Count',
                                                     'National Sales', 'National Sales %', 'Private Sales','Private Sales %', 'Total Sales', 'Average Price']]

brand_purchase_behaviour.head()

customer_brand_purchase_behaviour = pd.merge(customerFrame, brand_purchase_behaviour, on='household_key')
customer_brand_purchase_behaviour.to_csv('customer_brand_spend_behaviour.csv')


