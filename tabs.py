import os
import sys

CODE_EXTENSIONS = {"py","cpp","json","java"}
IGNORED_DIRS = {"venv","__pycache__",".git"}

def is_code(filename):
    for ext in CODE_EXTENSIONS:
        if filename.endswith("."+ext):
            return True
    return False

def replace_tabs(filepath):
    with open(filepath,"r") as fh:
        tabbed = fh.read()
    num_tabs = tabbed.count("\t")
    if num_tabs > 0:
        spaced = tabbed.replace("\t"," "*4)
        with open(filepath,"w") as fh:
            fh.write(spaced)
        print("Replaced",num_tabs,"tabs in",filepath)

for root, dirs, files in os.walk(sys.argv[1], topdown=True):
    for dirname in IGNORED_DIRS:
        if dirname in dirs:
            dirs.remove(dirname)
    for filename in files:
        filepath = os.path.join(root,filename)
        print(filepath)
        if is_code(filename):
            try:
                replace_tabs(filepath)
            except:
                print("Error editing",filepath)
