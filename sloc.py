#!/usr/bin/python3

import os
import re
import sys

EXTS = [("C++",["cpp","cc"],"//"),
        ("C",["c"],"//"),
        ("Assembly",["s"],None),
        ("header",["h"],"//"),
        ("Java",["java"],"//"),
        ("Python",["py"],"#"),
        ("Go",["go"],"//"),
        ("PHP",["php"],"//"),
        ("R",["r"],"#"),
        ("Rust",["rs"],"//"),
        ("Ruby",["rb"],"#"),
        ("Haskell",["hs"],"--"),
        ("Perl",["pl"],"#"),
        ("Scala",["sc","scala"],"//"),
        ("Teko",["to"],"//"),
        ("Shell",["sh"],"#"),
        ("SQL",["sql"],"--"),
        ("JS",["js"],"//"),
        ("JSON",["json"],None),
        ("CSS",["css"],"/\*"),
        ("HTML",["html"],"<!"),
        ("XML",["xml"],"<!"),
        ("YAML",["yml","yaml"],"#"),
        ("XSLT",["xslt"],"<!"),
        ("Embedded Ruby",["erb"],"<!"),
        ("CSV",["csv"],None),
        ("Markdown",["md","markdown"],"<!"),
        ("TeX",["tex"],"%"),
        ("TXT",["txt"],None),
        ("logs",["log"],None),
        ("Batchfile",["bat"],None),
        ("Shell",["sh","bash"],None),]

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
                    files.append(fullpath)
                else:
                    files += self.files_except(fullpath,excepts)
            return files

    def slo_dir(self,dirname,excepts):
        excepts += ["venv","__pycache__",".git",".idea","node_modules"]
        sloc_dict = {}
        unknown_exts = set()
        for language in list(zip(*EXTS))[0]:
            sloc_dict[language] = 0
            
        for filepath in self.files_except(dirname,excepts):
            known_ext = False
            for language, extensions, comment in EXTS:
                if any(filepath.lower().endswith("."+ext) for ext in extensions):
                    known_ext = True
                    try:
                        with open(filepath,"r") as fh:
                            content = fh.read()
                            sloc_dict[language] += self.slo(content,comment)
                    except UnicodeDecodeError:
                        try:
                            with open(filepath,"r",encoding="utf-8") as fh:
                                content = fh.read()
                                sloc_dict[language] += self.slo(content,comment)
                        except UnicodeDecodeError:
                            print(filepath + " is positively unreadable!")
            if not known_ext:
                filename = os.path.split(filepath)[-1]
                if "." in filename:
                    unknown_exts.add("." + filename.split(".")[-1])
        return sloc_dict, unknown_exts

    def go(self):
        dirname = sys.argv[1]
        if len(sys.argv) > 2:
            excepts = sys.argv[2:]
        else:
            excepts = []
        return (self.slo_dir(dirname,excepts))

if __name__ == "__main__":
    counter = SLOCounter()
    counts, unknown_exts = counter.go()
    if counts["C++"] > counts["C"]:
        counts["C++"] += counts["header"]
        counts["header"] = 0
    elif counts["C"] > counts["C++"]:
        counts["C"] += counts["header"]
        counts["header"] = 0
    for language, sloc in counts.items():
        if sloc > 0:
            print(language + ":" + (" "*(10-len(language))) + str(sloc))
    if len(unknown_exts) > 0:
        print("Also found extensions", ", ".join(sorted(list(unknown_exts)))) 
