import numpy as np

data = np.loadtxt('raparigas_rapazes_small.csv',dtype=str,encoding="UTF-8", delimiter=",")
dataNew = []
for dat in data[:,0]:
    valueNew = []
    for i in range(0,len(dat)):
        valueNew.append(ord(dat[i]))
    dataNew.append(valueNew)

for dat in dataNew:
    print(dat)