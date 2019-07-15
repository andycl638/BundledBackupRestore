import os
import time
from shutil import copy
from multiprocessing import Pool
import subprocess
from os.path import join, getsize

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

def get_all_dirs(volumePath):
    print("\nget a list of all the files that needs to be backed up")
    print("path: %s" %volumePath)
    start = time.time()
    dir_list = []
    set_list = []
    multi_set = []
    total_size = 0

    for root, dirs, files in os.walk(volumePath):
        for dir in dirs:
            dir_path=os.path.join(root, dir)
            #print(dir_path)

            for file in os.listdir(dir_path):
                file_path=os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)

            set_list.append(dir_path)
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
    print("\n")

    message = bundle_file_set(dir_list[0])

    end = time.time()
    elapsed = end - start
    result_str = "Results:\n"
    sizeStr = "Size of directory in tar: %s" %dir_list[1]
    elapsedStr = "\nTime elapsed per process: %s\n\n" %elapsed
    message = result_str + message + sizeStr + elapsedStr
    return message

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

def bundle_file_set(src_path):
    print("bundle the file set into tar")

    dest_path = "/scale01/scratch"

    staticTarName = "vzStar"
    uniqueName = staticTarName + str(time.time()) + ".star"

    #tarName = bundle + ".tar.gz"

    tar_name_str = "tarname: %s" %uniqueName
    tarPath = os.path.join(dest_path, uniqueName)
    tarCmd = "time star -c -f \"" + tarPath + "\" fs=32m bs=64K pat=*.* " + src_path + "/*.*"
    #tarCmd = "tar -zcvf " + tarPath + " " + bundlePath

    #print("running star cmd")
    #print(tarCmd)
    p = subprocess.Popen(tarCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

    message = tar_name_str + "\n" + tarCmd + "\n"
    return message

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

def log_files():
    print("this function will track all files being backed up")

if __name__ == '__main__':
    print("starting script\n")
    #fileList = get_all_files("/vz9")
    #setList = get_file_set(fileList, 10000000000)
    #parallel_bundler(setList)

    #Local
    #dir_list = get_all_dirs("/Users/andy/Documents/tester")
    #parallel_bundler(dir_list)

    dir_list = get_all_dirs("/vz6")
    parallel_bundler(dir_list)
    #get_dir_size(dir_list)
