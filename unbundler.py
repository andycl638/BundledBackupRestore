import subprocess, sys, os, time, glob, errno
from os.path import getsize
from multiprocessing import Pool
from metadatajson import MetadataJson
from stats import Stats
from shutil import rmtree

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

        cmd, bundle_size, elapsed_proc, dest = Unbundler.unbundle(unbundle_list[0], unbundle_list[1])
        #delete_message = Unbundler.delete_star(unbundle_list[0])

        end = time.time()
        elapsed = end - start
        stat.capture_stats(elapsed_proc, bundle_size, 0, "", 0, cmd, dest)

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

        '''cmd = "ls -l " + src'''
        start = time.time()
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=dest)

        while p.poll() is None:
            time.sleep(0.5)

        if p.returncode != 0:
            print(p.stdout.read())

        end = time.time()
        elapsed = end - start

        out, err = p.communicate()

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
