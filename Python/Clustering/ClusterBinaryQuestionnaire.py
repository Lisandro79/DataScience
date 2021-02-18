print(__doc__)

from sklearn.cluster import KMeans
from kmodes.kmodes import KModes
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import random


def find_clusters(X, n_clusters, rseed=42):
    # 1. Randomly choose clusters
    # rng = np.random.RandomState(rseed)
    # i = rng.permutation(X.shape[0])[:n_clusters]
    # centers = X[i]
    initial_centers = np.random.rand(n_clusters, 5)

    while True:
        # 2a. Assign labels based on closest center
        # Find indexes (argmin) of closest centers, then assign cluster label to each sample
        distances = euclidean_distances(X, initial_centers)
        labels = distances.argmin(axis=1)

        # 2b. Find new centers from means of points
        new_centers = np.array([X[labels == i].mean(0) if X[labels == i].any() else initial_centers[i]
                                for i in range(n_clusters)])

        # 2c. Check for convergence
        if np.all(initial_centers == new_centers):
            break
        initial_centers = new_centers

    return initial_centers, labels


# Create a dataset of 10,000 binary questionnaires of 5 binary responses each
number_possible_responses = 32
responses = np.arange(0, number_possible_responses)
bits = 5
result = (((responses[:, None] & (1 << np.arange(bits)))) > 0).astype(float)

# tuple (samples, )
selected_responses = tuple(random.choices(responses, k=10000))

# ndarray (samples, number of questions)
dataset = []
for resp in selected_responses:
    dataset.append(result[resp])

dataset = np.array(dataset)

# Test a measure of distance between the responses in the questionnaire

# Compare clustering algorithms
n_clusters = 32

# K-Means by hand
centers, labels = find_clusters(dataset, number_possible_responses)
X_embedded = TSNE(n_components=2).fit_transform(centers)
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=np.arange(0, n_clusters), s=50, cmap='viridis')

# K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=24).fit(dataset)
kmeans.predict(dataset)
X_embedded = TSNE(n_components=2).fit_transform(kmeans.cluster_centers_)
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=np.arange(0, n_clusters), s=50, cmap='viridis')

# K-Modes
km_cao = KModes(n_clusters=n_clusters, init="Cao", n_init=1, verbose=1)
fitClusters_cao = km_cao.fit_predict(dataset)
X_embedded = TSNE(n_components=2).fit_transform(km_cao.cluster_centroids_)
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=np.arange(0, n_clusters), s=50, cmap='viridis')

print('ciao')
