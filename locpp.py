import os
import re
import sys

def locpp(cpp):
    lines = re.findall("\n[\s]*[^\s][^\n]*","\n"+cpp)
    return len(lines)

def files_except(dirname, excepts):
    if os.path.split(dirname)[-1] in excepts:
        return []
    else:
        contents = os.listdir(dirname)
        files = []
        for item in contents:
            fullpath = os.path.join(dirname,item)
            if os.path.isfile(fullpath):
                files.append(fullpath)
            else:
                files += files_except(fullpath,excepts)
        return files

def locpp_dir(dirname,excepts):
    excepts += [".git"]
    totalcount = 0
    for filename in files_except(dirname,excepts):
        if filename.endswith(".cpp") or filename.endswith(".h"):
            with open(filename,"r",encoding="utf-8") as fh:
                totalcount += locpp(fh.read())
    return totalcount

#lop_dir("../git repos/plane-data",["messages"])

if __name__ == "__main__":
    dirname = sys.argv[1]
    if len(sys.argv) > 2:
        excepts = sys.argv[2:]
    else:
        excepts = []
    print(locpp_dir(dirname,excepts))
