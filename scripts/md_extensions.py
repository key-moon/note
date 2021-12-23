import re
import os
from .tag import get_tags
from os import path
from typing import Callable, Dict, List
from pwn import ELF
import html

F = Callable[[List[str], str], str]

def checksec_handler(args: List[str], file: str):
    binname = args[0]
    elf = ELF(path.join(path.dirname(file), binname), checksec=False)
    return f'Arch:     {elf.arch}-{elf.bits}-{elf.endian}\n{elf.checksec(color=False)}'

def details_handler(args: List[str], file: str) -> str:
    summary, content = args
    return f'<details><summary>{summary}</summary>\n\n{content}\n</details>\n'

def src_handler(args: List[str], file: str):
    name, type = args
    with open(path.join(path.dirname(file), name), "r") as f: 
        return f'```{type}\n{f.read().strip()}\n```\n'

def ctf_challs_handler(args: List[str], file: str):
    res = ""
    with os.scandir(path.dirname(file)) as it:
        for entry in it:
            if not entry.is_dir(): continue
            chall_dir = path.join(entry.path, "index.md")
            if not path.exists(chall_dir): continue
            with open(chall_dir) as f:
                tags = get_tags(f.read())
            name = ""
            if "genre" in tags:
                ex_info = ""
                if "points" in tags: ex_info += f' {tags["points"]} pts'
                name += f'[{tags["genre"]}{ex_info}]'
            if "problem_name" in tags:
                name += f' {tags["problem_name"]}'
            if "solves" in tags:
                name += f' ({tags["solves"]} solve(s))'
            if "during_ctf" in tags and tags["during_ctf"] != "false":
                name += ' ☆'
            res += f' - <a href="{html.escape(entry.name)}">{html.escape(name)}</a>\n'
    return res

_handlers = {
    "checksec": checksec_handler,
    "details": details_handler,
    "src": src_handler,
    "ctf_challs": ctf_challs_handler,
}

def process(s: str, filename: str, handlers=_handlers) -> str:
    s = f'(!{s})'
    i = 0
    def _process() -> str:
        nonlocal i
        if s[i:(i+2)] == '(!':
            i += 1
            l = []
            while s[i] != ')':
                i += 1
                l.append(_process())
            i += 1
            return handlers[l[0]](l[1:], filename)
        else:
            begin = i
            while s[i] != ':' and s[i] != ')': i += 1
            return s[begin:i]
    res = _process()
    assert(i == len(s))
    return res

def process_extensions(filename: str):
    with open(filename, "r") as f:
        doc = f.read()
    for tag in re.findall(r"\[!.*\]", doc):
        formula = tag[2:-1]
        doc = doc.replace(tag, process(formula, filename))
    with open(filename, "w") as f:
        f.write(doc)
