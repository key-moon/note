#!/bin/python

import shutil
import glob
import os.path as path
import os
from scripts.md_extensions import process_extensions

REPO_DIR = path.abspath(path.dirname(__file__))
DOCS_PATH = path.join(REPO_DIR, "docs")
THEME_PATH = path.join(REPO_DIR, "theme")
WRITEUPS_PATH = path.join(REPO_DIR, "writeups")

WRITEUPS_DEST_PATH = path.join(DOCS_PATH, "ctf")

os.chdir(REPO_DIR)

if path.exists(DOCS_PATH):
    shutil.rmtree(DOCS_PATH)

shutil.copytree(THEME_PATH, DOCS_PATH)
shutil.copytree(WRITEUPS_PATH, WRITEUPS_DEST_PATH)

for tmpl in glob.glob(path.join(WRITEUPS_DEST_PATH, "**/_template"), recursive=True):
    if path.exists(tmpl):
        shutil.rmtree(tmpl)

for md in glob.glob(path.join(WRITEUPS_DEST_PATH, "**/index.md"), recursive=True):
    process_extensions(md)

os.chdir(DOCS_PATH)
os.system("bundle install")
os.system("bundle exec jekyll serve")
