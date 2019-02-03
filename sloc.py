import os
import re
import sys

EXTS = [("C++",["cpp"],"//"),
        ("C",["c"],"//"),
        ("unknown header",["h"],"//"),
        ("Python",["py"],"#"),
        ("Java",["java"],"//"),
        ("Markdown",["md","markdown"],"<!"),
        ("TeX",["tex"],"%"),
        ("Teko",["to"],"//"),
        ("JS",["js"],"//"),
        ("CSS",["css"],"/\*"),
        ("HTML",["html"],"<!"),
        ("TXT",["txt"],None),
        ("Rust",["rs"],"//"),
        ("Perl",["pl"],"#"),
        ("Assembly",["s"],None)]

class SLOCounter:
    def __init__(self):
        pass
    
    def slo(self,code,comment):
        lines = re.findall("\n[\s]*[^\s][^\n]*","\n"+code)
        if comment is not None:
            lines = [line for line in lines if not re.match("\s*%s" % comment,line)]
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
                    files.append(fullpath.lower())
                else:
                    files += self.files_except(fullpath,excepts)
            return files

    def slo_dir(self,dirname,excepts):
        excepts += ["venv","__pycache__",".git"]
        sloc_dict = {}
        for language in list(zip(*EXTS))[0]:
            sloc_dict[language] = 0
            
        for filename in self.files_except(dirname,excepts):
            for language, extensions, comment in EXTS:
                if any(filename.endswith("."+ext) for ext in extensions):
                    try:
                        with open(filename,"r") as fh:
                            content = fh.read()
                    except UnicodeDecodeError:
                        try:
                            with open(filename,"r",encoding="utf-8") as fh:
                                content = fh.read()
                        except UnicodeDecodeError:
                            print(filename + " is positively unreadable!")
                    sloc_dict[language] += self.slo(content,comment)
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
    if counts["C++"] > counts["C"]:
        counts["C++"] += counts["unknown header"]
        counts["unknown header"] = 0
    elif counts["C"] > counts["C++"]:
        counts["C"] += counts["unknown header"]
        counts["unknown header"] = 0
    for language, sloc in counts.items():
        if sloc > 0:
            print(language + ":" + (" "*(10-len(language))) + str(sloc))
