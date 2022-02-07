#!/bin/python

import argparse
import os
import os.path as path
from lib.content import add_ctf
from lib.tag import set_tags
from lib.repo_path import writeups_dir
from lib.interactive import option_getter
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("CTF_NAME", nargs='?', default="")

    parser.add_argument("--screen-name", "-n", nargs='?', dest='SCREEN_NAME', default=None)
    parser.add_argument("--prologue", dest='PROLOGUE', action='store_const', default="false", const="true")

    parser.add_argument("--begin-date", nargs='?', dest='BEGIN_DATE', default=datetime.now().strftime("%Y-%m-%dT00:00:00"))
    parser.add_argument("--end-date", nargs='?', dest='END_DATE', default=datetime.now().strftime("%Y-%m-%dT00:00:00"))

    parser.add_argument("--team-name", "-t", nargs='?', dest='TEAM_NAME', default="")

    parser.add_argument("--solo", dest='SOLO', action='store_const', default="false", const="true")

    parser.add_argument("--team-points", "-P", nargs='?', dest='TEAM_POINTS', default="")
    parser.add_argument("--team-solves", "-S", nargs='?', dest='TEAM_SOLVES', default="")
    parser.add_argument("--my-points", "-p", nargs='?', dest='MY_POINTS', default="")
    parser.add_argument("--my-solves", "-s", nargs='?', dest='MY_SOLVES', default="")

    parser.add_argument("--rank", "-r", nargs='?', dest='RANK', default="")

    parser.add_argument("--no-editor", dest='OPEN_EDITOR', action='store_const', default=True, const=False)
    parser.add_argument("--interactive", "-i", dest='INTERACTIVE', action='store_const', default=False, const=True)
    res = parser.parse_args()
    
    tags = {
        "ctf_name": res.CTF_NAME,
        "prologue": res.PROLOGUE,
        "duration": f'[{res.BEGIN_DATE}, {res.END_DATE}]',
        'team_name': res.TEAM_NAME,
        'solo': res.SOLO,
        'team_points': res.TEAM_POINTS,
        'team_solves': res.TEAM_SOLVES,
        'my_points': res.MY_POINTS,
        'my_solves': res.MY_SOLVES,
        'rank': res.RANK
    }
    if res.INTERACTIVE:
        ctfs = [entry.name for entry in os.scandir(writeups_dir) if entry.is_dir()]
        ctfs.remove("_template")
        tags = option_getter(
            ["ctf_name", "prologue", "duration", "team_name", "solo", "team_points", "team_solves", "my_points", "my_solves", "rank"],
            tags,
            {
                "ctf_name": ctfs,
                "prologue": ["true", "false"],
                "team_name": ["zer0pts"],
                "solo": ["true", "false"],
                "genre": ["pwn", "crypto", "web", "rev", "misc", "osint", "forensics"],
            },
            {}
        )
    
    ctf_path = add_ctf(tags["ctf_name"], res.SCREEN_NAME)
    ctf_md_path = path.join(ctf_path, "index.md")
    with open(ctf_md_path, "r") as f:
        doc = f.read()
    doc = set_tags(doc, tags)
    with open(ctf_md_path, "w") as f:
        f.write(doc)
    
    if res.OPEN_EDITOR:
        os.system(f"code '{ctf_path}'")
