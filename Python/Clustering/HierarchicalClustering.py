import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering


def find_cluster(data, n_clusters):
    labels = []
    return labels


customer_data = pd.read_csv('./Shopping-data.csv')
data = customer_data.iloc[:, 3:5].values

f = plt.figure(figsize=(10, 7))
plt.title('Customer Dendrogram')
dend = shc.dendrogram(shc.linkage(data, method='ward'))
plt.close(f)

cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
cluster.fit_predict(data)

plt.scatter(data[:, 0], data[:, 1], c=cluster.labels_, cmap='rainbow')
plt.show()
