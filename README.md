# command-line-tools

A set of various python command line tools, intended to be added to PATH

## tabs.py

`tabs.py` checks all source code files in a directory and replaces any tabs with four spaces.

## sloc.py 

`sloc.py` prints out how many source lines of code in various languages are present in a directory:

```
> sloc.py teko

Python:    178
JSON:      45
Markdown:  65
Also found extensions .gitignore
```

## archive.py

`archive.py` creates a JSON file which stores any number of metadata snapshots of a directory.

```json
> archive.py command-line-tools/
> cat command-line-tools/archive.json

{
    "06 Feb 2019 00:24:25 UTC": {
        "dirs": {},
        "files": {
            ".gitignore": {
                "created": "19 Jan 2019 23:12:07 UTC",
                "last modified": "19 Jan 2019 23:12:07 UTC",
                "mode": 33206,
                "owner": 0,
                "size": 12
            },
            "README.md": {
                "created": "02 Oct 2018 22:13:46 UTC",
                "last modified": "03 Feb 2019 17:21:49 UTC",
                "mode": 33206,
                "owner": 0,
                "size": 420
            },
            "archive.py": {
                "created": "05 Feb 2019 23:09:52 UTC",
                "last modified": "06 Feb 2019 00:12:46 UTC",
                "mode": 33206,
                "owner": 0,
                "size": 2515
            },
            "sloc.py": {
                "created": "19 Jan 2019 22:33:10 UTC",
                "last modified": "04 Feb 2019 16:53:01 UTC",
                "mode": 33206,
                "owner": 0,
                "size": 3671
            },
            "tabs.py": {
                "created": "12 Jan 2019 00:59:32 UTC",
                "last modified": "19 Jan 2019 23:11:36 UTC",
                "mode": 33206,
                "owner": 0,
                "size": 1016
            }
        },
        "total_dirs": 0,
        "total_files": 5,
        "total_size": 7634
    }
}
```
