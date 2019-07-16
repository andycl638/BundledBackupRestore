import subprocess
import os
import time
from os.path import getsize

def unbundle(src, dest):

    get_bundle_size(src)

    cmd = "star -x -v -f " + src
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=dest)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

    out, err = p.communicate()
    print (out)

def get_bundle_size(src):
    bundle_size = os.path.getsize(src)
    print(bundle_size)
    return bundle_size

if __name__ == '__main__':

    unbundle("/scale01/scratch/testunbundle.star", "/vz8")
