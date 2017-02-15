import pandas as pd

from transform.customer_basket_dimension import basket_behavior
from transform.customer_basket_gap_dimension import basket_gap_behaviour
from transform.customer_brand_dimension import brand_purchase_behaviour
from transform.customer_commodity_dimension import commodity_purchase_behaviour
from transform.customer_department_dimension import department_purchase_behaviour
from transform.customer_sale_discount_dimension import discount_behaviour
from transform.promotion_behaviour import promotion_behavior

department_brand_purchase_behaviour = pd.merge(department_purchase_behaviour, brand_purchase_behaviour,
                                               on='household_key', how="outer").fillna(0)

commodity_department_brand_purchase_behaviour = pd.merge(department_brand_purchase_behaviour,
                                                         commodity_purchase_behaviour, on='household_key',
                                                         how="outer").fillna(0)

discount_department_brand_purchase_behaviour = pd.merge(commodity_department_brand_purchase_behaviour,
                                                        discount_behaviour, on='household_key',
                                                        how="outer").fillna(0)

basket_discount_department_brand_purchase_behaviour = pd.merge(
    discount_department_brand_purchase_behaviour, basket_behavior, on='household_key', how="outer"
).fillna(0)

gap_basket_discount_department_brand_purchase_behaviour = pd.merge(
    basket_discount_department_brand_purchase_behaviour, basket_gap_behaviour, on='household_key',
    how="outer"
).fillna(0)

promotion_gap_basket_discount_department_brand_purchase_behaviour = pd.merge(
    gap_basket_discount_department_brand_purchase_behaviour, promotion_behavior,
    on='household_key', how="outer")

customer_segmentation = promotion_gap_basket_discount_department_brand_purchase_behaviour

customer_segmentation.to_csv("customer_segmentation.csv")

percentileList = [.01, .02, .03, .05, .10, .20, .25, .30, .40, .50, .60, .70, .75, .80, .90, .95, .97, .98, .99]
customer_segmentation.head(10)
customer_segmentation.describe(percentiles=percentileList).to_csv("customer_segmentation_desc.csv")
