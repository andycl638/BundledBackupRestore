from multiprocessing import Process, Queue
import os, sys, time, errno
import json, subprocess, re
from shutil import copy, rmtree
from glob import glob
from parallelmgmt import ParallelMgmt
import pathlib

arr = 0

def f(name):
    print(name)

def dosomething(q, num):
    q.put([42,None,'hello'])
    time.sleep(5)
    print(num)

    if num == 2:
        p = Process(target=f, args=('bob',))
        p.start()
        p.join()

def dosomething3(num):
    time.sleep(5)
    for x in range(num):
        print(x)


def dosomething2(list):
    ParallelMgmt.test_proc(list)
    time.sleep(5)


    rundsmc()

def rundsmc():
    print("dsmc")

def test1():
    print("\nget a list of all the dirs that needs to be backed up")
    print("path: /vz6")
    start = time.time()
    dir_list = []
    set_list = []
    multi_set = []
    dir_size = 0
    total_size = 0

    for root, dirs, files in os.walk('/vz6'):

        for file in files:
            file_path=os.path.join(root, file)
            dir_size += os.path.getsize(file_path)

        set_list.append(root)
        set_list.append("dest")
        set_list.append(dir_size)
        dir_list.append(set_list)
        set_list = []
        total_size += dir_size
        dir_size = 0


    end = time.time()
    elapsed = end - start
    print(dir_list)
    print("Time to gather all files: %s" %elapsed)


def test2():
    print("\nget a list of all the dirs that needs to be backed up")
    print("path: /vz6")
    start = time.time()
    dir_size = 0
    set_list = []
    count = 0
    #set_list = [f.name for f in os.scandir('/vz6') if f.is_dir()]
    #'/Users/andy/Documents/folder'
    for root, dirs, files in os.walk('/vz6/Level3-10'):
        print(root)
        count += 1


    '''for p in pathlib.Path('/vz6/Level3-10').iterdir():
        if p.is_dir():
            count += 1
            print(p)
            set_list.append(str(p))

    for i in set_list:
        for root, dirs, files in os.walk(i):
            count += 1
            print(root)'''

    end = time.time()
    elapsed = end - start
    print("Time to gather all files: %s" %elapsed)
    print(set_list)
    print (count)

def test3():
    '''
        Prepares a list of directories that will be bundled

        Returns
            dir_list    -- list of directories
            total_size  -- the total size of data that will be backed up
    '''
    print("\nget a list of all the dirs that needs to be backed up")
    print("path: '/Users/andy/Documents/tester'")
    start = time.time()
    dir_list = []
    set_list = []
    multi_set = []
    dir_size = 0
    total_size = 0

    for root, dirs, files in os.walk('/Users/andy/Documents/tester'):
        for dir in dirs:
            dir_path=os.path.join(root, dir)

            for file in os.listdir(dir_path):
                file_path=os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    dir_size += os.path.getsize(file_path)

            set_list.append(dir_path)
            set_list.append("dest")
            set_list.append(dir_size)
            dir_list.append(set_list)
            set_list = []
            total_size += dir_size
            dir_size = 0

    end = time.time()
    elapsed = end - start
    print("Time to gather all files: %s" %elapsed)
    print("Got all dirs and size")
    print(dir_list)
    return dir_list, total_size

if __name__ == '__main__':
    testarr = [1,2,3,4,5,6,7,8,9]

    #ParallelMgmt.test_proc(testarr)

    #q = Queue()

    #q.put(dosomething2(testarr))
#    q.put(dosomething2(testarr))
    #print(q.get())
    '''p = Process(target=dosomething2, args=(q,testarr))
    p2 = Process(target=dosomething, args=(q,2))
    p3 = Process(target=dosomething3, args=(20,))


    p.start()
    print(q.get())
    p.join()

    p2.start()
    print(q.get())
    p2.join()'''

    test2()

'''
[['/Users/andy/Documents/tester/untitled folder', 'dest', 5254493],
['/Users/andy/Documents/tester/vz8', 'dest', 7350],
['/Users/andy/Documents/tester/group1', 'dest', 6148],
['/Users/andy/Documents/tester/3', 'dest', 6148],
['/Users/andy/Documents/tester/2', 'dest', 6148],
['/Users/andy/Documents/tester/untitled folder/sdw copy', 'dest', 3145728],
['/Users/andy/Documents/tester/untitled folder/sdw', 'dest', 3145728],
['/Users/andy/Documents/tester/group1/filer1', 'dest', 6148],
['/Users/andy/Documents/tester/group1/filer1/vz8', 'dest', 0],
['/Users/andy/Documents/tester/3/asfdasd', 'dest', 9565],
['/Users/andy/Documents/tester/3/asfdasd/wert3', 'dest', 0],
['/Users/andy/Documents/tester/2/zdaa', 'dest', 0]]'''




#delete_bundle('/scale01/scratch/vz8/vz8')
#remove('/scale01/scratch/vz8/vz7')
