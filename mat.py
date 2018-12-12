from matplotlib import pyplot as plt
import numpy as np
from sklearn.preprocessing import normalize

c = 1000
t = 10
lmbda = (c/t)
# s = normalize(np.random.poisson(t, c))
s =  normalize(np.random.poisson(t, c).reshape(-1,10))
print(s)
print(lmbda)
print(len(s))
# print(np.linalg.norm(s))
# s = -np.log(1.0 - np.random.random_sample(1000)) / lmbda
# print(s)
# print(len(s))
# s = np.random.poisson(5, 10000)
# plt.plot(s)
# plt.
count, bins, ignored = plt.hist(s.reshape(-1), 100, density=True)
plt.show()
# plt.plot(conections_interval)
# plt.show()