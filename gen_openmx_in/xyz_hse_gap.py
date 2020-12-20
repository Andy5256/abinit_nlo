
#%%
import os
import sys
import json
import numpy as np
import pandas as pd
import pickle as pkl

with open("Ref_HSE_gap.json", "r") as f:
    str  = json.load(f)
# print(str["materials"][0]["mp_id"])
for i in range(14):
    json.dump(str["materials"][i], open("HSE_gap.json", "w"), indent=4)
    mp_id = str["materials"][i]["mp_id"]
    mid = str["materials"][i]["mid"]
    # print(mp)
    # os.system('mkdir %s' %mp)
    os.system('mv HSE_gap.json %s' %mid)
# %%
