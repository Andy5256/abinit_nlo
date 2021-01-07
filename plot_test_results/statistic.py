#%%
import json
import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt('statistic.dat')
plt.bar([10,20,30,40], data[:,1], leftwidth=8)
# %%
