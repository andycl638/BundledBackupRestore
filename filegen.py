import os
import subprocess
from multiprocessing import Pool
import time

def generate_big_random_bin_file(filename):
    """
    generate big binary file with the specified size in bytes
    :param filename: the filename
    """
    size = 1024*1024
    with open('%s'%filename, 'wb') as fout:
        fout.write(os.urandom(size)) #1

    print ('big random binary file with size %f generated ok'%size)
    pass

def generate_file_ldeedee(level3Name, lvl3FileNum, level4Name, level4Num, lvl4FileNum, level5Name, level5Num, lvl5FileNum, root):

    level3Path = os.path.join(root, level3Name)
    print ("paths level 3: %s " %level3Path)
    for num in range(1, lvl3FileNum +1):
        fileName = "testfile" + str(num) + ".txt"
        filePath = os.path.join(level3Path, fileName)
        cmd = "/home/acheong/vsnapperf/ldeedee if=/dev/randhigh of=\"" + filePath + "\" bs=8k count=4"
        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            time.sleep(0.5)
        if p.returncode != 0:
            print(p.stdout.read())

    for num in range(1, level4Num + 1):
        level4Path = os.path.join(level3Path, level4Name + str(num))
        print ("paths level 4: \"%s\"" %level4Path)
        for num in range(1, lvl4FileNum +1):
            fileName = "testfile" + str(num) + ".txt"
            filePath = os.path.join(level4Path, fileName)
            cmd = "/home/acheong/vsnapperf/ldeedee if=/dev/randhigh of=\"" + filePath + "\" bs=8k count=4"
            print(cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while p.poll() is None:
                time.sleep(0.5)
            if p.returncode != 0:
                print(p.stdout.read())

        for num in range(1, level5Num + 1):
            level5Path = os.path.join(level4Path, level5Name + str(num))
            print("paths level 5: \"%s\"" %level5Path)
            print("Generating %s files" %lvl5FileNum)
            for num in range(1, lvl5FileNum +1):
                fileName = "testfile" + str(num) + ".txt"
                filePath = os.path.join(level5Path, fileName)
                cmd = "/home/acheong/vsnapperf/ldeedee if=/dev/randhigh of=\"" + filePath + "\" bs=8k count=4"
                print(cmd)
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while p.poll() is None:
                    time.sleep(0.5)
                if p.returncode != 0:
                    print(p.stdout.read())

def parallel_file_gen(level3Name, level3Num, lvl3FileNum, level4Name, level4Num, lvl4FileNum, level5Name, level5Num, lvl5FileNum, root):
    print("Parallel file creation")
    start = time.time()
    print("Time start: %s" %start)

    parallelArgs = create_args(level3Name, level3Num, lvl3FileNum, level4Name, level4Num, lvl4FileNum, level5Name, level5Num, lvl5FileNum, root)

    with Pool(8) as p:
        p.starmap(generate_file_ldeedee, parallelArgs)

    end = time.time()
    print("Time end: %s" %end)
    elapsed = end - start
    print("Time elapsed: %s" %elapsed)

def test_parallel_file_gen(x):
    print("testing parallel file creation")
    start = time.time()
    print("Time start: %s" %start)
    with Pool(5) as p:
        p.map(generate_big_random_bin_file, ["testfile0.txt", "testfile1.txt", "testfile2.txt", "testfile3.txt", "testfile4.txt", "testfile5.txt", "testfile6.txt", "testfile7.txt", "testfile8.txt", "testfile9.txt"])
        #print (p.map(multi_process_file_gen,[1,2,3]))

    end = time.time()
    print("Time end: %s" %end)
    elapsed = end - start

    print("Time elapsed: %s" %elapsed)

def test_sequential_file_gen():
    print("testing sequential file creation")
    start = time.time()
    print("Time start: %s" %start)

    arr = ["testfile0.txt", "testfile1.txt", "testfile2.txt", "testfile3.txt", "testfile4.txt"]
    for file in arr:
        generate_big_random_bin_file(file)

    end = time.time()
    print("Time end: %s" %end)
    elapsed = end - start

    print("Time elapsed: %s\n\n" %elapsed)

def create_args(level3Name, level3Num, lvl3FileNum, level4Name, level4Num, lvl4FileNum, level5Name, level5Num, lvl5FileNum, root):
    staticArgs = (lvl3FileNum, level4Name, level4Num, lvl4FileNum, level5Name, level5Num, lvl5FileNum, root)

    parallelArgs = []

    for num in range(1,level3Num+1):
        tupleBuild = (level3Name + str(num),)
        tupleBuild += staticArgs
        parallelArgs.append(tupleBuild)
    print(parallelArgs)

    return parallelArgs

def create_args2():

    parallelArgs = []

    tupleBuild1 = ("/vz9/Level3-1", 312500)
    tupleBuild2 = ("/vz9/Level3-1/Level4-1", 312500)
    tupleBuild3 = ("/vz9/Level3-1/Level4-2", 312500)
    tupleBuild4 = ("/vz9/Level3-1/Level4-1/Level5-1", 312500)
    tupleBuild5 = ("/vz9/Level3-1/Level4-2/Level5-1", 312500)

    parallelArgs.append(tupleBuild1)
    parallelArgs.append(tupleBuild2)
    parallelArgs.append(tupleBuild3)
    parallelArgs.append(tupleBuild4)
    parallelArgs.append(tupleBuild5)
    print(parallelArgs)

    return parallelArgs

def parallel_file_gen2():
    print("Parallel file creation")
    start = time.time()
    print("Time start: %s" %start)

    parallelArgs = create_args2()

    with Pool(8) as p:
        p.starmap(generate_file_ldeedee_unique, parallelArgs)

    end = time.time()
    print("Time end: %s" %end)
    elapsed = end - start
    print("Time elapsed: %s" %elapsed)

def generate_file_ldeedee_unique(root, fileNum):

    for num in range(1, fileNum +1):
        fileName = "testfile" + str(num) + ".txt"
        filePath = os.path.join(root, fileName)
        cmd = "/home/acheong/vsnapperf/ldeedee if=/dev/randhigh of=\"" + filePath + "\" bs=8k count=4"
        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            time.sleep(0.5)

        if p.returncode != 0:
            print(p.stdout.read())

if __name__ == '__main__':
    #if=/dev/randhigh of=/vsnap/vpool1/vz6/testfile1.txt bs=16k count=2
    root = "/vsnap/vpool1/vz8"
    level3Name = "Level3-"
    level3Num = 1
    lvl3FileNum = 312500
    level4Name = "Level4-"
    level4Num = 2
    lvl4FileNum = 312500
    level5Name = "Level5-"
    level5Num = 1
    lvl5FileNum = 312500

    #generate_big_random_bin_file("testfile.txt", 1024*1024)
    #parallel_file_gen(level3Name, level3Num, lvl3FileNum, level4Name, level4Num, lvl4FileNum, level5Name, level5Num, lvl5FileNum, root)
    #generate_file_ldeedee_unique(/vz9/)
    s = parallel_file_gen2()
    print(s)
    #test_parallel_file_gen("s")



"""
        root = "/vsnap/vpool1/vz6"
        level3Name = "Level3-"
        level3Num = 64
        lvl3FileNum = 1953125
        level4Name = "Level4-"
        level4Num = 128
        lvl4FileNum = 2197266
        level5Name = "Level5-"
        level5Num = 256
        lvl5FileNum = 1464844"""
