#!/usr/bin/python

import os
import os.path as path
import sys
from lib.repo_path import scripts_dir

if __name__ == "__main__":
    arg_dict = {
        "add-ctf": path.join(scripts_dir, "./add_ctf.py"),
        "add-chall": path.join(scripts_dir, "./add_chall.py"),
    }
    if sys.argv[1] == '-h':
        print('usage: note [-h] {add-ctf,add-chall} [ARGS [ARGS ...]]')
        exit(0)
    bin = arg_dict[sys.argv[1].strip()]
    args = sys.argv[2:]
    if len(args) == 0: args = ["-i"]
    os.execv(bin, [bin, *args])
