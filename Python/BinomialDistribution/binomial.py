import numpy as np
from scipy.stats import binom
import math
from matplotlib import pyplot as plt

n = 7
p = .6
k = np.arange(0, 8)

binomial = binom.pmf(k, n, p)
print(binomial)


f, ax = figure()
plt.plot(binomial, 'o')

plt.show()