"""
    untility toolkit library
"""
__all__ = ["xdate", "xtime", "module", "hash"]

import utl.xdate
import utl.xtime
import utl.hash


class module:
    """
        module manager
    """
    def __init__(self):
        self._path = None
        self._parent = None
        self._modules = {}

    def init(self, path, parent):
        """
            initialize module object
        :param path:
        :return:
        """
        import os
        self._path = path.rstrip("/")
        self._parent = parent

        files = os.listdir(self._path)
        for file in files:
            if os.path.isfile(self._path+"/"+file) and file.endswith(".py"):
                module = "".join(file.split(".")[:-1])
                self._modules[module] = file

        return self

    def load(self, module):
        """
            load specified module
        :param module: str, module name
        :return: module
        """
        if self._modules.get(module) is None:
            raise "module %s is not exist!" % module

        import importlib
        return importlib.import_module(self._parent+"."+module)

if __name__ == "__main__":
    module = module().init("../dbm/vendor/index", "dbm.vendor.index")
    module = module.load("csindex")
    print(module)

