import multiprocessing
import os, sys, time, errno
import json, subprocess, re
from shutil import copy, rmtree

from bundler import Bundler
from dsmcbackup import DsmcBackup
from unbundler import Unbundler
from dsmcrestore import DsmcRestore
from parallelmgmt import ParallelMgmt
from metadatajson import MetadataJson


def write_virtualmnt(file_path, virtual_mnt_pt):
    newfile = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "virtualmountpoint" in line:
                line = line.replace(line, "virtualmountpoint "  + virtual_mnt_pt + "\n")
            newfile.append(line)

    with open(file_path, 'w') as file:
        file.writelines(newfile)





num_consumers = multiprocessing.cpu_count()
print (num_consumers)



#delete_bundle('/scale01/scratch/vz8/vz8')
#remove('/scale01/scratch/vz8/vz7')
