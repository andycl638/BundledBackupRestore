import os
import time
from shutil import copy
import subprocess

def get_all_files(volumePath):
    print("get a list of all the files that needs to be backed up")
    print("path: %s" %volumePath)
    volumePath = os.getcwd()
    print("path: %s" %volumePath)

    fileList = []
    for root, dirs, files in os.walk(volumePath, topdown=False):
        for name in files:
            fileInfoList = []
            fullpath = os.path.join(root, name)

            fileSize = os.path.getsize(fullpath)
            fileInfoList.append(fullpath)
            fileInfoList.append(fileSize)
            fileList.append(fileInfoList)
    print("\n\nFILESET")
    print(fileList)
    return fileList

def get_file_set(fileList, setSize):
    print("select the files that need to be backed up into sets of 10GB")
    setList = []
    multiSet = []
    count = 0
    print(len(fileList))
    while len(fileList) > 0:
        for i in range(len(fileList)-1):
            arr = fileList.pop(i)
            if count <= 10000000000: #bytes, replace with setSize
                count += arr[1]
                setList.append(arr[0])

        print("\n\nSETLIST")
        print(setList)
        print(count)
        multiSet.append(setList)

    print("\n\nMULTISET")
    print(multiSet)
    return multiSet

def parallel_bundler(multiSet):
    start = time.time()
    print("Time start: %s" %start)



    with Pool(8) as p:
        p.starmap(copy_file_set, parallelArgs)

    end = time.time()
    print("Time end: %s" %end)
    elapsed = end - start
    print("Time elapsed: %s" %elapsed)

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

    #tarCmd = "time star -c -f " + uniqueName + ".star fs=32m bs=64K " + tarPath
    tarCmd = "tar -zcvf " + tarName + " " + bundle
    print(tarCmd)

    print("running tar")
    p = subprocess.Popen(tarCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        time.sleep(0.5)

    print(p.returncode)
    tarPath = os.path.join(path, tarName)
    return tarPath

def send_to_scratch(scratchPath, tarFile):
    sendCmd = "mv " + tarFile + " " + scratchPath
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
    fileList = get_all_files("/vz8")
    setList = get_file_set(fileList, 0)
    #bundlePath = copy_file_set(setList, "/Users/andy/Documents/NetAppVZBundling")
    #tarPath = bundle_file_set(bundlePath)
    #send_to_scratch("/Users/andy/Documents", tarPath)
    #delete_bundle(bundlePath)
