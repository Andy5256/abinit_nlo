#%%
import json
import numpy as np
import matplotlib.pyplot as plt
# take m.BiB3O6 as an example
chi = np.loadtxt('chi_compare_ref.dat')
# print(chi)
fig, ax1 = plt.subplots(figsize=(5,5))
chi_ab = abs(chi[:,0])
chi_gxm = abs(chi[:,1])
chi_fl = abs(chi[:,2])
chi_ref = abs(chi[:,3])
ax1.scatter(chi_ref, chi_fl, color='b', marker='x',s=25, label='fl')
ax1.scatter(chi_ref, chi_ab, color='r', marker='+',s=10, label='ab')
ax1.scatter(chi_ref, chi_gxm, color='g', marker='*',s=20, label='gxm')
plt.plot([0,140],[0,140], c='k')
plt.legend()
inset = plt.axes((.55, .2, .3, .3))
inset.plot([0,7], [0,7], color='k')
inset.scatter(chi_ref[-7:], chi_fl[-7:], color='b', marker='x',s=25)
inset.scatter(chi_ref[-7:], chi_ab[-7:], color='r', marker='+',s=10)
inset.scatter(chi_ref[-7:], chi_gxm[-7:], color='g', marker='*',s=20)
# plt.xlabel()
# inset.set_xscale('log')
# inset.set_yscale('log')
# plt.xlim(0,20)
plt.savefig('chi_compare_ref.png',dpi=300)
# %%
