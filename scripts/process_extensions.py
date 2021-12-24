import re
import sys
from .lib.md_extensions import process

if __name__ == "__main__":
    assert(2 <= len(sys.argv))
    filename = sys.argv[1]
    with open(filename, "r") as f:
        doc = f.read()
    for tag in re.findall(r"\[!.*\]", doc):
        formula = tag[2:-1]
        doc = doc.replace(tag, process(formula, filename))
    with open(filename, "w") as f:
        f.write(doc)