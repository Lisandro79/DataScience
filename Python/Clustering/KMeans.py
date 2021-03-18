import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


# https://github.com/geodra/Articles/blob/master/K-Means_scratch.ipynb
def kmeans(X, k=3, max_iterations=100):
    '''
    X: multidimensional data
    k: number of clusters
    max_iterations: number of repetitions before clusters are established

    Steps:
    1. Convert data to numpy aray
    2. Pick indices of k random point without replacement
    3. Find class (P) of each data point using euclidean distance
    4. Stop when max_iteration are reached of P matrix doesn't change

    Return:
    np.array: containg class of each data point
    '''
    if isinstance(X, pd.DataFrame):
        X = X.values
    idx = np.random.choice(len(X), k, replace=False)
    centroids = X[idx, :]
    P = np.argmin(distance.cdist(X, centroids, 'euclidean'), axis=1)
    for _ in range(max_iterations):
        centroids = np.vstack([X[P == i, :].mean(axis=0) for i in range(k)])
        tmp = np.argmin(distance.cdist(X, centroids, 'euclidean'), axis=1)
        if np.array_equal(P, tmp):
            break
        P = tmp
    return P


df = pd.read_csv('datasets/cluster_validation_data.txt', sep=',', header=None)
df.head()

X = df.values
sc = StandardScaler()
sc.fit(X)
X = sc.transform(X)

P = kmeans(X)
assert len(df) == len(P)

# denormalize data
X = sc.inverse_transform(X)
fig = plt.figure(figsize=(10, 7))
plt.scatter(X[:, 0], X[:, 1], c=P)