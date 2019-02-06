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

def included(path,skips):
    for skip in skips:
        if path.endswith(skip):
            return False
    return True

def dir_json(dirpath,skips):
    obj = {"files":{},"dirs":{},"total_files":0,"total_dirs":0,"total_size":0}
    
    for item in os.listdir(dirpath):
        fullpath = os.path.join(dirpath,item)
        if included(fullpath, skips):
            if os.path.isfile(fullpath):
                obj["total_files"] += 1
                stats = os.stat(fullpath)
                obj["files"][item] = {"size":stats.st_size,
                                      "mode":stats.st_mode,
                                      "created":datetime.fromtimestamp(stats.st_ctime).strftime(DATE_FORMAT),
                                      "last modified":datetime.fromtimestamp(stats.st_mtime).strftime(DATE_FORMAT),
                                      "owner":stats.st_uid}
                obj["total_size"] += stats.st_size
                
            else:
                obj["total_dirs"] += 1
                subdir_json = dir_json(fullpath,skips)
                obj["dirs"][item] = subdir_json
                obj["total_files"] += subdir_json["total_files"]
                obj["total_dirs"] += subdir_json["total_dirs"]
                obj["total_size"] += subdir_json["total_size"]
            
    return obj

def archive_dir(args):
    archive_filename = os.path.join(args.dirpath,"archive.json")
    skips = args.skips + [".git","venv","__pycache__",".drivedownload"]
    
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
