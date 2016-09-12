# trusty

[![Build Status](https://travis-ci.org/little9/trusty.svg?branch=master)](https://travis-ci.org/little9/trusty)

This is a Python utility for creating BagIt archives compatiable with
the [APTrust bagging profile](https://sites.google.com/a/aptrust.org/aptrust-wiki/technical-documentation/processing-ingest/aptrust-bagit-profile#TOC-Bag-and-Bagging-Requirements).

# Usage:

```python
t = Trusty({'title':'Title','description':'A description','access':'Restricted'})
t.create_aptrust_bags('./path/to/files')
```

This will create a single bag for each file in the root directory that you provide. The bag
include the entire directory struture for the file in the data/ folder of the bag. If you provided a folder like ``` /Users/jamie/Desktop/files ``` the files in the data folder would include Users and the other subdirectories.

After creation bags will be moved to storage location that is set in the settings.yaml file. 

# Running tests:

```bash
python test.py
```

# Running on the command line

```
./trusty 'Title' 'Description' 'Restricted' /path/to/files
```