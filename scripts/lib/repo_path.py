from os import path

scripts_dir = path.dirname(__file__)
repo_dir = path.dirname(scripts_dir)
writeups_dir = path.join(repo_dir, "writeups")
docs_dir = path.join(repo_dir, "docs")

def get_ctf_dir(name):
    return path.join(writeups_dir, name)

def get_chall_dir(ctf_name, chall_name):
    return path.join(get_ctf_dir(ctf_name), chall_name)

def get_ctf_docs_dir(name):
    return path.join(docs_dir, name)

def get_chall_docs_dir(ctf_name, chall_name):
    return path.join(get_ctf_docs_dir(ctf_name), chall_name)

TEMPLATE_NAME = "_template"
