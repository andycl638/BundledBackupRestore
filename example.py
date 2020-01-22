import subprocess, sys, os, time, glob, errno, multiprocessing
from os.path import getsize
from multiprocessing import Pool

from stats import Stats
from shutil import rmtree

from externalcommand import ExternalCommand
from metadatajson import MetadataJson

metadatajson = MetadataJson()

class Unbundler():
    '''
        Unbundler class
        Unbundles files into .star files from filer to scratch space
        Unbundle: extract archived files to filer
        Star: linux unique standard tape archiver
    '''

    def __init__(self, src_path, dest_path, optfile):
        '''
            Initialize Unbundler object

            Instance Variable:
                src_path    -- The archive file path in scratch containing star
                               files that need to be extracted
                dest_path   -- The filer path where the extracted files will be sent to
        '''

        self.src_path = src_path
        self.dest_path = dest_path
        self.optfile = optfile

    def build_list(self, src_list):
        '''
            Build a consumable list of archive files that will be extracted to filer

            Arguments:
                src_list        -- list of all archive files that will be extracted

            Returns:
                unbundle_list   -- tuple containing src and destination path for extracting files
        '''

        print("building out list to unbundle")

        unbundle_list = []
        temp = []
        for src in src_list:
            temp.append(src)
            temp.append(self.dest_path)
            unbundle_list.append(temp)
            temp = []

        return unbundle_list

    def parallel_unbundle(self, obj, procs, elapsed):
        '''
            Conducts the unbundle function in parallel
            Displays agregate results of the bundle process

        Arguments:
            unbundle_list       -- list of archive files that will be extracted
            proc                -- Number of processor used to perform bundling
        '''
        total_data_transferred = 0

        for stat in obj:
            stat.display_stats_unbundle()
            total_data_transferred += stat.bundled_size

        total_throughput = Stats.display_total_stats(total_data_transferred, elapsed)
        return total_throughput

    @classmethod
    def unbundle_func(self, unbundle_list):
        '''
            Function called in parallel_unbundler() which gives it an array containing
            src_path and dest_path
            Captures stats of each process

            Arguments:
                unbundle_list       -- Array containing src_path and dest_path

            Returns:
                stat                -- Stat object of the process
        '''
        stat = Stats()
        start = time.time()
        proc_name = multiprocessing.current_process().name

        cmd, bundle_size, elapsed_proc, dest = Unbundler.unbundle(unbundle_list[0], unbundle_list[1])
        #delete_message = Unbundler.delete_star(unbundle_list[0])

        end = time.time()
        elapsed = end - start
        stat.capture_stats(elapsed_proc, bundle_size, 0, "", proc_name, cmd, dest, end)

        return stat

    @classmethod
    def unbundle(self, src, dest):
        '''
            Runs subprocess cmd to extract data from the archive file back to the filer

            Arguments:
                src             -- Archive file path
                dest            -- Filer path

            Returns:
                cmd             -- extract cmd in string form
                bundle_size     -- size of Archive file in bytes
                elapsed         -- The elapsed time of the subprocess cmd
        '''
        print("unbundle the tar into filer")
        bundle_size = Unbundler.get_bundle_size(src)

        cmd = "star -x -v -f " + src

        elapsed = ExternalCommand.ext_cmd(cmd, dest)

        return cmd, bundle_size, elapsed, dest

    @classmethod
    def get_bundle_size(self, src):
        '''
            Get the size of each archive file

            Arguments:
                src             -- Archive file path

            Returns:
                bundle_size     -- size of Archive file in bytes
        '''
        bundle_size = os.path.getsize(src)
        return bundle_size

    def get_restore_list(self, data):
        '''
            get a list of star files from json obj
            This list can be used to restore back to filer

            Arguments:
                data            -- json object used to gather all paths of archive files

            Returns:
                restore_list    -- List with full path of all archive files
        '''
        restore_list = []
        bundled_files_arr = data['bundled_files']

        for bundled_file_data in bundled_files_arr:
            restore_list.append(bundled_file_data['name'])

        return restore_list

    def get_all_volume(self):
        '''
            Get a list of all star files that needs to be restored for a volume

            Returns:
                restore_list    -- List with full path of all archive files
        '''
        restore_list = []

        for root, dirs, files in os.walk(self.src_path):
            for name in files:
                if name.lower().endswith('.star'):
                    restore_list.append(os.path.join(root,name))

        #print(restore_list)
        return restore_list

    @classmethod
    def delete_star(self, src):
        '''
            Delete all archive files from scratch once restore is complete

            Arguments:
                src         -- Archive file Path

            Returns:
                message     -- Message display whether files were deleted or not
        '''
        try:
            #os.remove(src)
            message = "\nDeleted star: " + src
        except:
            message = "\nError while deleting file: " + src
        return message

    def delete_bundle(self):
        '''
            Delete all archive files from scratch once restore is complete

            Arguments:
                src         -- Archive file Path

            Returns:
                message     -- Message display whether files were deleted or not
        '''
        try:
            rmtree(self.src_path)
            message = "\nDeleted bundle: " + self.src_path
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def create_vol(self):
        optfiledata = MetadataJson.deserialize_json(self.optfile)
        group = optfiledata['group']
        path = os.path.join(self.src_path, group)
        print(path)
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
        return path

