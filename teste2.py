import numpy as np
N = 3000
T = 300
lmbda = N/T
y = -np.log(1.0 - np.random.random_sample(int(N))) / lmbda
for i in range(len(y)):
    print(y[i])
print(np.average(y))
print(lmbda)
print(sum(y))