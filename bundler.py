import os
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
    #print(fileList)
    return fileList

def get_file_set(fileList):
    print("select the files that need to be backed up into sets of 10GB")
    setList = []
    count = 0

    for name, size in fileList:
        if count <= 10000000000: #bytes
            count += size
            setList.append(name)
    print(setList)
    print(count)
    return setList

def bundle_file_set():
    print("bundle the file set into tar")

def log_files():
    print("this function will track all files being backed up")

if __name__ == '__main__':
    fileList = get_all_files("/vz8")
    get_file_set(fileList)
