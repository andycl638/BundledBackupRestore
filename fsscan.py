from multiprocessing import Process, Queue
import os, sys, time, errno
import json, subprocess, re
from shutil import copy, rmtree
import glob
import pathlib
from sys import platform

def get_file_time(path):
    print("Last modified: %s" % time.ctime(os.path.getmtime(path)))
    print("Created: %s" % time.ctime(os.path.getctime(path)))
    stat = os.stat(path)
    print(stat)
    print("Created: %s" % time.ctime(stat.st_ctime))

def write_to_file(path, data):
    start =time.time()
    static_name = "fsscan"
    unique_name = static_name + str(time.time()) + ".txt"
    file_path = os.path.join(path, unique_name)

    print("file: " + file_path)

    with open(file_path, "w+") as write_file:
        for stat in data:
            write_file.write(stat + "\n")
    end = time.time()
    elapsed_time = end-start
    return elapsed_time

def scan_walk(path):
    file_stat = []
    start =time.time()
    for root, dir, files in os.walk(path):
        for file in files:
            statinfo = os.stat(os.path.join(root, file))
            stat_str = "INODE: " + str(statinfo.st_ino) + " SIZE: " + str(statinfo.st_size) + " MTIME: "+ str(statinfo.st_mtime)
            file_stat.append(stat_str)
    end = time.time()
    scan_time = end-start
    return file_stat, scan_time

def scan_glob(path):
    file_stat = []
    start = time.time()
    for file in glob.iglob(path + "/**/*.*", recursive=True):
        statinfo = os.stat(file)
        stat_str = "INODE: " + str(statinfo.st_ino) + " SIZE: " + str(statinfo.st_size) + " MTIME: "+ str(statinfo.st_mtime)
        file_stat.append(stat_str)

    end = time.time()
    scan_time = end-start
    return file_stat, scan_time

def scan_find(path):
    file_stat = []
    cmd = "find " + path + " -type f -print0 | xargs -0 stat --format " + "\"INODE: %i SIZE: %s MTIME: %Y\""
    start = time.time()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in p.stdout:
        line = line.rstrip()
        stat_str = line.decode("utf-8")
        file_stat.append(stat_str)

    end = time.time()
    scan_time = end-start
    return file_stat, scan_time

def scan_scandir(path):
    file_stat = []
    start = time.time()
    for entry in os.scandir(path):
        if entry.is_file():
            yield os.path.join(path, entry.name)
        else:
            yield from scan_scandir(entry.path)

def scan_scandir_wrapper(path):
    file_stat = []
    start = time.time()
    for entry in scan_scandir(path):
        statinfo = os.stat(entry)
        stat_str = "INODE: " + str(statinfo.st_ino) + " SIZE: " + str(statinfo.st_size) + " MTIME: "+ str(statinfo.st_mtime)
        file_stat.append(stat_str)
    end = time.time()
    scan_time = end-start
    return file_stat, scan_time

def scan_listdir(path):
    file_stat = []
    start =time.time()
    entries = os.listdir(path)
    print(entries)
            #statinfo = os.stat(os.path.join(root, file))
            #stat_str = "INODE: " + str(statinfo.st_ino) + " SIZE: " + str(statinfo.st_size) + " MTIME: "+ str(statinfo.st_mtime)
            #file_stat.append(stat_str)
    end = time.time()
    scan_time = end-start
    return file_stat, scan_time

def scan_pathlib(path):
    dir = pathlib.Path(path)
    for file in dir.iterdir():
        print(file)

if __name__ == '__main__':

    path = '/Users/andy/Documents/tester'

    if platform == "linux" or platform == "linux2":
        path = "/vsnap/vpool1/vz9"


    file_stat, scan_time = scan_scandir_wrapper(path)
    write_file_time = write_to_file(path, file_stat)

    print("\nSCANDIR")
    print("scan_time")
    print(scan_time)
    print("write_file_time")
    print(write_file_time)

    file_stat, scan_time = scan_walk(path)
    write_file_time = write_to_file(path, file_stat)

    print("\nOS.WALK")
    print("scan_time")
    print(scan_time)
    print("write_file_time")
    print(write_file_time)

    file_stat, scan_time = scan_find(path)
    write_file_time = write_to_file(path, file_stat)

    print("\nFIND")
    print("scan_time")
    print(scan_time)
    print("write_file_time")
    print(write_file_time)

    file_stat, scan_time = scan_glob(path)
    write_file_time = write_to_file(path, file_stat)

    print("\nGLOB.IGLOB")
    print("scan_time")
    print(scan_time)
    print("write_file_time")
    print(write_file_time)


    #find u -type f -print0 | xargs -0 stat --format "%n INODE: %i SIZE: %s MTIME: %Y"
