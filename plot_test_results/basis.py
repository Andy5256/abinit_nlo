#%%
import json
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('basis.dat')
x = data[:,1]
y = data[:,2]
plt.plot(x/84, y*2, 'o-', c='b', label = 'This cal.')
plt.xlabel('#orbitals/#states')
plt.ylabel(r'$\chi$ (+sci.)(pm/V)')
plt.scatter(308/84, -24.08, c='r', label = 'Ref.')
plt.legend()
plt.savefig('basis.png')
# plt.xlim(0,20)

