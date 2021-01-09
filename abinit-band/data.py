#%%
import matplotlib.pyplot as plt
import numpy as np

# with open('data.dat') as f:
#     info = f.readline
info = np.loadtxt('k8.dat')
plt.plot(info[:,0], info[:,1], '-o')
# %%
