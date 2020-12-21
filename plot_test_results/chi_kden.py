#%%
import json
import numpy as np
import matplotlib.pyplot as plt
# take m.BiB3O6 as an example
chi = np.loadtxt('mp-76734.dat')
# print(chi)
x = chi[:,0]
y = chi[:,1]
plt.plot(x, y)
plt.xlim(0,20)
plt.savefig('mp-76734.png')
# %%
