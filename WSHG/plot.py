#%%
import numpy as np
import matplotlib.pyplot as plt

info = np.loadtxt('ReSHG_312.dat')

plt.plot(info[0,:])
plt.xlim(25,75)

# %%
