import os

import pandas as pd

path = os.environ['data_path']
os.chdir(path + "/source")

productFrame = pd.read_csv('product.csv')
customerFrame = pd.read_csv('hh_demographic.csv')
transactionFrame = pd.read_csv('transaction_data.csv')
os.chdir(path)

Cust_behavior = pd.read_csv("customer_segmentation.csv", sep=',', index_col=0)
Cust_behavior.shape
pd.DataFrame(list(Cust_behavior)).to_csv('varnames.csv')

###### Prepare the data . Remove unnecessary variables ***********

### capturing all commodity and sub commodity vars
Commodity_vars = [c for c in Cust_behavior.columns if "Commodity" in c]

drop_vars = [
    'Department_MISC SALES TRAN',
    'Department_MISC. TRANS.',
    # 'Department_Total Sale',
    'National Count',
    'National Count %',
    'Private Count',
    'Private Count %',
    'Total Count',
    'National Sales',
    'Private Sales',
    'Private Sales %',
    'Retail Discount',
    'Coupon Discount',
    'Total Discount',
    'Days_Diff',
    'Days_Visit',
    'Transction count',
    'TypeA_participated',
    'TypeB_participated',
    'TypeC_participated',
    'TypeA_redeemed',
    'TypeB_redeemed',
    'TypeC_redeemed',
    'Item_Count',
    'Basket_Count'
]

df_cluster = Cust_behavior.drop(drop_vars, axis=1)

pd.DataFrame(df_cluster.describe(percentiles=[0, .10, .25, .50, .75, .90, .95, .99])).T.to_csv('percentiles.csv')

######### *********** Pre-processing data for Feeding into clusters  ********************
######## Feature scaling
from sklearn import preprocessing

std_scale = preprocessing.StandardScaler().fit(df_cluster)
df_cluster_scaled = pd.DataFrame(std_scale.transform(df_cluster), columns=df_cluster.columns)

############# PCA implementation for reducing dimensions ************

from sklearn.decomposition import PCA as sklearnPCA

pca = sklearnPCA(n_components=20)
df_clus_with_components = pca.fit_transform(df_cluster_scaled)

#### This provides % of variance explained by each component (component 1 is highest then decreases...
#### Select till the point where cumulative sum < 95% .. Basically means till component number N, 95% of
#### variance is explained

eigenvalues = pd.DataFrame(pca.explained_variance_).to_csv("eigen_values.csv")

######### *********** Creating clusters ********************
from sklearn import cluster
from sklearn.metrics import silhouette_score

#### Using Silhoutter score to understand the right number of clusters.
#### Higher the silhoutter score, better . So usually the k that maximizes Silhoutter score should be selected
#### Read Below link for interpretation
### http://stackoverflow.com/questions/23687247/efficient-k-means-evaluation-with-silhouette-score-in-sklearn
#### ***USe this only as a guideline as this method has it's limitations . Business Judgement takes precedence

for k in range(2, 11):
    kmeans = cluster.KMeans(n_clusters=k)
    kmeans.fit(df_clus_with_components)
    label = kmeans.labels_
    sil_coeff = silhouette_score(df_cluster_scaled, label, metric='euclidean')
    print("k={}, The Silhouette Coefficient is {}".format(k, sil_coeff))

### Number of clusters
k = 12
kmeans = cluster.KMeans(n_clusters=k)
kmeans.fit(df_clus_with_components)  ##3 fitting cluster

####### *********** Scoring and analyzing cluster ********************

###### caution ----Ideally a training sample needs to separated out for all this analysis . Not doing it because
### there are only 800 customers . Analyzing on Test sample
### Assigning cluster to each row in the ORIGINAL data .
df_cluster['cluster_labels'] = kmeans.predict(df_clus_with_components)

analyze_output = pd.DataFrame(df_cluster.groupby(['cluster_labels']).mean())
analyze_output['hh_count'] = df_cluster.groupby(['cluster_labels'])['household_key'].count()
analyze_output.T.to_csv('analyze.csv')
