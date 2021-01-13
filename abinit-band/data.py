#%%
import matplotlib.pyplot as plt
import numpy as np

# with open('data.dat') as f:
#     info = f.readline
info = np.loadtxt('k8.dat')
plt.plot(info[:,0]/44, -info[:,1], '-o', label = 'k8*8*8')
info = np.loadtxt('k9.dat')
plt.plot(info[:,0]/44, -info[:,1], '-o', label = 'k9*9*9')
k11 = np.loadtxt('k11.dat')
plt.plot(k11[:,0]/44, -k11[:,1], '-o', label = 'k11*11*11')
plt.xlabel('# of orbitals/# of occ')
plt.ylabel('$χ_{36}^{(2)}$(pm/V)')
plt.title('AgGaS$_2$ Static SHG 312')
plt.hlines(24.08, xmin=k11[0,0]/44, xmax=k11[-1,0]/44, colors='r', label = 'Reference', linestyles='--')
plt.hlines(34.21, xmin=k11[0,0]/44, xmax=k11[-1,0]/44, colors='k', label = 'openmx', linestyles='--')
plt.legend(loc= 'best', bbox_to_anchor=(0.5,0, 0.5,0.9))
plt.xlim(k11[0,0]/44, k11[-1,0]/44)
plt.savefig('AgGaS2_SHG_312.png',dpi=1000)
# %%
