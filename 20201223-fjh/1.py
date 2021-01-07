# %%
from xyz import XYZ_Client

xyz = XYZ_Client("w003.phys.tsinghua.edu.cn", 4000)
xyz.login("admin", "admin")

plans = xyz.work_table("plan")
for plan in plans:
    if plan["id"] == 253:
        break

mids = plan["mids"]

# %%
cals = xyz.search_calculation(mids, 6, "finish")
child_tids = [6, [[19, [0, 0]], [19, [0, 0]], 0]]

cals2 = []
for cal in cals:
    if cal["child_tids"] == child_tids:
        cals2.append((cal["mid"], cal["id"]))


# %%
for mid, calc_id in cals2:
    print("%8d %8d" % (mid, calc_id))
