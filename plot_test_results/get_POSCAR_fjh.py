#%%
import os
import json
import numpy as np
import pandas as pd
str = np.loadtxt('1.txt',dtype=int)
# print(str)
for i in range(30):
    cid = str[i,1]
    mid = str[i,0]
    # print(cid)
    os.system('cp ../%s/POSCAR POSCAR_%s' %(cid, mid))
    # json.dump(str["materials"][i], open("HSE_gap.json", "w"), indent=4)
    # mp_id = str["materials"][i]["mp_id"]
    # mid = str["materials"][i]["mid"]
    # # print(mp)
    # # os.system('mkdir %s' %mp)
    # os.system('mv HSE_gap.json %s' %mid)
# %%
