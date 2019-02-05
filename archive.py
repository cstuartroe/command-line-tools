import os
import json
from datetime import datetime
import argparse

DATE_FORMAT = "%d %b %Y %H:%M:%S UTC"

parser = argparse.ArgumentParser()
parser.add_argument('dirpath', metavar="path/to/dir", type=str, nargs="?",
                    help = "Relative or absolute path to the directory",
                    default=".")
parser.add_argument('skips', metavar="<skip dir>", type=list, nargs="*",
                    help = "directories to skip over")

def included(dirpath,skips):
    for skip in skips:
        if dirpath.endswith(skip):
            return False
    return True

def dir_json(dirpath,skips):
    obj = {"files":{},"dirs":{}}
    
    for item in os.listdir(dirpath):
        fullpath = os.path.join(dirpath,item)
        
        if os.path.isfile(fullpath):
            stats = os.stat(fullpath)
            obj["files"][item] = {"size":stats.st_size,
                                  "mode":stats.st_mode,
                                  "created":datetime.fromtimestamp(stats.st_ctime).strftime(DATE_FORMAT),
                                  "last modified":datetime.fromtimestamp(stats.st_mtime).strftime(DATE_FORMAT),
                                  "owner":stats.st_uid}
            
        elif included(fullpath,skips):
            obj["dirs"][item] = dir_json(fullpath,skips)
            
    return obj

def archive_dir(args):
    archive_filename = os.path.join(args.dirpath,"archive.json")
    skips = args.skips + [".git","venv","__pycache__"]
    
    try:
        with open(archive_filename,"r",encoding="utf-8") as fh:
            archive_json = json.load(fh)
    except FileNotFoundError:
        archive_json = {}
        
    datestr = datetime.utcnow().strftime(DATE_FORMAT)
    archive_json[datestr] = dir_json(args.dirpath,skips)
    
    with open(archive_filename,"w",encoding="utf-8") as fh:
        json.dump(archive_json, fh, indent=4, sort_keys=True)

if __name__ == "__main__":
    args = parser.parse_args()
    archive_dir(args)
