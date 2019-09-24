from multiprocessing import Process, Queue
import os, sys, time, errno
import json, subprocess, re
from shutil import copy, rmtree
from glob import glob
from parallelmgmt import ParallelMgmt
import pathlib

def get_file_time(path):
    print("Last modified: %s" % time.ctime(os.path.getmtime(path)))
    print("Created: %s" % time.ctime(os.path.getctime(path)))

if __name__ == '__main__':
    get_file_time('/Users/andy/Documents/tester/test.txt')
