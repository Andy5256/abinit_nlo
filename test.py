try:
    from sdk.xyz import XYZ_Client
except:
    import sys
    sys.path.append(".")
    from sdk.xyz import XYZ_Client

xyz = XYZ_Client("localhost", 4567)

xyz.login("admin", "admin")

mids = []
for i in range(10):
    mid = xyz.insert_material("test-%02d" % (i,), "test", {"0": "./Gemfile"})
    mids.append(mid)

mset_id = xyz.insert_mset("test-mset")
xyz.add_to_mset("test-mset", mids)
mset_id2 = xyz.insert_mset("test-1")
xyz.add_to_mset("test-1", mids[0:2])


cid = xyz.insert_code(1, "echo a > a", {"input": [], "output": ["a"]})
tid = xyz.insert_task(cid, "test-echo", "--", "config", True)

# a <- (b, c), b <- (d, e), c <- (e, 0), d <- (), e <- (0)
cid = xyz.insert_code(1, "echo a > a", {"input": ["b", "c"], "output": ["a"]})
a = xyz.insert_task(cid, "a", "a", "a <- b, c", True)

cid = xyz.insert_code(1, "echo b > b", {"input": ["d", "e"], "output": ["b"]})
b = xyz.insert_task(cid, "b", "b", "b <- d, e", True)

cid = xyz.insert_code(
    1, "echo c > c", {"input": ["e", "self.0"], "output": ["c"]})
c = xyz.insert_task(cid, "c", "c", "c <- e, 0", True)

cid = xyz.insert_code(1, "echo d > d", {"input": [], "output": ["d"]})
d = xyz.insert_task(cid, "d", "d", "d <- empty()", True)

cid = xyz.insert_code(1, "echo e > e", {"input": ["self.0"], "output": ["e"]})
e = xyz.insert_task(cid, "e", "e", "e <- 0", True)

tree_id = xyz.insert_tree(
    "tree-test",
    [a, b, c, d, e, e, 0, 0, 0],
    [[0, [1, 2]], [1, [3, 4]], [2, [5, 6]], [3, []], [4, [7]], [5, [8]]],
)
# -------------------------------------------------------------------
# or use reduced tids / tree_map, like:
# -------------------------------------------------------------------
# tree_id = xyz.insert_tree(
#     "tree-test",
#     [a, b, c, d, e, e],
#     [[0, [1, 2]], [1, [3, 4]], [2, [5, None]], [4, [None]]], [5, [None]]],
# )
# -------------------------------------------------------------------

pid = xyz.insert_plan("test-plan", mset_id2, tree_id, 1)

xyz.plan_set_script(pid, 1)

# xyz.plan_set_active(pid, True, True)
# calcs = xyz.search_calculation(mids, a, "__all__")
ctree_id = xyz.insert_tree("tree_c", [4, 6, 0], [[0, [1, 2]], [1, [2]]])
xyz.insert_tree(
    "complex_tree",
    [2, 3, -ctree_id, 5, 6, 0],
    [[0, [1, 2]], [1, [3, 4]], [3, []], [4, [5]]],
)
