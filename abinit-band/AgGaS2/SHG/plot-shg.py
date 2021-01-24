#%%
import matplotlib.pyplot as plt
import numpy as np

# a='_tol0.0002'
a='_s216'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
openmx = np.loadtxt('ImSHG_312'+a+'.dat')
ax1.plot(openmx[:,0], openmx[:,1], label='openmx')
# abinit = np.loadtxt('ImSHG_111.dat')
# abinit = np.loadtxt('optic_2_0003_0001_0002-ChiTotIm'+a+'.out')
# ax1.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im SHG 312')
# plt.ylim(-300,300)
ax1.legend()
plt.xlim(0,6)
plt.title('AgGaS$_2$ Im_SHG_312')
ax2 = plt.subplot(122)
openmx = np.loadtxt('ReSHG_312'+a+'.dat')
ax2.plot(openmx[:,0], openmx[:,1], label='openmx')
# abinit = np.loadtxt('ReSHG_111.dat')
abinit = np.loadtxt('optic_2_0003_0001_0002-ChiTotRe'+a+'.out')
ax2.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('$\chi$$^{(2)}$$_{312}$')
ax2.legend()
plt.xlim(0,0.006)
# plt.ylim(-40,-30)
# plt.ylim(-300,300)
plt.title('AgGaS$_2$ Re_SHG_312')
ax2.legend()
plt.tight_layout()
plt.savefig('SHG_312'+a+'.png')
# %%
