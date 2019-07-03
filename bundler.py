import os
import time
from shutil import copy
from multiprocessing import Pool
import subprocess

def get_all_files(volumePath):
    print("get a list of all the files that needs to be backed up")
    print("path: %s" %volumePath)
    fileList = []

    for root, dirs, files in os.walk(volumePath):
        print(root)
        print(dirs)
        print(files)
        for name in files:
            fileInfoList = []
            fullpath = os.path.join(root, name)

            fileSize = os.path.getsize(fullpath)
            fileInfoList.append(fullpath)
            fileInfoList.append(fileSize)
            fileList.append(fileInfoList)
    #print("\n\nFILESET")
    #print(fileList)
    return fileList

def get_file_set(fileList, setSize):
    print("select the files that need to be backed up into sets of 10GB")
    #setList = ()
    setList = []
    multiSet = []
    count = 0
    #print(len(fileList))

    while len(fileList) > 0:
        for fileTuple in fileList:
            #print(fileTuple)
            #tupleBuild = (fileTuple[0],)
            #tupleBuild += setList
            #print(tupleBuild)
            #setList = tupleBuild
            setList.append(fileTuple[0])
            count += fileTuple[1]
            fileList.remove(fileTuple)
            #print(len(fileList))
            if count > setSize:
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
    return multiSet

def parallel_bundler(multiSet):
    start = time.time()
    print("Time start: %s" %start)
    print("\n\nMULTISET")
    print(multiSet)
    with Pool(8) as p:
        p.map(bundled_func, multiSet)

    end = time.time()
    print("Time end: %s" %end)
    elapsed = end - start
    print("Time elapsed: %s" %elapsed)

def bundled_func(setList):
    bundlePath = copy_file_set(setList, "/Users/andy/Documents/tester")
    tarPath = bundle_file_set(bundlePath)
    send_to_scratch("/Users/andy/Documents", tarPath)
    delete_bundle(bundlePath)

def copy_file_set(setList, tarDir):
    staticTarName = "vzTar"
    uniqueName = staticTarName + str(time.time())
    bundlePath = os.path.join(tarDir, uniqueName)
    print("tarPath: %s" %bundlePath)
    os.makedirs(bundlePath)
    for srcFile in setList:
        copy(srcFile, bundlePath)


    print ("bundlePath: %s" %bundlePath)
    return bundlePath

def bundle_file_set(bundlePath):
    print("bundle the file set into tar")
    path, bundle = os.path.split(bundlePath)

    tarName = bundle + ".tar.gz"
    print("tarname: %s" %tarName)
    tarPath = os.path.join(path, tarName)
    #tarCmd = "time star -c -f " + uniqueName + ".star fs=32m bs=64K " + tarPath
    tarCmd = "tar -zcvf " + tarPath + " " + bundlePath
    print(tarCmd)

    print("running tar")
    p = subprocess.Popen(tarCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    print(p.returncode)
    tarPath = os.path.join(path, tarName)
    return tarPath

def send_to_scratch(scratchPath, tarPath):
    sendCmd = "mv " + tarPath + " " + scratchPath
    print(sendCmd)
    print("running send")
    p = subprocess.Popen(sendCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    print(p.returncode)
    print(p.stdout.read())

def delete_bundle(bundlePath):
    deleteCmd = "rm -rf " + bundlePath
    print(deleteCmd)
    print("running send")
    p = subprocess.Popen(deleteCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    print(p.returncode)
    print(p.stdout.read())

def log_files():
    print("this function will track all files being backed up")

if __name__ == '__main__':
    print("starting script")
    fileList = get_all_files("/Users/andy/Documents/tester")
    setList = get_file_set(fileList, 1048576)
    parallel_bundler(setList)
