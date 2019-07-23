import os
import sys
import time
from shutil import copy
from multiprocessing import Pool
import subprocess
from os.path import join, getsize

def get_all_dirs(src_path, dest_path):
    print("\nget a list of all the files that needs to be backed up")
    print("path: %s" %src_path)
    start = time.time()
    dir_list = []
    set_list = []
    multi_set = []
    total_size = 0

    for root, dirs, files in os.walk(src_path):
        for dir in dirs:
            dir_path=os.path.join(root, dir)
            #print(dir_path)

            for file in os.listdir(dir_path):
                file_path=os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)

            set_list.append(dir_path)
            set_list.append(dest_path)
            set_list.append(total_size)
            dir_list.append(set_list)
            set_list = []

            #print(total_size/1024/1024)
            total_size = 0

    end = time.time()
    elapsed = end - start
    print("Time to gather all files: %s" %elapsed)
    print("Got all dirs and size")
    print(dir_list)
    return dir_list

def get_dir_size(dir_path):
    set_list = []

    total_size = 0

    for file in os.listdir(dir_path):
        file_path=os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)
        set_list.append(dir_path)
        set_list.append(total_size)

    print(set_list)
    return set_list

def parallel_bundler(dir_list):
    print("\nStarting parallel bundler")
    start = time.time()

    with Pool(8) as p:
        messages = p.map(bundled_func, dir_list)

    for message in messages:
        print(message)

    end = time.time()
    elapsed = end - start
    print("Total Time elapsed: %s" %elapsed)

def bundled_func(dir_list):

    start = time.time()

    message, elapsed_proc_time = bundle_file_set(dir_list[0], dir_list[1])

    end = time.time()
    elapsed = end - start

    size_mib = dir_list[2]/1024/1024
    size_gib = size_mib/1024

    throughput = size_mib / elapsed_proc_time
    result_str = "\nResults:"
    size_str = "\nSize of tar director in GiB: " + str(size_gib)
    elapsed_str = "\nTime elapsed per process: %s" %elapsed
    throughput_str = "\nThroughput (MiB/sec): " + str(throughput)
    message = result_str + message + size_str + elapsed_str + throughput_str
    return message


def bundle_file_set(src_path, dest_path):
    print("bundle the file set into tar")

    static_tar_name = "vzStar"
    unique_name = static_tar_name + str(time.time()) + ".star"

    tar_name_str = "\ntarname: %s" %unique_name
    tar_path = os.path.join(dest_path, unique_name)
    cmd = "time star -c -f \"" + tar_path + "\" fs=32m bs=64K pat=*.* " + src_path + "/*.*"
    start = time.time()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())
    end = time.time()
    elapsed_proc_time = end - start
    message = tar_name_str + "\n" + cmd
    return message, elapsed_proc_time


def log_files():
    print("this function will track all files being backed up")

def main(argv):
    #src
    #dest
    if len(argv) < 2:
        print("Not enough arguments. Need two arguments.")
        print("Example: src dest")
        sys.exit()
    if len(argv) > 2:
        print("Too many arguments. Need two arguments.")
        print("Syntax: python3 bundler.py <src path> <dest path>")
        sys.exit()

    src_path = argv[0]
    dest_path = argv[1]
    if os.path.isdir(src_path):
        print("Source Path: %s" %src_path)
    else:
        print("Source path is not valid: %s" %src_path)
        sys.exit()
    if os.path.isdir(dest_path):
        print("Destination Path: %s" %dest_path)
    else:
        print("Destination path is not valid: %s" %dest_path)
        sys.exit()

    dir_list = get_all_dirs(src_path, dest_path)
    parallel_bundler(dir_list)

if __name__ == '__main__':
    print("starting script\n")
    #fileList = get_all_files("/vz9")
    #setList = get_file_set(fileList, 10000000000)
    #parallel_bundler(setList)
    main(sys.argv[1:])
    #Local
    #dir_list = get_all_dirs("/Users/andy/Documents/tester")
    #parallel_bundler(dir_list)


    #get_dir_size(dir_list)

"""
def send_to_scratch(scratchPath, tarPath):
    print("\nMove tar file to scratch")
    sendCmd = "mv " + tarPath + " " + scratchPath
    print(sendCmd)

    p = subprocess.Popen(sendCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

def delete_bundle(bundlePath):
    print("\nDeleting bundle")
    deleteCmd = "rm -rf " + bundlePath
    print(deleteCmd)

    p = subprocess.Popen(deleteCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

def get_all_files(volumePath):
    print("\nget a list of all the files that needs to be backed up")
    print("path: %s" %volumePath)
    start = time.time()
    fileList = []

    for root, dirs, files in os.walk(volumePath):
        for name in files:
            fileInfoList = []
            fullpath = os.path.join(root, name)

            fileSize = os.path.getsize(fullpath)
            fileInfoList.append(fullpath)
            fileInfoList.append(fileSize)
            fileList.append(fileInfoList)

    end = time.time()
    elapsed = end - start
    print("Time to gather all files: %s" %elapsed)
    return fileList

def copy_file_set(setList, tarDir):
    print("\nc=Copying file to set")
    staticTarName = "vzStar"
    uniqueName = staticTarName + str(time.time())
    bundlePath = os.path.join(tarDir, uniqueName)
    print("tarPath: %s" %bundlePath)
    os.makedirs(bundlePath)
    for srcFile in setList:
        copy(srcFile, bundlePath)

    print ("bundlePath: %s" %bundlePath)
    print(len(setList))
    return bundlePath, len(setList)

def get_file_set(fileList, setSize):
    print("\nselect the files that need to be backed up into sets of 10GB")
    start = time.time()
    setList = []
    multiSet = []
    count = 0

    while len(fileList) > 0:
        for fileTuple in fileList:
            setList.append(fileTuple[0])
            count += fileTuple[1]
            fileList.remove(fileTuple)
            #print(len(fileList))
            if count > setSize:
                print("COUNT: %s" %count)
                count = 0
                break;

        #print("\n\nSETLIST")
        #print(setList)
        #print("COUNT: %s" %str(count))
        multiSet.append(setList)
        #setList = ()
        setList = []
    #print("\n\nMULTISET")
    #print(len(fileList))
    #print(multiSet)
    end = time.time()
    elapsed = end - start
    print("Time to get file set: %s" %elapsed)
    return multiSet


"""
