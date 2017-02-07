# -*- coding: utf-8 -*-
# chaniging directory to current
import os

from transform.utils import *

retval = os.getcwd()
path = os.environ['data_path']
os.chdir(path)
retval = os.getcwd()

import pandas as pd

Cust_behavior = pd.read_csv("customer_department_spend_behaviour.csv", sep=',', index_col=0)

# Pre clustering - ANALAYSIS
# get what each of the categorical variable contains
list(Cust_behavior.columns.values)
all_cat_vars = ['AGE_DESC', 'MARITAL_STATUS_CODE', 'INCOME_DESC', 'HOMEOWNER_DESC', 'HH_COMP_DESC',
                'HOUSEHOLD_SIZE_DESC', 'KID_CATEGORY_DESC']
All_frequencies = pd.DataFrame(Cust_behavior[all_cat_vars].apply(lambda x: x.value_counts()).T.stack())
All_frequencies.to_csv


Cust_behavior['income_num'] = Cust_behavior['INCOME_DESC'].apply(income_conversion)
Cust_behavior['hh_size_num'] = Cust_behavior['HOUSEHOLD_SIZE_DESC'].apply(household_size_conversion)
Cust_behavior['age_num'] = Cust_behavior['AGE_DESC'].apply(age_conversion)

# Subset features to be used for clustering
features_to_use = ['CHEF SHOPPE', 'COSMETICS', 'COUP/STR & MFG', 'DELI', 'DRUG GM',
                   'FLORAL', 'FROZEN GROCERY', 'GARDEN CENTER', 'GROCERY', 'KIOSK-GAS', 'MEAT', 'MEAT-PCKGD',
                   'MISC SALES TRAN', 'MISC. TRANS.', 'NUTRITION', 'PASTRY', 'PRODUCE', 'RESTAURANT', 'SALAD BAR',
                   'SEAFOOD', 'SEAFOOD-PCKGD', 'SPIRITS', 'TRAVEL & LEISUR', 'age_num', 'hh_size_num', 'income_num']
df_cluster = Cust_behavior[features_to_use]

# Pre-processing data for Feeding into clusters
from sklearn import preprocessing

std_scale = preprocessing.StandardScaler().fit(df_cluster)
df_cluster_scaled = pd.DataFrame(std_scale.transform(df_cluster), columns=df_cluster.columns)

# type(df_std)

# Creating clusters
from sklearn import cluster
from sklearn.metrics import silhouette_score

# Using Silhoutter score to understand the right number of clusters.
# Higher the silhoutter score, better . So usually the k that maximizes Silhoutter score should be selected
# Read Below link for interpretation
# http://stackoverflow.com/questions/23687247/efficient-k-means-evaluation-with-silhouette-score-in-sklearn
# USe this only as a guideline as this method has it's limitations . Business Judgement takes precedence

for k in range(2, 11):
    kmeans = cluster.KMeans(n_clusters=k)
    kmeans.fit(df_cluster_scaled)
    label = kmeans.labels_
    sil_coeff = silhouette_score(df_cluster_scaled, label, metric='euclidean')
    print("k={}, The Silhouette Coefficient is {}".format(k, sil_coeff))

# Number of clusters
k = 6
kmeans = cluster.KMeans(n_clusters=k)
kmeans.fit(df_cluster_scaled)  # fitting cluster

# Scoring and analyzing cluster

# caution ----Ideally a training sample needs to separated out for all this analysis . Not doing it because
# there are only 800 customers . Analyzing on Test sample
# Assigning cluster to each row in the ORIGINAL data .
Cust_behavior['labels'] = kmeans.predict(df_cluster_scaled)

# Analyzing output .Seeing cluster profile by looking at average of important variables in each cluster
# This will provide us an idea of how each cluster is different

Aggregations = {'CHEF SHOPPE': 'mean',
                'COSMETICS': 'mean',
                'COUP/STR & MFG': 'mean',
                'DELI': 'mean',
                'DRUG GM': 'mean',
                'FLORAL': 'mean',
                'FROZEN GROCERY': 'mean',
                'GARDEN CENTER': 'mean',
                'GROCERY': 'mean',
                'KIOSK-GAS': 'mean',
                'MEAT': 'mean',
                'MEAT-PCKGD': 'mean',
                'MISC SALES TRAN': 'mean',
                'MISC. TRANS.': 'mean',
                'NUTRITION': 'mean',
                'PASTRY': 'mean',
                'PRODUCE': 'mean',
                'RESTAURANT': 'mean',
                'SALAD BAR': 'mean',
                'SEAFOOD': 'mean',
                'SEAFOOD-PCKGD': 'mean',
                'SPIRITS': 'mean',
                'TRAVEL & LEISUR': 'mean',
                'age_num': 'mean',
                'hh_size_num': 'mean',
                'income_num': 'mean'}

analyze_output = Cust_behavior.groupby(['labels']).agg(Aggregations).transpose()
analyze_output.to_csv('out1.csv')


#### Explore how to make the output more readable in html ..
