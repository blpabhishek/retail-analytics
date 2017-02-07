import os

retval = os.getcwd()
path = os.environ['data_path']
os.chdir(path)
retval = os.getcwd()

import pandas as pd

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
tdf1.columns = ['household_key', 'PRODUCT Count', 'Sales']
pdf = productFrame[['PRODUCT_ID', 'BRAND']]
pdf.columns = ['PRODUCT Count', 'BRAND']

brand_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT Count') \
    .groupby(['household_key', 'BRAND']) \
    .agg({"PRODUCT Count": 'count', "Sales": 'sum'}).unstack()
brand_purchase_behaviour = brand_purchase_behaviour.reset_index()
brand_purchase_behaviour = brand_purchase_behaviour[['PRODUCT Count', 'Sales', 'household_key']]
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

# customer_brand_purchase_behaviour = pd.merge(customerFrame, brand_purchase_behaviour, on='household_key',how='left')


tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE', 'QUANTITY']]
pdf = productFrame[['PRODUCT_ID', 'DEPARTMENT']]

department_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID', how='left').groupby(
    ['household_key', 'DEPARTMENT']).agg({"SALES_VALUE": 'sum', "QUANTITY": 'sum'}).unstack()
department_purchase_behaviour = department_purchase_behaviour.reset_index().fillna(0)
department_purchase_behaviour = department_purchase_behaviour[['SALES_VALUE', 'QUANTITY', 'household_key']]
department_purchase_behaviour['SALES_VALUE', 'Total Sale'] = department_purchase_behaviour['SALES_VALUE'].sum(axis=1)
department_purchase_behaviour = department_purchase_behaviour[['household_key', 'SALES_VALUE', 'QUANTITY']]
department_purchase_behaviour.head(10)

department_brand_purchase_behaviour = pd.merge(department_purchase_behaviour, brand_purchase_behaviour,
                                               on='household_key', how='outer').fillna(0)
department_brand_purchase_behaviour.head(10)

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
commodity_purchase_behaviour = commodity_purchase_behaviour.reset_index()
commodity_purchase_behaviour.head(10)

commodity_department_brand_purchase_behaviour = pd.merge(department_brand_purchase_behaviour,
                                                         commodity_purchase_behaviour, on='household_key',
                                                         how='outer').fillna(0)
commodity_department_brand_purchase_behaviour.head(10)

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE']]
pdf = productFrame[['PRODUCT_ID', 'SUB_COMMODITY_DESC']]
pdf.columns = ['PRODUCT_ID', 'SUB_COMMODITY']

sub_commodity_purchase_behaviour = pd.merge(tdf1, pdf, on='PRODUCT_ID').groupby(['household_key', 'SUB_COMMODITY']).agg(
    {"SALES_VALUE": 'sum'}).unstack()
sub_commodity_purchase_behaviour = sub_commodity_purchase_behaviour.reset_index().fillna(0)
sub_commodity_purchase_behaviour.head(10)

sub_commodity_department_brand_purchase_behaviour = pd.merge(commodity_department_brand_purchase_behaviour,
                                                             sub_commodity_purchase_behaviour, on='household_key',
                                                             how='outer').fillna(0)
sub_commodity_department_brand_purchase_behaviour.head(10)

tdf1 = transactionFrame[['household_key', 'PRODUCT_ID', 'SALES_VALUE', 'RETAIL_DISC', 'COUPON_MATCH_DISC']]

discount_behaviour = transactionFrame.groupby(['household_key']).agg(
    {"SALES_VALUE": 'sum', "RETAIL_DISC": 'sum', "COUPON_MATCH_DISC": 'sum'})
discount_behaviour = discount_behaviour.reset_index().fillna(0)
discount_behaviour['TOTAL_DISC'] = discount_behaviour['RETAIL_DISC'] + discount_behaviour['COUPON_MATCH_DISC']
discount_behaviour['PERCENT_DISC'] = abs(discount_behaviour['TOTAL_DISC'] / discount_behaviour['SALES_VALUE'])
discount_behaviour.columns = ['household_key', 'Retail Discount', 'Sale Value', 'Coupon Discount', 'Total Discount',
                              'Discount Percentage']

discount_sub_commodity_department_brand_purchase_behaviour = pd.merge(sub_commodity_department_brand_purchase_behaviour,
                                                                      discount_behaviour, on='household_key',
                                                                      how='outer').fillna(0)
discount_sub_commodity_department_brand_purchase_behaviour.head(10)

tdf1 = transactionFrame[['household_key', 'BASKET_ID']]
basket_behavior = tdf1.groupby(['household_key']).agg({"BASKET_ID": 'count'}).reset_index()
basket_behavior.columns = ['household_key', 'Basket Count']
basket_behavior.head(10)

basket_discount_sub_commodity_department_brand_purchase_behaviour = pd.merge(
    discount_sub_commodity_department_brand_purchase_behaviour, basket_behavior, on='household_key',
    how='outer').fillna(0)
basket_discount_sub_commodity_department_brand_purchase_behaviour.head(10)

tdf1 = transactionFrame[['household_key', 'DAY']]
tdf1['Day_Diff'] = tdf1.groupby('household_key')['DAY'].transform(pd.Series.diff).fillna(0)
tdf1.sort_index(inplace=True)
tdf1 = tdf1[tdf1['Day_Diff'] > 0]
basket_gap_behaviour = tdf1.groupby('household_key').agg({"Day_Diff": 'sum', "household_key": 'count'})
basket_gap_behaviour.columns = ['Days_Diff', 'Days_Visit']
basket_gap_behaviour['Avg_Days'] = basket_gap_behaviour['Days_Diff'] / basket_gap_behaviour['Days_Visit']
basket_gap_behaviour = basket_gap_behaviour.reset_index()
basket_gap_behaviour.head(10)

gap_basket_discount_sub_commodity_department_brand_purchase_behaviour = pd.merge(
    basket_discount_sub_commodity_department_brand_purchase_behaviour, basket_gap_behaviour, on='household_key',
    how='outer').fillna(0)
gap_basket_discount_sub_commodity_department_brand_purchase_behaviour.head(10)

customer_segmentation = pd.merge(gap_basket_discount_sub_commodity_department_brand_purchase_behaviour, customerFrame,
                                 on='household_key', how='left')
print customer_segmentation.head(10)
