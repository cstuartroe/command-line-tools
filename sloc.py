import os
import re
import sys

EXTS = {"C++":["cpp","h"],"Python":["py"],"Java":["java"],"Markdown":["md"],"TeX":["tex"],"Teko":["to"]}

class SLOCounter:
    def __init__(self):
        pass
    
    def slo(self,code):
        lines = re.findall("\n[\s]*[^\s][^\n]*","\n"+code)
        lines = [line for line in lines if not re.match("\s*(#|//)",line)]
        return len(lines)

    def files_except(self, dirname, excepts):
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
                    files += self.files_except(fullpath,excepts)
            return files

    def slo_dir(self,dirname,excepts):
        excepts += ["venv","__pycache__",".git"]
        sloc_dict = {}
        for language in EXTS.keys():
            sloc_dict[language] = 0
            
        for filename in self.files_except(dirname,excepts):
            for language, extensions in EXTS.items():
                if any(filename.endswith("."+ext) for ext in extensions):
                    with open(filename,"r",encoding="utf-8") as fh:
                        sloc_dict[language] += self.slo(fh.read())
        return sloc_dict

    def go(self):
        dirname = sys.argv[1]
        if len(sys.argv) > 2:
            excepts = sys.argv[2:]
        else:
            excepts = []
        return (self.slo_dir(dirname,excepts))

if __name__ == "__main__":
    counter = SLOCounter()
    counts = counter.go()
    for language, sloc in counts.items():
        if sloc > 0:
            print(language + ":" + (" "*(10-len(language))) + str(sloc))
