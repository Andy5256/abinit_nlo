#%%
import numpy as np
import matplotlib.pyplot as plt

info = np.loadtxt('ReSHG_123.dat')

plt.plot(info[0,:], 'o-')
plt.xlim(0,75)
plt.xlabel('Band Index')
plt.ylabel('$χ_{ij}^{(2)}$(pm/V)')
plt.savefig('AgGaS2_ReSHG_123_bandidx_shg.png',dpi=500)

# %%
