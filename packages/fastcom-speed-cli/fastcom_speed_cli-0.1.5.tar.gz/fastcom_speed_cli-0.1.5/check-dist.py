from typing import Dict, Optional
from packaging import version
from glob import glob
import os

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

def get_project_name()->str:
    pyproject_path = os.path.realpath("./pyproject.toml")
    with open(pyproject_path, 'rb') as f:
        pyproject_toml = toml.load(f)
    
    # Access the project name
    maybe_name = pyproject_toml.get(
        'project', {}).get(
            'name', None
        )
    if not maybe_name:
        raise RuntimeError(f"cannot get project name from {pyproject_path}")
    return maybe_name



PROJECT_NAME = get_project_name()
dist_dir = os.path.realpath("./dist")


def write_to_github_output(data: Dict[str, str]):
    # Get the path to the GitHub output file
    github_output_path = os.getenv('GITHUB_OUTPUT')

    if github_output_path:
        with open(github_output_path, 'a') as f:
            for key, val in data.items():
                f.write(f"{key}={val}\n")
    else:
        print(data)


def main():
    is_pypi_compatible = False
    file_prefix = PROJECT_NAME.replace("-", "_")
    gz_files = glob(f"{dist_dir}/{file_prefix}-*.tar.gz")
    if not gz_files:
        raise RuntimeError(f"there is no gz package file in {dist_dir}")
    for i in gz_files:
        file_ver = os.path.basename(i).lstrip(file_prefix + "-").rstrip(".tar.gz")
        if version.parse(file_ver).local:
            is_pypi_compatible = False
            break
        else:
            is_pypi_compatible = True
    write_to_github_output({"is_pypi_compatible": str(is_pypi_compatible).lower()})
    

if __name__ == "__main__":
    main()
