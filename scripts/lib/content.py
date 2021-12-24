from genericpath import exists
from typing import Callable

import re
from os import path
from glob import glob
from shutil import copy, copytree

from .repo_path import TEMPLATE_NAME, get_chall_dir, get_ctf_dir
from .tag import set_tag


def get_screen_name(name: str):
    name, _ = re.subn(r"[^a-zA-Z0-9\-_]+", "_", name)
    return name.strip('_')

def foreach_files(name, op: Callable[[str], str]):
    for path in glob(name):
        with open(path, "r") as f:
            content = f.read()
        with open(path, "w") as f:
            f.write(op(content))

def add_ctf(name, screen_name = None):
    if screen_name is None: screen_name = get_screen_name(name)
    path_name = get_ctf_dir(screen_name)
    if path.exists(path_name): raise FileExistsError("file already exists")
    copytree(get_ctf_dir(TEMPLATE_NAME), path_name)
    foreach_files(path.join(path_name, "**/index.md"), lambda content: set_tag(content, "ctf_name", name))
    return path_name

def add_chall(ctf_name, chall_name, chall_screen_name = None):
    ctf_screen_name = get_screen_name(ctf_name)
    if chall_screen_name is None: chall_screen_name = get_screen_name(chall_name)
    ctf_path = get_ctf_dir(ctf_screen_name)
    if not exists(ctf_path): add_ctf(ctf_screen_name)
    path_name = get_chall_dir(ctf_screen_name, chall_screen_name)
    if path.exists(path_name): raise FileExistsError("file already exists")
    copytree(get_chall_dir(ctf_screen_name, TEMPLATE_NAME), path_name)
    foreach_files(path.join(path_name, "index.md"), lambda content: set_tag(content, "chall_name", chall_name))
    return path_name

# article list per CTF / article list per tag
# latest
