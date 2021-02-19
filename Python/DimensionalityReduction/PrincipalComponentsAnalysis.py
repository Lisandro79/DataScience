import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

""" 
https://towardsdatascience.com/principal-component-analysis-pca-from-scratch-in-python-7f3e2a540c51 
"""

df = datasets.load_iris(as_frame=True)
fr = df.target.to_frame().astype(float) # add targets
df.data.insert(4, 'target', fr.iloc[:, 0].values, True)
df.data['target'] = df.data['target'].astype(str)
df.data['target'] =  df.data['target'].replace('0.0', 'setosa')
df.data['target'] =  df.data['target'].replace('1.0', 'versicolor')
df.data['target'] = df.data['target'].replace('2.0', 'virginica')

# Scale data
X_scaled = StandardScaler().fit_transform(df.data.iloc[:, 0:4].values)

# Covariance matrix
features = X_scaled.T
cov_matrix = np.cov(features)

# Eigendecomposition is a process that decomposes a square matrix into eigenvectors and eigenvalues.
# Eigenvectors are simple unit vectors, and eigenvalues are coefficients which give the magnitude to the eigenvectors.
values, vectors = np.linalg.eig(cov_matrix)

explained_variances = []
total_values = np.sum(values)
for i in range(len(values)):
    explained_variances.append(values[i] / total_values)
# print(explained_variances)

# Visualize
projected_1 = X_scaled.dot(vectors.T[0])
projected_2 = X_scaled.dot(vectors.T[1])
projected_3 = X_scaled.dot(vectors.T[2])

res = pd.DataFrame(projected_1, columns=['PC1'])
res['PC2'] = projected_2
res['PC3'] = projected_3
res['Y'] = df.data['target']
print(res.head())

# 2D Scatterplot
plt.figure(figsize=(10, 7))
sns.scatterplot(res['PC1'], res['PC2'], hue=res['Y'], s=200)
plt.show()

# 3D scatterplot
fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')
ax = Axes3D(fig)
sc = ax.scatter(xs=res['PC1'], ys=res['PC2'], zs=res['PC3'], s=40, c=fr.iloc[:, 0].values,
                marker='o', cmap='rainbow', alpha=1)
plt.show()
