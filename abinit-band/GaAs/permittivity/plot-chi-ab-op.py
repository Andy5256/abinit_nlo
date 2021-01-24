#%%
import matplotlib.pyplot as plt
import numpy as np

# a=str(12100)
b='1780'
# b='1180'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
info1 = np.loadtxt('Im_chi_11.dat')
ax1.plot(info1[:,0], info1[:,1], label='openmx')
abinit = np.loadtxt('optic_2_0001_0001-linopt_'+b+'.out')
ax1.plot(abinit[:798,0], abinit[:798,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im $\epsilon$${_r}$$^{xx}$')
ax1.legend()
plt.xlim(0,8)
# plt.ylim(0,50)
plt.title('GaAs Im_chi_11')
ax2 = plt.subplot(122)
info2 = np.loadtxt('Re_chi_11.dat')
ax2.plot(info2[:,0], info2[:,1], label='openmx')
abinit = np.loadtxt('optic_2_0001_0001-linopt_'+b+'.out')
ax2.plot(abinit[799:1597,0], abinit[799:1597,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Re $\epsilon$${_r}$$^{xx}$')
ax2.legend()
plt.xlim(0,8)
# plt.ylim(-30,30)
plt.title('GaAs Re_chi_11')
ax2.legend()
plt.tight_layout()
plt.savefig('Chi_11_'+b+'.png')
# %%
