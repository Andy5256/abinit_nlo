#%%
import matplotlib.pyplot as plt
import numpy as np

# a=str(12100)
b='11180_e0.1'
shift = 1.05
# b='1180'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
info1 = np.loadtxt('Im_chi_11.dat')
ax1.plot(info1[:,0], 2*info1[:,1], label='openmx*2')
abinit = np.loadtxt('optic_2_0001_0001-linopt_'+b+'.out')
ax1.plot(abinit[:118,0], abinit[:118,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im $\epsilon$${_r}$$^{xx}$')
ax1.legend()
plt.xlim(0,6)
# plt.ylim(0,50)
plt.title('AgGaS$_2$ Im_chi_11')
ax2 = plt.subplot(122)
info2 = np.loadtxt('Re_chi_11.dat')
ax2.plot(info2[:,0], shift + 2*info2[:,1], label='openmx*2+'+str(shift))
abinit = np.loadtxt('optic_2_0001_0001-linopt_'+b+'.out')
ax2.plot(abinit[119:235,0], abinit[119:235,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Re $\epsilon$${_r}$$^{xx}$')
ax2.legend()
plt.xlim(0,6)
# plt.ylim(-30,30)
plt.title('AgGaS$_2$ Re_chi_11')
ax2.legend()
plt.tight_layout()
plt.savefig('Chi_11_'+b+'_rescale_'+str(shift)+'.png')
# %%
