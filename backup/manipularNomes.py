import numpy as np

data = np.loadtxt('raparigas.csv',dtype=str,encoding="UTF-8")

for dat in data[0:30]:
    print(dat)
