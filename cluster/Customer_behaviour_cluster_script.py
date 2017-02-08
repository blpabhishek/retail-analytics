# -*- coding: utf-8 -*-
#chaniging directory to current
import os
path = "/Users/abhishek/Projects/retail-analytics/data"
os.chdir(path)

import pandas as pd
import numpy as np

Cust_behavior = pd.read_csv("customer_segmentation_v3.csv", sep = ',', index_col = 0)
Cust_behavior.shape
pd.DataFrame(list(Cust_behavior)).to_csv('varnames.csv')

########## ************ Pre clustering - ANALAYSIS *************
##### get what each of the categorical variable contains 
list(Cust_behavior.columns.values)
all_cat_vars =  ['AGE_DESC','MARITAL_STATUS_CODE','INCOME_DESC','HOMEOWNER_DESC','HH_COMP_DESC', 'HOUSEHOLD_SIZE_DESC', 'KID_CATEGORY_DESC']
All_frequencies = pd.DataFrame(Cust_behavior[all_cat_vars].apply(lambda x: x.value_counts()).T.stack())
All_frequencies.to_csv

#########*********Treating categorical variable.Converting to numeric to make them usable

#### Creating a new income variable for each customer which is equal to the mean of the income bucket the customer falls in 


def income_conversion (income) :
    if income == "Under 15K" :
        return 7500
    if income == "15-24K" :
        return 19500
    if income == "25-34K" :
        return 29500
    if income == "35-49K" :
        return 42000
    if income == "50-74K" :
        return 62000
    if income == "75-99K" :
        return 87000
    if income == "100-124K" :
        return 112000
    if income == "125-149K" :
        return 137000
    if income == "150-174K" :
        return 164000
    if income == "175-199K" :
        return 187000
    if income == "200-249K" :
        return 224500
    if income == "250K+" :
        return 250000
    return 62000  ### if income is not in any of these categories, replacing with most frequent category


def household_size_conversion(hh_size):
    if hh_size == "1" :
        return 1
    if hh_size == "2" :
        return 2
    if hh_size == "3" :
        return 3
    if hh_size == "4" :
        return 4
    if hh_size == "5+" :
        return 5
    return 2 ### if null return the category with max frequency

def age_conversion(age):
    if age == "19-24":
        return 21.5
    if age == "25-34":
        return 29.5
    if age == "35-44":
        return 39.5
    if age == "45-54":
        return 49.5
    if age == "55-64":
        return 59.5
    if age == "65+":
        return 65
    return 49.5  ### if null return the category with max frequency 


Cust_behavior['income_num'] = Cust_behavior['INCOME_DESC'].apply(income_conversion)
Cust_behavior['hh_size_num'] = Cust_behavior['HOUSEHOLD_SIZE_DESC'].apply(household_size_conversion)
Cust_behavior['age_num'] = Cust_behavior['AGE_DESC'].apply(age_conversion)






### Subset features to be used for clustering 
#features_to_use = ['National Product Count %','Private Product Count %','Average Product Price',
#'Total Product Sales','income_num','hh_size_num','age_num' ]
#df_cluster = Cust_behavior[features_to_use]

###### JUGAAAD _UNCLEAN. CHANGE LATER*********
drop_vars = all_cat_vars + ['household_key',"('household_key', '')","('SALES_VALUE', 'Total Sale')",'Total Count',
                            'Sale Value','Transction count']
df_cluster = Cust_behavior.drop(drop_vars, axis =1)


######### *********** Pre-processing data for Feeding into clusters  ********************
######## Feature scaling 
from sklearn import preprocessing
std_scale = preprocessing.StandardScaler().fit(df_cluster)
df_cluster_scaled = pd.DataFrame(std_scale.transform(df_cluster), columns = df_cluster.columns )

############# PCA implementation for reducing dimensions ************

from sklearn.decomposition import PCA as sklearnPCA
pca = sklearnPCA(n_components= 15)
df_with_components = pca.fit_transform(df_cluster_scaled)

#### This provides % of variance explained by each component (component 1 is highest then decreases...
#### Select till the point where cumulative sum < 95% .. Basically means till component number N, 95% of 
#### variance is explained 

eigenvalues = pd.DataFrame(pca.explained_variance_).to_csv("eigen_values.csv")


components =  pd.DataFrame(pca.components_)
##### can drop this intermediate table later 
#### Renaming columns to get the features names for each components 
components.columns = list(df_cluster_scaled)
components_final = pd.DataFrame(components).T.to_csv("components_in_depth.csv")

#### Plottting eigen values to see where to set the cut-off for number of components 
import matplotlib.pyplot as plt
#pca.fit(X_digits)
plt.figure(1, figsize=(4, 3))
plt.clf()
#plt.axes([.2, .2, .7, .7])
plt.plot(pca.explained_variance_, linewidth=2)
plt.axis('tight')
plt.xlabel('n_components')
plt.ylabel('explained_variance_')



#type(df_std)

######### *********** Creating clusters ********************
from sklearn import cluster
from sklearn.metrics import  silhouette_score

#### Using Silhoutter score to understand the right number of clusters. 
#### Higher the silhoutter score, better . So usually the k that maximizes Silhoutter score should be selected 
#### Read Below link for interpretation 
### http://stackoverflow.com/questions/23687247/efficient-k-means-evaluation-with-silhouette-score-in-sklearn
#### ***USe this only as a guideline as this method has it's limitations . Business Judgement takes precedence

for k in range(2, 11):
    kmeans = cluster.KMeans(n_clusters=k)
    kmeans.fit(df_cluster_scaled)
    label = kmeans.labels_
    sil_coeff = silhouette_score(df_cluster_scaled, label, metric='euclidean')
    print("k={}, The Silhouette Coefficient is {}".format(k, sil_coeff))

### Number of clusters 
k = 6
kmeans = cluster.KMeans(n_clusters=k)
kmeans.fit(df_cluster_scaled) ##3 fitting cluster

####### *********** Scoring and analyzing cluster ********************

###### caution ----Ideally a training sample needs to separated out for all this analysis . Not doing it because
### there are only 800 customers . Analyzing on Test sample 
### Assigning cluster to each row in the ORIGINAL data .  
Cust_behavior['labels'] = kmeans.predict(df_cluster_scaled)


#### Analyzing output .Seeing cluster profile by looking at average of important variables in each cluster
### This will provide us an idea of how each cluster is different 

Aggregations = {'National Product Count %' : 'mean',
                'Private Product Count %' : 'mean',
                'Average Product Price' : 'mean',
                'Total Product Sales' : 'mean',
                'household_key' : 'count',
                'income_num' : 'mean',
                'hh_size_num' : 'mean',
                'age_num' : 'mean'}

analyze_output = Cust_behavior.groupby(['labels']).agg(Aggregations).reset_index()

analyze_output.to_csv('analyze.csv')
#analyze_output


#### Explore how to make the output more readable in html ..