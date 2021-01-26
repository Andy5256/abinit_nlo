#%%
import matplotlib.pyplot as plt
import numpy as np

# a='_tol0.0002'
a='_s0_e0.1'
b='_11180_s0_e0.1'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
openmx = np.loadtxt('ImSHG_312'+a+'.dat')
ax1.plot(openmx[:,0], openmx[:,1], label='openmx')
# abinit = np.loadtxt('ImSHG_111.dat')
abinit = np.loadtxt('optic_2_0003_0001_0002-ChiTotIm'+b+'.out')
ax1.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('$\chi$$^{(2)}$(pm/V)')
# plt.ylim(-300,300)
ax1.legend()
plt.xlim(0,6)
plt.title('AgGaS$_2$ Im_SHG_312')
ax2 = plt.subplot(122)
openmx = np.loadtxt('ReSHG_312'+a+'.dat')
ax2.plot(openmx[:,0], openmx[:,1], label='openmx')
# abinit = np.loadtxt('ReSHG_111.dat')
abinit = np.loadtxt('optic_2_0003_0001_0002-ChiTotRe'+b+'.out')
ax2.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('$\chi$$^{(2)}$(pm/V)')
ax2.legend()
plt.xlim(0,6)
# plt.ylim(-40,-30)
# plt.ylim(-300,300)
plt.title('AgGaS$_2$ Re_SHG_312')
ax2.legend()
plt.tight_layout()
plt.savefig('SHG_312_compare.png')
# %%

# %%
