# py-backup-script
## Release 0.1.0

Python script for backing up systems from a TOML configuration file. 

### Dependencies:

```
sudo pip3 install toml
```

### Instructions:

1. Make sure Python3 is installed

2. Look at hosts.example.toml and copy it to hosts.toml

```
cp hosts.example.toml hosts.toml
```

3. Configure hosts.toml

```
vim hosts.toml
```

4. Make sure host that is running script has publickey permissions to remote host with defined user

5. Make sure remote user has sudo permissions for running any specified operation

### Usage:

```
chmod +x py-backup-script.py
./py-backup-script.py -c hosts.toml
```

### py-backup-script cli:

```
Beginning backup script

usage: py-backup-script.py [-h] [-v] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -c CONFIG, --config CONFIG
```
