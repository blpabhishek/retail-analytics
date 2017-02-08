# -*- coding: utf-8 -*-
# changing directory to current
import os

path = os.environ['data_path']
os.chdir(path)

import pandas as pd

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')

campaign_desc = pd.read_csv('campaign_desc.csv')
campaign_table = pd.read_csv('campaign_table.csv')

coupon_redempt_table = pd.read_csv('coupon_redempt.csv')
coupon_table = pd.read_csv('coupon.csv')

campaign_details = pd.merge(campaign_table, campaign_desc)
campaign_details.head()

included_in_a_campaign = campaign_details.groupby(['household_key', 'DESCRIPTION']).agg(
    {'CAMPAIGN': 'count'}).reset_index()
included_in_a_campaign.head()
grouped_by_campaign = included_in_a_campaign.pivot_table(index='household_key', columns='DESCRIPTION',
                                                         values='CAMPAIGN').fillna(0).reset_index()

grouped_by_campaign['Total Campaign Participated'] = grouped_by_campaign['TypeA'] + grouped_by_campaign['TypeB'] + \
                                                     grouped_by_campaign['TypeC']
grouped_by_campaign.head()

redeemed_coupons_count = coupon_redempt_table.groupby(['household_key']).agg({'COUPON_UPC': 'count'}).reset_index()
redeemed_coupons_count.head()

coupon_redempt_table = pd.read_csv('coupon_redempt.csv')

redemption_by_campaign_type = coupon_redempt_table.merge(campaign_details, how="left").groupby(
    ['household_key', 'DESCRIPTION']).agg({'CAMPAIGN': 'count'}).reset_index()

redemption_by_campaign_type.head()

redemption_per_customer_per_type = redemption_by_campaign_type.pivot_table(index='household_key', columns='DESCRIPTION',
                                                                           values='CAMPAIGN').fillna(0).reset_index()

redemption_per_customer_per_type['Total_redemption'] = redemption_per_customer_per_type['TypeA'] + \
                                                       redemption_per_customer_per_type['TypeB'] + \
                                                       redemption_per_customer_per_type['TypeC']

redemption_per_customer_per_type.head()

all_unique_customer = transactionFrame.groupby(['household_key']).agg({'household_key': 'count'})
all_unique_customer.columns = ['Transction count']
all_unique_customer = all_unique_customer.reset_index()
all_unique_customer.head()

promotion_behavior_of_redemeed_customer = grouped_by_campaign.merge(redemption_per_customer_per_type,
                                                                    on="household_key",
                                                                    suffixes=['_participated', '_redeemed'])

promotion_behavior_of_all = all_unique_customer.merge(promotion_behavior_of_redemeed_customer, on="household_key",
                                                      how="left").fillna('0')

promotion_behavior_of_all.head()
