#%%
import json
import numpy as np
import matplotlib.pyplot as plt

info = np.loadtxt('radius.dat')
plt.plot(info[:,1], 2*info[:,2], 'o-', c='b', label = 'This cal.')
plt.xlabel('total radius number')
plt.ylabel(r'$\chi$ (+sci.)(pm/V)')
plt.scatter(72, -24.08, c='r', label = 'Ref.')
plt.legend()
plt.savefig('radius.png')
# %%
