#!/usr/bin/env python3
'''
this script should not depends on any other packages except virtualenv
'''

import virtualenv
import re
import sys
import traceback

MIN_PYTHON_VERSION=(3, 8)
assert sys.version_info >= MIN_PYTHON_VERSION, f"please use proper venv or python interpreter to make sure the python version >= {MIN_PYTHON_VERSION}, current version is {sys.version_info}"

import shutil
import subprocess
import os
import argparse
from typing import NamedTuple, Tuple, Union, List, Optional
import logging
import pathlib

local_venv_path = "./venv"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--pyright-ver",
        dest="pyright_ver",
        default="1.1.374",
        type=str
    )
    parser.add_argument(
        "--nodecache",
        dest="nodecache",
        default=os.path.realpath("./cache"),
        type=str
    )
    parser.add_argument(
        "--nodeenv",
        dest="nodeenv",
        default=os.path.realpath("./nodeenv"),
        type=str
    )
    return parser.parse_args()


def create_local_venv():
    venv_path = os.path.realpath(local_venv_path)
    logging.warning(f"create venv in {venv_path}")
    py_ver = "".join(map(str, sys.version_info[:2]))
    virtualenv.cli_run(
        ["--symlinks", "--clear", "--prompt", f"local{py_ver}", local_venv_path]
    )
    assert os.path.exists(os.path.join(local_venv_path, "bin", "activate")), "fail to create local venv"


def main():
    parsed_args = parse_arguments()
    print(parsed_args)
    use_localvenv = True
    have_venv = prepare_venv(use_localvenv=use_localvenv)
    generate_devenv_scripts(
        use_localvenv,
        parsed_args.pyright_ver,
        nodecache=parsed_args.nodecache,
        nodeenv=parsed_args.nodeenv
    )
    install_mypy(user=False)
    install_tomli(user=False)
    install_dependencies()
    

devenv='''set -e
{source_cmd}
set +e

export PYRIGHT_PYTHON_DEBUG=1
export PYRIGHT_PYTHON_FORCE_VERSION={pyright_version}
export PYRIGHT_PYTHON_VERBOSE=1
export PYRIGHT_PYTHON_GLOBAL_NODE=0
export PYRIGHT_PYTHON_CACHE_DIR="{nodecache}"
export PYRIGHT_PYTHON_ENV_DIR="{nodeenv}"
'''

devenv_exec='''#!/bin/bash
source "{devenv_path}"
set -e
set -o pipefail
if (($# > 0)); then
    set -x
    exec "$@"
fi
'''

def generate_devenv_scripts(
        use_localvenv: bool, 
        pyright_ver: str,
        nodecache: str,
        nodeenv: str
    ) -> bool:
    if use_localvenv:
        localvenv_realpath = str(pathlib.Path(local_venv_path).resolve())
        assert os.path.exists(localvenv_realpath)
    else:
        localvenv_realpath = None
    devenv_source = []
    if localvenv_realpath:
        devenv_source.append(f'source "{localvenv_realpath}/bin/activate"')
    else:
        devenv_source.append(">&2 echo -e '\033[33mWARNING: Using global python environment!\033[0m'")
    render_template(
        template=devenv,
        output="./devenv",
        source_cmd = "\n".join(devenv_source),
        pyright_version = pyright_ver,
        nodecache = nodecache,
        nodeenv = nodeenv
    )
    render_template(
        devenv_exec,
        "./devenv_exec",
        devenv_path = str(pathlib.Path("./devenv").resolve())
    )
    os.chmod("./devenv_exec", mode=0o755)
    return localvenv_realpath is not None





def render_template(template: str, output: Optional[str], **kwargs)->str:
    rendered = template.format(**kwargs)
    if output:
        if pathlib.Path(output).exists():
            os.unlink(output)
        with open(output, "w") as _f:
            _f.write(rendered)
            _f.flush()
    return rendered


def install_mypy(user: bool):
    for packet in ["pip", "mypy", "pyright", "pytest", "build"]:
        cmd = [
            "./devenv_exec",
            "pip",
            "install",
            "--upgrade",
            packet
        ]
        if user:
            cmd.append("--user")
        run_command(cmd)


def install_tomli(user: bool):
    try:
        import tomllib
    except ModuleNotFoundError:
        # before py311 we need tomli to parse toml
        cmd = [
            "./devenv_exec",
            "pip",
            "install",
            "--upgrade",
            "tomli"
        ]
        if user:
            cmd.append("--user")
        run_command(cmd) 


def install_dependencies():
    cmd = [
        "./devenv_exec",
            "pip",
            "install",
            "-e", # to make editable install (won't copy files to ./venv) to allow pyright work on the source without confusing it from installed version.
            "."
    ]
    run_command(cmd)


def run_command(
    cmd: Union[str, List[str]]
)->None:
    logging.warning("call `%s`", " ".join(cmd) if not isinstance(cmd, str) else cmd)
    is_shell = isinstance(cmd, str)
    subprocess.check_call(cmd, shell=is_shell, stdout=sys.stderr)


def prepare_venv(use_localvenv:bool)->bool:
    if use_localvenv:
        if os.path.exists(os.path.join(local_venv_path, "bin", "activate")):
            logging.warning(f"use existing local venv")
        else:
            create_local_venv()
        return True
    else:
        logging.warning(f"we will use global python environment in {os.environ.get('VIRTUAL_ENV', sys.executable)}")
        if os.path.exists(local_venv_path):
            logging.warning(f"mv venv to venv.bak")
            if os.path.exists("venv.bak"):
                shutil.rmtree("venv.bak")
            shutil.move(local_venv_path, local_venv_path+".bak")
        return os.environ.get('VIRTUAL_ENV') is not None


if __name__ == '__main__':
    main()
