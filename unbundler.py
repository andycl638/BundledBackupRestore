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

    def __init__(self, src_path, dest_path):
        '''
            Initialize Unbundler object

            Instance Variable:
                src_path    -- The archive file path in scratch containing star
                               files that need to be extracted
                dest_path   -- The filer path where the extracted files will be sent to
        '''

        self.src_path = src_path
        self.dest_path = dest_path

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

    def parallel_unbundle(self, proc_obj, elapsed):
        '''
            Conducts the unbundle function in parallel
            Displays agregate results of the bundle process

        Arguments:
            unbundle_list       -- list of archive files that will be extracted
            proc                -- Number of processor used to perform bundling
        '''
        total_data_transferred = 0

        for stat in proc_obj:
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

        proc_name = multiprocessing.current_process().name

        cmd, bundle_size, elapsed_proc, dest = Unbundler.unbundle(unbundle_list[0], unbundle_list[1])

        end = time.time()
  
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
            print(message)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
