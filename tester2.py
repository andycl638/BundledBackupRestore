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
    stat = os.stat(path)
    print(stat)
    print("Created: %s" % time.ctime(stat.st_ctime))

if __name__ == '__main__':
    #get_file_time('/Users/andy/Documents/tester/test.txt')
    #get_file_time('/vz9/test.txt')
    lista = [1 ,2 ,3, 4]
    listb = [1,2,3,4,5]
    print(list(set(listb) - set(lista)))

    time = "Timestamp: " + time.ctime()
    print (time)




'''
Restoring   7,516,258,304 /scale01/scratch/group2/filer1/vz8/vzStar1570115926.2015986.star [Done]
Restoring   7,516,258,304 /scale01/scratch/group2/filer1/vz8/vzStar1570115926.2015986.star [Done]

Restoring   7,516,258,304 /scale01/scratch/group2/filer1/vz8/vzStar1570115926.2012866.star [Done]
Restoring   7,516,258,304 /scale01/scratch/group2/filer1/vz8/vzStar1570115926.2012866.star [Done]'''

'''

time star -x -f /scratch/v1_1_2_20190603_161730.star > /scratch/rest1.txt &
time star -x -f /scratch/v1_3_4_20190603_161730.star > /scratch/rest2.txt &
time star -x -f /scratch/v1_4_6_20190603_161730.star > /scratch/rest3.txt &
time star -x -f /scratch/v1_7_8_20190603_161730.star > /scratch/rest4.txt &



Bundle TEST 1
bundle
time star -c -f /scale01/scratch/stars/test2.star fs=32m bs=64K /vz8/test/ > /scale01/scratch/results/bundle1.txt

Unbundle TEST 1
mkdir /vz8/unbundle1

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt

cd /vz8 && rm -rf /vz8/unbundle*

Unbundle TEST 2
mkdir /vz8/unbundle1 /vz8/unbundle2

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt

rm -rf /vz8/unbundle*

Unbundle TEST 3
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt

rm -rf /vz8/unbundle*

Unbundle TEST 5
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt


rm -rf /vz8/unbundle*

Unbundle TEST 8
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt

cd /vz8
rm -rf /vz8/unbundle*

Unbundle TEST 10
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8 /vz8/unbundle9 /vz8/unbundle10

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz8/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz8/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt

cd /vz8
rm -rf /vz8/unbundle*

Unbundle TEST 13
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8 /vz8/unbundle9 /vz8/unbundle10 /vz8/unbundle11 /vz8/unbundle12 /vz8/unbundle13

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz8/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz8/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz8/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz8/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz8/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt

cd /vz8
rm -rf /vz8/unbundle1 &
rm -rf /vz8/unbundle2 &
rm -rf /vz8/unbundle3 &
rm -rf /vz8/unbundle4 &
rm -rf /vz8/unbundle5 &
rm -rf /vz8/unbundle6 &
rm -rf /vz8/unbundle7 &
rm -rf /vz8/unbundle8 &
rm -rf /vz8/unbundle9 &
rm -rf /vz8/unbundle10 &
rm -rf /vz8/unbundle11 &
rm -rf /vz8/unbundle12 &
rm -rf /vz8/unbundle13 &
rm -rf /vz8/unbundle14 &
rm -rf /vz8/unbundle15 &
rm -rf /vz8/unbundle16 &
rm -rf /vz8/unbundle17 &
rm -rf /vz8/unbundle18 &
rm -rf /vz8/unbundle19 &
rm -rf /vz8/unbundle20

cd vz8
rm -rf unbundle1 &
rm -rf unbundle2 &
rm -rf unbundle3 &
rm -rf unbundle4 &
rm -rf unbundle5 &
rm -rf unbundle6 &
rm -rf unbundle7 &
rm -rf unbundle8 &
rm -rf unbundle9 &
rm -rf unbundle10 &
rm -rf unbundle11 &
rm -rf unbundle12 &
rm -rf unbundle13 &
rm -rf unbundle14 &
rm -rf unbundle15 &
rm -rf unbundle16 &
rm -rf unbundle17 &
rm -rf unbundle18 &
rm -rf unbundle19 &
rm -rf unbundle20 &
rm -rf unbundle21 &
rm -rf unbundle22 &
rm -rf unbundle23 &
rm -rf unbundle24 &
rm -rf unbundle25 &
rm -rf unbundle26 &
rm -rf unbundle27 &
rm -rf unbundle28 &
rm -rf unbundle29 &
rm -rf unbundle30 &
rm -rf unbundle31 &
rm -rf unbundle32 &
rm -rf unbundle33 &
rm -rf unbundle34 &
rm -rf unbundle35 &
rm -rf unbundle36 &
rm -rf unbundle37 &
rm -rf unbundle38 &
rm -rf unbundle39 &
rm -rf unbundle40 &
rm -rf unbundle41 &
rm -rf unbundle42 &
rm -rf unbundle43 &
rm -rf unbundle44 &
rm -rf unbundle45 &
rm -rf unbundle46 &
rm -rf unbundle47 &
rm -rf unbundle48 &
rm -rf unbundle49 &
rm -rf unbundle50 &


Unbundle TEST 16
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8 /vz8/unbundle9 /vz8/unbundle10 /vz8/unbundle11 /vz8/unbundle12 /vz8/unbundle13 /vz8/unbundle14 /vz8/unbundle15 /vz8/unbundle16

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz8/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz8/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz8/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz8/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz8/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz8/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz8/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz8/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt

cd /vz8
rm -rf /vz8/unbundle*


Unbundle TEST 20
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8 /vz8/unbundle9 /vz8/unbundle10 /vz8/unbundle11 /vz8/unbundle12 /vz8/unbundle13 /vz8/unbundle14 /vz8/unbundle15 /vz8/unbundle16 /vz8/unbundle17 /vz8/unbundle18 /vz8/unbundle19 /vz8/unbundle20

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz8/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz8/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz8/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz8/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz8/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz8/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz8/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz8/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt &
cd /vz8/unbundle17 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle17.txt &
cd /vz8/unbundle18 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle18.txt &
cd /vz8/unbundle19 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle19.txt &
cd /vz8/unbundle20 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle20.txt

cd /vz8


Unbundle TEST 25
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8 /vz8/unbundle9 /vz8/unbundle10 /vz8/unbundle11 /vz8/unbundle12 /vz8/unbundle13 /vz8/unbundle14 /vz8/unbundle15 /vz8/unbundle16 /vz8/unbundle17 /vz8/unbundle18 /vz8/unbundle19 /vz8/unbundle20 /vz8/unbundle21 /vz8/unbundle22 /vz8/unbundle23 /vz8/unbundle24 /vz8/unbundle25

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz8/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz8/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz8/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz8/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz8/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz8/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz8/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz8/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt &
cd /vz8/unbundle17 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle17.txt &
cd /vz8/unbundle18 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle18.txt &
cd /vz8/unbundle19 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle19.txt &
cd /vz8/unbundle20 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle20.txt &
cd /vz8/unbundle21 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle21.txt &
cd /vz8/unbundle22 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle22.txt &
cd /vz8/unbundle23 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle23.txt &
cd /vz8/unbundle24 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle24.txt &
cd /vz8/unbundle25 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle25.txt

cd /vz8

Unbundle TEST 40
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8 /vz8/unbundle9 /vz8/unbundle10
mkdir /vz8/unbundle11 /vz8/unbundle12 /vz8/unbundle13 /vz8/unbundle14 /vz8/unbundle15 /vz8/unbundle16 /vz8/unbundle17 /vz8/unbundle18 /vz8/unbundle19
mkdir /vz8/unbundle20 /vz8/unbundle21 /vz8/unbundle22 /vz8/unbundle23 /vz8/unbundle24 /vz8/unbundle25 /vz8/unbundle26 /vz8/unbundle27 /vz8/unbundle28 /vz8/unbundle29
mkdir /vz8/unbundle30 /vz8/unbundle31 /vz8/unbundle32 /vz8/unbundle33 /vz8/unbundle34 /vz8/unbundle35 /vz8/unbundle36 /vz8/unbundle37 /vz8/unbundle38 /vz8/unbundle39 /vz8/unbundle40

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz8/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz8/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz8/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz8/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz8/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz8/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz8/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz8/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt &
cd /vz8/unbundle17 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle17.txt &
cd /vz8/unbundle18 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle18.txt &
cd /vz8/unbundle19 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle19.txt &
cd /vz8/unbundle20 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle20.txt &
cd /vz8/unbundle21 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle21.txt &
cd /vz8/unbundle22 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle22.txt &
cd /vz8/unbundle23 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle23.txt &
cd /vz8/unbundle24 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle24.txt &
cd /vz8/unbundle25 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle25.txt &
cd /vz8/unbundle26 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle26.txt &
cd /vz8/unbundle27 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle27.txt &
cd /vz8/unbundle28 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle28.txt &
cd /vz8/unbundle29 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle29.txt &
cd /vz8/unbundle30 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle30.txt &
cd /vz8/unbundle31 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle31.txt &
cd /vz8/unbundle32 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle32.txt &
cd /vz8/unbundle33 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle33.txt &
cd /vz8/unbundle34 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle34.txt &
cd /vz8/unbundle35 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle35.txt &
cd /vz8/unbundle36 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle36.txt &
cd /vz8/unbundle37 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle37.txt &
cd /vz8/unbundle38 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle38.txt &
cd /vz8/unbundle39 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle39.txt &
cd /vz8/unbundle40 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle40.txt

cd /vz8

Unbundle TEST 50
mkdir /vz8/unbundle1 /vz8/unbundle2 /vz8/unbundle3 /vz8/unbundle4 /vz8/unbundle5 /vz8/unbundle6 /vz8/unbundle7 /vz8/unbundle8 /vz8/unbundle9 /vz8/unbundle10 /vz8/unbundle11 /vz8/unbundle12 /vz8/unbundle13 /vz8/unbundle14 /vz8/unbundle15 /vz8/unbundle16 /vz8/unbundle17 /vz8/unbundle18 /vz8/unbundle19 /vz8/unbundle20 /vz8/unbundle21 /vz8/unbundle22 /vz8/unbundle23 /vz8/unbundle24 /vz8/unbundle25 /vz8/unbundle26 /vz8/unbundle27 /vz8/unbundle28 /vz8/unbundle29 /vz8/unbundle30 /vz8/unbundle31 /vz8/unbundle32 /vz8/unbundle33 /vz8/unbundle34 /vz8/unbundle35 /vz8/unbundle36 /vz8/unbundle37 /vz8/unbundle38 /vz8/unbundle39 /vz8/unbundle40 /vz8/unbundle41 /vz8/unbundle42 /vz8/unbundle43 /vz8/unbundle44 /vz8/unbundle45 /vz8/unbundle46 /vz8/unbundle47 /vz8/unbundle48 /vz8/unbundle49 /vz8/unbundle50

cd /vz8/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz8/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz8/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz8/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz8/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz8/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz8/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz8/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz8/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz8/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz8/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz8/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz8/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz8/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz8/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz8/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt &
cd /vz8/unbundle17 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle17.txt &
cd /vz8/unbundle18 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle18.txt &
cd /vz8/unbundle19 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle19.txt &
cd /vz8/unbundle20 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle20.txt &
cd /vz8/unbundle21 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle21.txt &
cd /vz8/unbundle22 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle22.txt &
cd /vz8/unbundle23 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle23.txt &
cd /vz8/unbundle24 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle24.txt &
cd /vz8/unbundle25 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle25.txt &
cd /vz8/unbundle26 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle26.txt &
cd /vz8/unbundle27 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle27.txt &
cd /vz8/unbundle28 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle28.txt &
cd /vz8/unbundle29 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle29.txt &
cd /vz8/unbundle30 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle30.txt &
cd /vz8/unbundle31 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle31.txt &
cd /vz8/unbundle32 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle32.txt &
cd /vz8/unbundle33 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle33.txt &
cd /vz8/unbundle34 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle34.txt &
cd /vz8/unbundle35 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle35.txt &
cd /vz8/unbundle36 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle36.txt &
cd /vz8/unbundle37 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle37.txt &
cd /vz8/unbundle38 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle38.txt &
cd /vz8/unbundle39 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle39.txt &
cd /vz8/unbundle40 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle40.txt &
cd /vz8/unbundle41 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle41.txt &
cd /vz8/unbundle42 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle42.txt &
cd /vz8/unbundle43 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle43.txt &
cd /vz8/unbundle44 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle44.txt &
cd /vz8/unbundle45 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle45.txt &
cd /vz8/unbundle46 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle46.txt &
cd /vz8/unbundle47 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle47.txt &
cd /vz8/unbundle48 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle48.txt &
cd /vz8/unbundle49 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle49.txt &
cd /vz8/unbundle50 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle50.txt

cd /vz8




time rsync -a --delete blanktest/ unbundle1/

time rsync -a --delete blanktest/ unbundle1/ &
time rsync -a --delete blanktest/ unbundle2/ &
time rsync -a --delete blanktest/ unbundle3/ &
time rsync -a --delete blanktest/ unbundle4/ &
time rsync -a --delete blanktest/ unbundle5/ &
time rsync -a --delete blanktest/ unbundle6/ &
time rsync -a --delete blanktest/ unbundle7/ &
time rsync -a --delete blanktest/ unbundle8/ &
time rsync -a --delete blanktest/ unbundle9/ &
time rsync -a --delete blanktest/ unbundle10/ &
time rsync -a --delete blanktest/ unbundle11/ &
time rsync -a --delete blanktest/ unbundle12/ &
time rsync -a --delete blanktest/ unbundle13/ &
time rsync -a --delete blanktest/ unbundle14/ &
time rsync -a --delete blanktest/ unbundle15/ &
time rsync -a --delete blanktest/ unbundle16/ &
time rsync -a --delete blanktest/ unbundle17/ &
time rsync -a --delete blanktest/ unbundle18/ &
time rsync -a --delete blanktest/ unbundle19/ &
time rsync -a --delete blanktest/ unbundle20/ &
time rsync -a --delete blanktest/ unbundle21/ &
time rsync -a --delete blanktest/ unbundle22/ &
time rsync -a --delete blanktest/ unbundle23/ &
time rsync -a --delete blanktest/ unbundle24/ &
time rsync -a --delete blanktest/ unbundle25/
'''
