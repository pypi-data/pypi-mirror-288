#usr/bin/python

import subprocess

retcode = subprocess.call(["ls", "-l"])
print(retcode)