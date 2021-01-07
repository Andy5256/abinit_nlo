import requests
import json
from functools import wraps


def api_def(function):
    @wraps(function)
    def wrapper(self, *args, **kw_args):
        var_names = function.__code__.co_varnames[1:]
        vars = dict(zip(var_names, args))
        vars.update(kw_args)
        ret = function(self, **vars)
        if ret is not None:
            for key, value in ret.items():
                if value is None:
                    vars.pop(key)
                else:
                    vars[key] = value

        return self.api_run(function.__name__, vars)

    return wrapper


class XYZ_Client:
    def __init__(self, url="localhost", port=4567, debug=False):
        self.url = "http://%s:%d" % (url, port)
        self.api_version = "v3"
        self.debug = debug

    def api_run(self, api_name, post_data):
        url = self.url + "/api/" + self.api_version + "/" + api_name

        files = None
        if "files" in post_data.keys():
            if type(post_data["files"]) == dict:
                files = post_data["files"]
                post_data.pop("files")

        if self.debug:
            print(post_data)

        if self.api_version == "v0":
            r = requests.post(url, post_data, files=files)
        if self.api_version == "v1":
            r = self.sess.post(url, post_data, files=files)
        if self.api_version == "v2":
            post_data["token"] = self.token
            r = requests.post(url, post_data, files=files)
        if self.api_version == "v3":
            r = requests.post(url, post_data, files=files)

        try:
            return r.json()
        except ValueError:
            return None

    def login(self, username=None, password=None):
        """Login to XYZ-Project Website
        v0: login()
        v1: login(<username>, <password>)
        v2: login("__token__", <token>)
        v3: login("__public__")
        """
        if username is None:
            self.api_version = "v0"
            return
        if username == "__token__":
            self.api_version = "v2"
            self.token = password
            return
        if username == "__public__":
            self.api_version = "v3"
            return

        self.api_version = "v1"
        self.sess = requests.Session()
        self.sess.post(
            self.url + "/login_check",
            {"name": username, "passwd": password, "active_key": ""},
        )

    # -----------------------------------------------------
    # APIs (kind: 2)
    # -----------------------------------------------------
    @api_def
    def reset_active_key(self):
        return

    @api_def
    def restart_calculation(self, calc_id: int):
        return

    @api_def
    def change_password(self, old: str, new: str):
        return

    @api_def
    def insert_token(self, api_ids: list):
        raise "Disabled API"

    @api_def
    def delete_token(self, token_id: int):
        return {"token_id2": token_id}

    @api_def
    def insert_material(self, name: str, source: str, files: dict = {}):
        """Insert a material to database
        Returns:
            id of this material
            None if fails
        """
        delimiter = "#" + "-" * 30 + "\n"
        contents = ""
        for fn, path in files.items():
            contents += delimiter + fn + "\n" + delimiter
            with open(path, "r") as f:
                contents += f.read()
        return {"files": contents}

    @api_def
    def delete_material(self, mid: int):
        return {"mid2": mid}

    @api_def
    def search_material(self, filter: dict = {}):
        property = []
        condition = []
        for p, c in filter.items():
            property.append(p)
            condition.append(c)
        return {"p[]": property, "c[]": condition, "filter": None}

    @api_def
    def insert_mset(self, ms_name: str):
        """Insert a material set to database
        Returns:
            id of this material set
            None if fails
        """
        return

    @api_def
    def delete_mset(self, ms_name: str):
        return

    @api_def
    def add_to_mset(self, ms_name: str, mids: list):
        return {"mids[]": mids, "mids": None}

    @api_def
    def remove_from_mset(self, ms_name: str, mids: list):
        return {"mids[]": mids, "mids": None}

    @api_def
    def mset_materials(self, ms_name: str):
        return

    @api_def
    def insert_share_file(self, filename: str, path: str):
        return {
            "files": {"file": (filename, open(path, "rb"))},
            "filename": None,
            "path": None,
        }

    @api_def
    def delete_share_file(self, filename: str):
        return {"fn": filename, "filename": None}

    @api_def
    def rename_share_file(self, old: str, new: str):
        return

    @api_def
    def update_material_file(self, mid: int, filename: str, path: str):
        return {
            "files": {"file": (filename, open(path, "rb"))},
            "filename": None,
            "path": None,
        }

    @api_def
    def delete_material_file(self, mid: int, filename: str):
        return {"fn": filename, "filename": None}

    @api_def
    def insert_code(self, cores: int, entrance: str, iop: dict, freeze: bool = True):
        """Insert a code to database
        Returns:
            id of this code
            None if fails
        """
        if cores not in (1, 24):
            raise "Cores must be 1 or 24."
        _iop = {}
        for key in ["input", "output", "property"]:
            _iop[key] = iop.get(key, [])
        if freeze:
            _freeze = "freeze"
        else:
            _freeze = None
        return {"iop": json.dumps(_iop), "freeze": _freeze}

    @api_def
    def delete_code(self, cid: int):
        return {"cid2": cid}

    @api_def
    def update_code(
        self, cid: int, cores: int, entrance: str, iop: dict, freeze: bool = True
    ):
        if cores not in (1, 24):
            raise "Cores must be 1 or 24."
        _iop = {}
        for key in ["input", "output", "property"]:
            _iop[key] = iop.get(key, [])
        if freeze:
            _freeze = "freeze"
        else:
            _freeze = None
        return {"iop": json.dumps(_iop), "freeze": _freeze}

    @api_def
    def insert_task(
        self,
        cid: int,
        name: str,
        description: str,
        config: str,
        enable: bool = True,
        freeze: bool = True,
    ):
        """Insert a task to database
        Returns:
            id of this task
            None if fails
        """
        if freeze:
            _freeze = "freeze"
        else:
            _freeze = None
        return {"freeze": _freeze}

    @api_def
    def delete_task(self, tid: int):
        return {"tid2": tid}

    @api_def
    def update_task(
        self,
        tid: int,
        cid: int,
        name: str,
        description: str,
        config: str,
        enable: bool = True,
        freeze: bool = True,
    ):
        if freeze:
            _freeze = "freeze"
        else:
            _freeze = None
        return {"freeze": _freeze}

    @api_def
    def insert_tree(self, name: str, tids: list, tree: list):
        """Insert a tree to database
        Returns:
            id of this tree
            None if fails
        """
        # expand tids
        new_tids = tids.copy()
        new_tree = []
        for father, childs in tree:
            _childs = []
            for c in childs:
                if c is None:
                    _childs.append(len(new_tids))
                    new_tids.append(0)
                else:
                    _childs.append(c)
            new_tree.append([father, _childs])

        return {
            "tid": new_tids[0],
            "tids": json.dumps(new_tids),
            "t": json.dumps(new_tree),
            "tree": None,
        }

    @api_def
    def delete_tree(self, tree_id: int):
        return

    @api_def
    def answer_tree(self):
        raise "Disabled API"

    @api_def
    def remove_from_tree(self):
        raise "Disabled API"

    @api_def
    def save_tree(self):
        raise "Disabled API"

    @api_def
    def insert_plan(self, name: str, mset_id: int, tree_id: int, script_id: int):
        """Insert a plan to database
        Returns:
            id of this plan
            None if fails
        """
        return {"sid": script_id}

    @api_def
    def delete_plan(self, plan_id: int):
        return {"pid": plan_id, "plan_id": None}

    @api_def
    def plan_set_active(self, plan_id: int, active: bool, debug: False):
        # False -> 0
        if active and debug:
            _debug = 1
        else:
            _debug = 0

        return {"pid": plan_id, "plan_id": None, "active": int(active), "debug": _debug}

    @api_def
    def plan_set_script(self, plan_id: int, script_id: int):
        return {"pid": plan_id, "sid": script_id}

    @api_def
    def search_calculation(self, mid, tid, state: str = "__all__"):
        ret = {}
        if type(mid) == list:
            ret["mid"] = json.dumps(mid)
        if type(tid) == list:
            ret["tid"] = json.dumps(tid)
        ret["state"] = state
        return ret

    @api_def
    def get_property(self, mid, pname: str):
        ret = {}
        if type(mid) == list:
            if sorted(mid) != mid:
                raise "Please Sort Mids"
            ret["mid[]"] = mid
            ret["mid"] = None
        return ret

    @api_def
    def set_property(self, mid: int, pname: str, value):
        return {"value": json.dumps(value)}

    @api_def
    def get_property_public(self, mid, pname: str):
        if self.api_version != "v3":
            raise "Please Set api_version = 'v3'"
        ret = {}
        if type(mid) == list:
            if sorted(mid) != mid:
                raise "Please Sort Mids"
            ret["mid[]"] = mid
            ret["mid"] = None
        return ret

    @api_def
    def search_material_public(self, filter: dict = {}):
        if self.api_version != "v3":
            raise "Please Set api_version = 'v3'"
        property = []
        condition = []
        for p, c in filter.items():
            property.append(p)
            condition.append(c)
        return {"p[]": property, "c[]": condition, "filter": None}

    @api_def
    def terminate_calculation(self, calc_id: int):
        if self.api_version != "v0":
            raise "Please Set api_version = 'v0'"
        return

    # -----------------------------------------------------
    # Work API
    # -----------------------------------------------------
    @api_def
    def work_user(self):
        return

    @api_def
    def work_table(self, db: str, uid: int = 0):
        """Work Table Pages
        Args:
            db must be one of (mset, code, task, tree, plan)
        """
        if db not in ("mset", "code", "task", "tree", "plan"):
            raise "db must be one of (mset, code, task, tree, plan)"
        return

    @api_def
    def insert_package(self, pkg_name):
        return

    @api_def
    def all_packages(self):
        return


# -- example -- #
"""
from xyz import XYZ_Client

xyz = XYZ_Client("localhost", 4567)
xyz.login("admin", "admin")
user = xyz.work_user()
print("Welcome,", user["name"])
"""
