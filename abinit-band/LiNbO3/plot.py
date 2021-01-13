#%%
import matplotlib.pyplot as plt
import numpy as np

info = np.loadtxt('333.dat')
plt.plot(info[:,1]/30, info[:,2], '-o', label = 'k5*5*5')
plt.xlabel('# of orbitals/# of occ')
plt.ylabel('|χ_{ij}^{(2)|}$(pm/V)')
plt.title('LiNbO$_3$ Static SHG 333')
plt.hlines(53.9, xmin=info[0,1]/30, xmax=info[-1,1]/30, colors='r', label = 'Reference', linestyles='--')
plt.hlines(11.5, xmin=info[0,1]/30, xmax=info[-1,1]/30, colors='k', label = 'openmx', linestyles='--')
plt.legend(loc= 'best', bbox_to_anchor=(0.5,0, 0.5,0.8))
plt.xlim(info[0,1]/30, info[-1,1]/30)
plt.savefig('LiNbO3_SHG333.png',dpi=1000)
# %%
