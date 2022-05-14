import numpy as np

data = np.random.normal(0, 1, 10000000)
measurements = np.cos(data)
print(np.std(measurements))
