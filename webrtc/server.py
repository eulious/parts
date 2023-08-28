#!/usr/bin/env python

from subprocess import Popen, getoutput

proc = Popen("npx peer --port 9001", shell=True)

try:
    proc.wait()
except KeyboardInterrupt:
    print("kill")
    proc.kill()
    for line in getoutput("ps").split("\n"):
        if "peerjs" in line:
            pid = line.strip().split()[0]
            getoutput(f"kill -9 {pid}")