'''

time star -x -f /scratch/v1_1_2_20190603_161730.star > /scratch/rest1.txt &
time star -x -f /scratch/v1_3_4_20190603_161730.star > /scratch/rest2.txt &
time star -x -f /scratch/v1_4_6_20190603_161730.star > /scratch/rest3.txt &
time star -x -f /scratch/v1_7_8_20190603_161730.star > /scratch/rest4.txt &



Bundle TEST 1
bundle
time star -c -f /scale01/scratch/stars/test2.star fs=32m bs=64K /vz7/test/ > /scale01/scratch/results/bundle1.txt

Unbundle TEST 1
mkdir /vz7/unbundle1

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt

cd /vz7 && rm -rf /vz7/unbundle*

Unbundle TEST 2
mkdir /vz7/unbundle1 /vz7/unbundle2

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt

rm -rf /vz7/unbundle*

Unbundle TEST 3
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt

rm -rf /vz7/unbundle*

Unbundle TEST 5
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3 /vz7/unbundle4 /vz7/unbundle5

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz7/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz7/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt


rm -rf /vz7/unbundle*

Unbundle TEST 8
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3 /vz7/unbundle4 /vz7/unbundle5 /vz7/unbundle6 /vz7/unbundle7 /vz7/unbundle8

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz7/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz7/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz7/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz7/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz7/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt

cd /vz7
rm -rf /vz7/unbundle*

Unbundle TEST 10
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3 /vz7/unbundle4 /vz7/unbundle5 /vz7/unbundle6 /vz7/unbundle7 /vz7/unbundle8 /vz7/unbundle9 /vz7/unbundle10

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz7/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz7/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz7/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz7/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz7/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz7/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz7/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt

cd /vz7
rm -rf /vz7/unbundle*

Unbundle TEST 13
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3 /vz7/unbundle4 /vz7/unbundle5 /vz7/unbundle6 /vz7/unbundle7 /vz7/unbundle8 /vz7/unbundle9 /vz7/unbundle10 /vz7/unbundle11 /vz7/unbundle12 /vz7/unbundle13

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz7/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz7/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz7/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz7/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz7/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz7/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz7/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz7/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz7/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz7/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt

cd /vz7
rm -rf /vz7/unbundle1 &
rm -rf /vz7/unbundle2 &
rm -rf /vz7/unbundle3 &
rm -rf /vz7/unbundle4 &
rm -rf /vz7/unbundle5 &
rm -rf /vz7/unbundle6 &
rm -rf /vz7/unbundle7 &
rm -rf /vz7/unbundle8 &
rm -rf /vz7/unbundle9 &
rm -rf /vz7/unbundle10 &
rm -rf /vz7/unbundle11 &
rm -rf /vz7/unbundle12 &
rm -rf /vz7/unbundle13 &
rm -rf /vz7/unbundle14 &
rm -rf /vz7/unbundle15 &
rm -rf /vz7/unbundle16 &
rm -rf /vz7/unbundle17 &
rm -rf /vz7/unbundle18 &
rm -rf /vz7/unbundle19 &
rm -rf /vz7/unbundle20

cd vz7
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
rm -rf unbundle20


Unbundle TEST 16
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3 /vz7/unbundle4 /vz7/unbundle5 /vz7/unbundle6 /vz7/unbundle7 /vz7/unbundle8 /vz7/unbundle9 /vz7/unbundle10 /vz7/unbundle11 /vz7/unbundle12 /vz7/unbundle13 /vz7/unbundle14 /vz7/unbundle15 /vz7/unbundle16

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz7/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz7/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz7/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz7/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz7/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz7/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz7/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz7/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz7/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz7/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz7/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz7/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz7/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt

cd /vz7
rm -rf /vz7/unbundle*


Unbundle TEST 20
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3 /vz7/unbundle4 /vz7/unbundle5 /vz7/unbundle6 /vz7/unbundle7 /vz7/unbundle8 /vz7/unbundle9 /vz7/unbundle10 /vz7/unbundle11 /vz7/unbundle12 /vz7/unbundle13 /vz7/unbundle14 /vz7/unbundle15 /vz7/unbundle16 /vz7/unbundle17 /vz7/unbundle18 /vz7/unbundle19 /vz7/unbundle20

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz7/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz7/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz7/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz7/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz7/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz7/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz7/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz7/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz7/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz7/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz7/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz7/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz7/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt &
cd /vz7/unbundle17 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle17.txt &
cd /vz7/unbundle18 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle18.txt &
cd /vz7/unbundle19 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle19.txt &
cd /vz7/unbundle20 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle20.txt

cd /vz7


Unbundle TEST 20
mkdir /vz7/unbundle1 /vz7/unbundle2 /vz7/unbundle3 /vz7/unbundle4 /vz7/unbundle5 /vz7/unbundle6 /vz7/unbundle7 /vz7/unbundle8 /vz7/unbundle9 /vz7/unbundle10 /vz7/unbundle11 /vz7/unbundle12 /vz7/unbundle13 /vz7/unbundle14 /vz7/unbundle15 /vz7/unbundle16 /vz7/unbundle17 /vz7/unbundle18 /vz7/unbundle19 /vz7/unbundle20 /vz7/unbundle21 /vz7/unbundle22 /vz7/unbundle23 /vz7/unbundle24 /vz7/unbundle25

cd /vz7/unbundle1 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle1.txt &
cd /vz7/unbundle2 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle2.txt &
cd /vz7/unbundle3 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle3.txt &
cd /vz7/unbundle4 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle4.txt &
cd /vz7/unbundle5 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle5.txt &
cd /vz7/unbundle6 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle6.txt &
cd /vz7/unbundle7 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle7.txt &
cd /vz7/unbundle8 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle8.txt &
cd /vz7/unbundle9 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle9.txt &
cd /vz7/unbundle10 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle10.txt &
cd /vz7/unbundle11 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle11.txt &
cd /vz7/unbundle12 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle12.txt &
cd /vz7/unbundle13 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle13.txt &
cd /vz7/unbundle14 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle14.txt &
cd /vz7/unbundle15 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle15.txt &
cd /vz7/unbundle16 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle16.txt &
cd /vz7/unbundle17 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle17.txt &
cd /vz7/unbundle18 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle18.txt &
cd /vz7/unbundle19 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle19.txt &
cd /vz7/unbundle20 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle20.txt &
cd /vz7/unbundle21 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle21.txt &
cd /vz7/unbundle22 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle22.txt &
cd /vz7/unbundle23 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle23.txt &
cd /vz7/unbundle24 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle24.txt &
cd /vz7/unbundle25 && time star -x -v -f /scale01/scratch/stars/test.star > /scale01/scratch/results/unbundle25.txt

cd /vz7
'''
