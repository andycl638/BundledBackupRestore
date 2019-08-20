import multiprocessing
import os, sys, time, errno
import json, subprocess
from shutil import copy, rmtree


def delete_bundle(path):
    '''
        Delete all archive files from scratch once backup is complete

        Arguments:
            src         -- Archive file Path

        Returns:
            message     -- Message display whether files were deleted or not
    '''
    start = time.time()
    try:
        rmtree(path)
        message = "\nDeleted bundle: " + path
        print(message)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
    end = time.time()

    elapsed = end-start
    print("Deleting with rmtree")
    print(elapsed)

def remove(path):
    """
    Remove the file or directory
    """

    cmd = "rm -rf " + path

    start = time.time()

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

    end = time.time()

    elapsed = end-start
    print("Deleting with rmdir and remove")
    print(elapsed)

num_consumers = multiprocessing.cpu_count()
print (num_consumers)

print("TESTING DELETE FUNCTION SPEED")

delete_bundle('/scale01/scratch/vz8/vz8')
remove('scale01/scratch/vz8/vz7')
