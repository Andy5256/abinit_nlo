#%%
import matplotlib.pyplot as plt
import numpy as np

info = np.loadtxt('222.dat')
plt.plot(info[12:27,1]/30, -info[12:27,2], '-o', label = 'k5*5*5')
plt.plot(info[28:33,1]/30, -info[28:33,2], '-o', label = 'k8*8*8')
plt.plot(info[:5,1]/30, -info[:5,2], '-o', label = 'k11*11*11')
plt.xlabel('# of orbitals/# of occ')
plt.ylabel('|χ_{ij}^{(2)|}$(pm/V)')
plt.title('BiB$_3$O$_6$ Static SHG 222')
plt.hlines(10.28, xmin=info[12,1]/30, xmax=info[27,1]/30, colors='r', label = 'Reference', linestyles='--')
plt.hlines(10.00, xmin=info[12,1]/30, xmax=info[27,1]/30, colors='k', label = 'openmx', linestyles='--')
plt.legend(loc= 'best', bbox_to_anchor=(0.5,0, 0.5,0.4))
plt.xlim(info[12,1]/30, info[27,1]/30)
plt.savefig('BiB3O6_SHG222.png',dpi=1000)
# %%
