#!/bin/python

import argparse
import os
import os.path as path
from lib.content import add_chall
from lib.tag import set_tags
from lib.repo_path import writeups_dir
from lib.interactive import option_getter
import readline
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("CTF_NAME", nargs='?', default="")
    parser.add_argument("CHALL_NAME", nargs='?', default="")

    parser.add_argument("--screen-name", "-n", nargs='?', dest='SCREEN_NAME', default=None)
    parser.add_argument("--genre", "-g", nargs='?', dest='GENRE', default="")
    parser.add_argument("--date", "-d", nargs='?', dest='DATE', default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--tag", "-t", nargs='?', dest='TAG', default="[]")
    parser.add_argument("--in-ctf", dest='IN_CTF', action='store_const', default="false", const="true")
    parser.add_argument("--no-editor", dest='OPEN_EDITOR', action='store_const', default=True, const=False)
    parser.add_argument("--interactive", "-i", dest='INTERACTIVE', action='store_const', default=False, const=True)
    res = parser.parse_args()
    
    tags = {
        "ctf_name": res.CTF_NAME,
        "problem_name": res.CHALL_NAME,
        "genre": res.GENRE,
        "solved_date": res.DATE,
        "during_ctf": res.IN_CTF,
        "tag": res.TAG
    }
    if res.INTERACTIVE:
        ctfs = [entry.name for entry in os.scandir(writeups_dir) if entry.is_dir()]
        ctfs.remove("_template")
        tags = {
            **tags,
            **option_getter(
                ["ctf_name", "problem_name", "genre", "solved_date", "during_ctf", "tag"],
                tags,
                {
                    "ctf_name": ctfs,
                    "genre": ["pwn", "crypto", "web", "rev", "misc", "osint", "forensics"],
                    "during_ctf": ["true", "false"] 
                },
                {}
            )
        }
    
    chall_path = add_chall(tags["ctf_name"], tags["problem_name"], res.SCREEN_NAME)
    chall_md_path = path.join(chall_path, "index.md")
    with open(chall_md_path, "r") as f:
        doc = f.read()
    doc = set_tags(doc, tags)
    with open(chall_md_path, "w") as f:
        f.write(doc)
    
    if res.OPEN_EDITOR:
        os.system(f"code '{chall_path}'")
