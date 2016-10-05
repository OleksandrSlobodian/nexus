# Nexus (ver2.11.4-01) Nuget Trimmer Python Tool.    


This script trimms nexus nuget repositories, trimming procedure based on artifact versioning.  
The script starts with some options:

```
Options:
  -h, --help       show this help message and exit
  --user=USER      nexus API username
  --passwd=PASSWD  nexus API password
  --host=HOST      nexus API host
  --port=PORT      nexus API port
  --keep=KEEP      nexus Artifact versions to keep
  --omit=OMIT      coma separated Nexus repositories
```

```--host``` is mandatory option, all other criteria can be left empty (None).  
If empty, script will run in dry-run mode (no changes will be done to Nexus).
***

## Running it

You can run script by hand, in dry-run mode, via:

```
$ python trimmer.py --host=127.0.0.1 --keep=0

```

To run this script in 'trimming' mode specify ```--user``` and ```--passwd``` options:

```
$ python trimmer.py --host=127.0.0.1 --user=admin --passwd=admin123 --keep=100 --omit=npm,central

```
In this case script will purge all old artifact versions in all repositories except npm and central and keep last 100 versions of each artifact.