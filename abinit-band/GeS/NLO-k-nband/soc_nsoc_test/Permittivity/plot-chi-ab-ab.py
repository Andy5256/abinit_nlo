#%%
import matplotlib.pyplot as plt
import numpy as np

a='soc_e0.05'
b='nsoc_e0.05'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
info1 = np.loadtxt('optic_2_0001_0001-linopt_'+a+'.out')
ax1.plot(info1[:599,0], info1[:599,1], label='abinit'+a)
abinit = np.loadtxt('optic_2_0001_0001-linopt_'+b+'.out')
ax1.plot(abinit[:599,0], abinit[:599,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im $\epsilon$${_r}$$^{xx}$')
ax1.legend()
plt.xlim(0,6)
plt.title('1L-GeS Im_chi_11')
ax2 = plt.subplot(122)
info2 = np.loadtxt('optic_2_0001_0001-linopt_'+a+'.out')
ax2.plot(info2[599:1197,0], info2[599:1197,1], label='abinit'+a)
abinit = np.loadtxt('optic_2_0001_0001-linopt_'+b+'.out')
ax2.plot(abinit[599:1197,0], abinit[599:1197,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Re $\epsilon$${_r}$$^{xx}$')
ax2.legend()
plt.xlim(0,6)
plt.title('1L-GeS Re_chi_11')
ax2.legend()
plt.tight_layout()
plt.savefig('Chi_11_'+a+'_'+b+'.png')
# %%
