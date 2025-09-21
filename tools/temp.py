import numpy as np

f1 = np.linspace(0.1,1,9)
f2 = f1.copy()

for i in range(len(f1)):
    print(f1[i]*f2[i]/f1[i], f1[i]*(1-f2[i])/f1[i])