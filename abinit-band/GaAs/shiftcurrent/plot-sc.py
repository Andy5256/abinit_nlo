#%%
import matplotlib.pyplot as plt
import numpy as np

a='_k200_e0.1'
plt.figure(figsize=(6,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(111)
openmx = np.loadtxt('shiftcond_123'+a+'.dat')
ax1.plot(openmx[:,0], -openmx[:,1], label='openmx')
# abinit = np.loadtxt('ImSHG_111.dat')
# abinit = np.loadtxt('optic_2_0001_0002_0002-ChiTotIm_'+a+'.out')
# ax1.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('$\delta$$_{123}$ ($\mu$A*V$^2$)')
ax1.legend()
plt.xlim(0,8)
plt.ylim(0,65)
plt.title('GaAs sc_123')
# ax2 = plt.subplot(122)
# openmx = np.loadtxt('shiftcond_123_k100.dat')
# ax2.plot(openmx[:,0], openmx[:,1], label='openmx')
# abinit = np.loadtxt('ReSHG_111.dat')
# abinit = np.loadtxt('optic_2_0001_0002_0002-ChiTotRe_'+a+'.out')
# ax2.plot(abinit[:,0], abinit[:,2], label='abinit')
# plt.xlabel('$\omega$ (eV)')
# plt.ylabel('$\delta$$_{123}$ ($\niu$A*V$^2$)')
# ax2.legend()
# plt.xlim(0,8)
# plt.ylim(-300,300)
# plt.title('GaAs sc_123')
# ax2.legend()
# plt.tight_layout()
plt.savefig('sc_123'+a+'.png')
# %%
import numpy as np
a=[1,2,3,4,5,6,7,8,9]
print(a)
a[::3,:]
# %%
