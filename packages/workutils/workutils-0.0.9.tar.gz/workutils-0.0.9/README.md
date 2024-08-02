# workutils
A tool to solve daily work including file encoding conversion, keyword search, and file type analysis.

## Installation
You can install, upgrade, or uninstall workutils with these commands:
```shell
$ pip install workutils
$ pip install --upgrade workutils
$ pip uninstall workutils
```

## Help

```shell
$ workutils -h
usage: workutils [-h] [-s SUFFIX] [-k KEYWORDS] [-a] [-o OUTPUT] directory

A tool for daily work

positional arguments:
  directory             Folder path to analyze

options:
  -h, --help            show this help message and exit
  -s SUFFIX, --suffix SUFFIX
                        File suffix to analyze
  -k KEYWORDS, --keywords KEYWORDS
                        Count Keywords in all files, such as 'key word1','key word2'
  -a, --all-files       Traverse all files, including hidden files
  -o OUTPUT, --output OUTPUT
                        File path to save the result
  -d, --delete          Delete specified files after confirmation
```

# Example

### Select the folder path to analyze
```sh
$ workutils ../
E:\workutils\a.txt
E:\workutils\LICENSE
E:\workutils\README.md
E:\workutils\workutils\workutils.py
E:\workutils\workutils\__init__.py
========================================
Suffix    Counts
----------------------------------------
.txt      1
          1
.md       1
.py       2
----------------------------------------
Total     5
========================================
$
```

### Select the folder path and specify the files with a certain suffix to analyze.
```sh
$ workutils ../ -s py
E:\workutils\workutils\workutils.py
E:\workutils\workutils\__init__.py
========================================
Suffix    Counts
----------------------------------------
.py       2
----------------------------------------
Total     2
========================================
$ 
```

### Traverse all files, including hidden files
```sh
$ workutils ../ -a   
E:\workutils\a.txt
E:\workutils\LICENSE
E:\workutils\README.md
E:\workutils\.git\config
...
E:\workutils\.git\refs\remotes\origin\HEAD
E:\workutils\workutils\workutils.py
E:\workutils\workutils\__init__.py
========================================
Suffix    Counts
----------------------------------------
.txt      1
          15
.md       1
.sample   13
.idx      1
.pack     1
.py       2
----------------------------------------
Total     34
========================================
PS $ 
```

### Input result file path to save the result
```sh
$ workutils ../ -s py -o result.txt
E:\workutils\workutils\workutils.py
E:\workutils\workutils\__init__.py
========================================
Suffix    Counts
----------------------------------------
.py       2
----------------------------------------
Total     2
========================================
The result has been saved to the E:\workutils\workutils\result.txt file.
$ 
```

### Find keywords and count occurrences in all files
```sh
$ workutils ./ -s log -k 'AS0100504GN_2' -o a.txt
E:\workutils\workutils\1111.log
E:\workutils\workutils\a\a.log
E:\workutils\workutils\b\test.log
E:\workutils\workutils\c\c.log
==================================================
Suffix              Counts
--------------------------------------------------
.log                4
--------------------------------------------------
Total               4
==================================================


100%|███████████████████████████████████████████████| 4/4 [00:00<00:00,  3.76it/s]
==================================================
Keyword             Matches             File Name
--------------------------------------------------
AS0100504GN_2       32                  1111.log
--------------------------------------------------
==================================================

The result has been saved to the E:\workutils\workutils\a.txt file.
$ 
```

### Deleted files 
```sh
$ workutils ../ -s py -d
E:\workutils\workutils\workutils.py
E:\workutils\workutils\__init__.py
========================================
Suffix    Counts
----------------------------------------
.py       2
----------------------------------------
Total     2
========================================


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Are you sure you want to delete these files?
                Type 'yes' to confirm: yes
Deleted file: E:\workutils\workutils\workutils.py
Deleted file: E:\workutils\workutils\__init__.py
$
```
