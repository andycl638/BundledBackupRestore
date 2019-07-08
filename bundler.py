import os
import time
from shutil import copy
from multiprocessing import Pool
import subprocess

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
    #print("\n\nFILESET")
    #print(fileList)
    end = time.time()
    elapsed = end - start
    print("Time to gather all files: %s" %elapsed)
    return fileList

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

def parallel_bundler(multiSet):
    print("\nStarting parallel bundler")
    start = time.time()

    #print("\n\nMULTISET")
    #print(multiSet)
    with Pool(8) as p:
        test = p.map(bundled_func, multiSet)

    for message in test:
        print(message)

    end = time.time()
    elapsed = end - start
    print("Total Time elapsed: %s" %elapsed)

def bundled_func(setList):
    start = time.time()
    bundlePath, setListNum = copy_file_set(setList, "/scale01/scratch")
    tarPath = bundle_file_set(bundlePath)
    send_to_scratch("/scale01/scratch/stars", tarPath)
    delete_bundle(bundlePath)

    end = time.time()
    elapsed = end - start
    setNumStr = "\nNumber of files in set: %s" %setListNum
    elapsedStr = "\ntime elapsed per process: %s\n\n" %elapsed
    message = setNumStr + elapsedStr
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

def bundle_file_set(bundlePath):
    print("\nbundle the file set into tar")
    path, bundle = os.path.split(bundlePath)

    #tarName = bundle + ".tar.gz"
    tarName = bundle + ".star"
    print("tarname: %s" %tarName)
    tarPath = os.path.join(path, tarName)
    tarCmd = "time star -c -f " + tarPath + " fs=32m bs=64K " + bundlePath
    #tarCmd = "tar -zcvf " + tarPath + " " + bundlePath
    print(tarCmd)

    print("running star cmd")
    p = subprocess.Popen(tarCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

    tarPath = os.path.join(path, tarName)
    return tarPath

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
    fileList = get_all_files("/vz6")
    setList = get_file_set(fileList, 10000000000)
    parallel_bundler(setList)
