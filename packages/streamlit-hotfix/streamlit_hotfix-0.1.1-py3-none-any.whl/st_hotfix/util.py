import importlib.util

def find_pkg_dir(pkg_name: str):
    return importlib.util.find_spec(pkg_name).submodule_search_locations[0]