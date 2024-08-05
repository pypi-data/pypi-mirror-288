import importlib
import traceback

import importlib
import pkgutil
import os
import sys

def all_modules(package_name):
    # Add the package directory to sys.path
    package_dir = os.path.join(os.path.dirname(__file__), package_name)
    sys.path.insert(0, package_dir)

    # Import the package
    package = importlib.import_module(package_name)
    module_names = []

    # Iterate over all modules in the package
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module_names.append(f"{package_name}.{module_name}")
    return module_names

def main():
    problems = []
    for name in all_modules("fast_speedtest"):
        print(f"try import {name}")
        try:
            mymodule = importlib.import_module(name)
        except Exception as e:
            problems.append(traceback.print_exc())
    if  problems:
        for _p in problems:
            print(_p)
        exit(1)
    exit(0)
        
if __name__ == "__main__":
    main()
