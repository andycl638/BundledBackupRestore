from multiprocessing import Process, Queue
import os, sys, time, errno
import json, subprocess, re
from shutil import copy, rmtree

from parallelmgmt import ParallelMgmt

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

    print("\nget a list of all the dirs that needs to be backed up")
    print("path: /vz6")
    start = time.time()
    dir_size = 0


    for root, dirs, files in os.walk('/vz6'):
        for dir in dirs:
            dir_path=os.path.join(root, dir)

            for file in os.listdir(dir_path):
                file_path=os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    dir_size += os.path.getsize(file_path)

            print(dir_path)
            print(dir_size)
            dir_size = 0

    end = time.time()
    elapsed = end - start
    print("Time to gather all files: %s" %elapsed)




#delete_bundle('/scale01/scratch/vz8/vz8')
#remove('/scale01/scratch/vz8/vz7')
