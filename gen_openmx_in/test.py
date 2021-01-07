#%%
import json
a = {}
with open('a.json', 'r') as frp:
    a  = json.load(frp)
# print(a['aaa'][1])
b = a.get('ccc', 80)
print(b)
print('hi')
print("hey")
# %%