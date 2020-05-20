import os, sys, time, errno
import json, subprocess, multiprocessing
from shutil import copy, rmtree
from multiprocessing import Pool

from os.path import join, getsize
from metadatajson import MetadataJson
from stats import Stats
from externalcommand import ExternalCommand


metadatajson = MetadataJson()

class Bundler():
    ''' Bundler class
        Bundles files into .star files from filer to scratch space
        Currently: Uses directories to bundle to decrease the count of files
        Bundle: grouping large amount of files together to get archived
        Star: linux unique standard tape archiver
    '''

    def __init__(self, src_path, dest_path):
        '''
            Initialize Bundler object

            Instance Variable:
                src_path    -- The filer path containing volumes/files that need to be backed up
                dest_path   -- The scratch path where the bundled files will be sent to
        '''
        self.src_path = src_path
        self.dest_path = dest_path
    
   
    def get_dirs(self):
        '''
            Prepares a list of directories to search for changed files

            Returns
                dir_list    -- list of directories
        '''
        print("\nget a list of all the dirs that needs to be backed up")
        print("path: %s" %self.src_path)
        start = time.time()
        dir_list = []

        for root, dirs, files in os.walk(self.src_path):
            dir_list.append(root)

        end = time.time()
        elapsed = end - start
        print("Time to gather all files: %s" %elapsed)
        return dir_list

    def bundle_func(self, dir_list):
        '''
            Function called in parallel_bundler() which gives it an array containing
            src_path and dest_path
            Generates json object and captures stats of each process

            Arguments:
                dir_list           -- Array containing src_path and dest_path

            Returns:
                bundled_file_data  -- Json object of archive file
                stat               -- Stat object of the process
        '''
        stat = Stats()
        start = time.time()
        proc_name = multiprocessing.current_process().name

        cmd, elapsed_proc_time, tar_path = Bundler.bundle_file_set(dir_list[0], dir_list[1])

        end = time.time()
        elapsed = end - start

        tar_size = Bundler.get_bundle_size(tar_path)

        bundled_file_data = {}

        stat.capture_stats(elapsed_proc_time, tar_size, 0, tar_path, proc_name, cmd, "", end)

        return  bundled_file_data, stat, tar_path

    @staticmethod
    def bundle_file_set(src_path, dest_path):
        '''
            Runs subprocess cmd to archive a directory to the destination path

            Arguments:
                src_path            -- directory path that will be archived
                dest_path           -- path where the archive file will be sent

            Returns:
                message_cmd         -- Archive command string
                elapsed_proc_time   -- The elapsed time of the subprocess cmd
                tar_path            -- The archived file path
        '''
        static_tar_name = "vzStar"
        unique_name = static_tar_name + str(time.time()) + ".star"

        tar_name_str = "\ntarname: %s" %unique_name
        tar_path = os.path.join(dest_path, unique_name)
        cmd = "time star -c -f \"" + tar_path + "\" fs=32m bs=64K pat=*.* " + src_path + "/*.*"

        elapsed_proc_time = ExternalCommand.ext_cmd(cmd, None)

        message_cmd = tar_name_str + "\n" + cmd
        return message_cmd, elapsed_proc_time, tar_path

    @staticmethod
    def incr_bundle_set(files, dest_path):
        '''
            Runs subprocess cmd to archive a directory to the destination path

            Arguments:
                files               -- list of file that have a ctime greater than backup time
                dest_path           -- path where the archive file will be sent

            Returns:
                message_cmd         -- Archive command string
                elapsed_proc_time   -- The elapsed time of the subprocess cmd
                tar_path            -- The archived file path
        '''

        print("bundle the file set into tar")

        static_tar_name = "vzStar"
        unique_name = static_tar_name + str(time.time()) + ".star"

        tar_name_str = "\ntarname: %s" %unique_name
        tar_path = os.path.join(dest_path, unique_name)
        file_bundle = ''
        for file in files:
            file_bundle = file_bundle + ' ' + file

        cmd = "time star -c -f \"" + tar_path + "\" fs=32m bs=64K" + file_bundle

        elapsed_proc_time = ExternalCommand.ext_cmd(cmd, None)

        message_cmd = tar_name_str + "\n" + cmd
        return message_cmd, elapsed_proc_time, tar_path

    @staticmethod
    def get_bundle_size(src):
        '''
            Get the size of each archive file

            Arguments:
                src             -- Archive file path

            Returns:
                bundle_size     -- size of Archive file in bytes
        '''
        bundle_size = os.path.getsize(src)
        return bundle_size

    def delete_bundle(self):
        '''
            Delete all archive files from scratch once backup is complete

            Arguments:
                self         -- get destination path

            Returns:
                message     -- Message display whether files were deleted or not
        '''
        try:
            rmtree(self.dest_path)
            message = "\nDeleted bundle: " + self.dest_path
            print(message)
        except OSError as e:
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred

    def delete_star(self):
        '''
            Delete all archive files from scratch once restore is complete

            Arguments:
                src         -- Archive file Path

            Returns:
                message     -- Message display whether files were deleted or not
        '''
        try:
            print(self.dest_path)
            bundle_list = os.listdir(self.dest_path)
            for bundle in bundle_list:
                if bundle.endswith('.star'):
                    os.remove(os.path.join(self.dest_path, bundle))

            message = "\nDeleted bundles in: " + self.dest_path
            print(message)
        except OSError as e:
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred
'''

    def get_dirs_tuple(self):

            Prepares a list of directories that will be bundled

            Returns
                dir_list    -- tuple with source dir and destination

        print("\nget a list of all the dirs that needs to be backed up")
        print("path: %s" %self.src_path)
        start = time.time()
        dir_list = []
        set_list = []

        for root, dirs, files in os.walk(self.src_path):
            set_list.append(root)
            set_list.append(self.dest_path)
            dir_list.append(set_list)
            set_list = []

        end = time.time()
        elapsed = end - start
        print("Time to gather all files: %s" %elapsed)
        return dir_list

    @classmethod
    def parallel_bundler(self, proc_obj, total_size, path, elapsed):

            Conducts the bundle function in parallel
            Displays results of the bundle process
            A json file is created containing metadata that were archived
            The json file can be used to backup specific directories

            Arguments:
                dir_list    -- list of directories that will be bundled
                total_size  -- the total size of data that will be backed up
                                used to calculate results
                proc        -- Number of processor used to perform bundling


        data = {}
        bundled_file_arr = []
        total_data_transferred = 0

        for bundled_file_data, stat, tar_path in proc_obj:
            bundled_file_arr.append(bundled_file_data)
            stat.display_stats_bundle()
            total_data_transferred += stat.bundled_size

        data['total_size'] = total_size
        data['bundled_files'] = bundled_file_arr

        total_throughput = Stats.display_total_stats(total_data_transferred, elapsed)

        print("\nCreating json metadata file")
        metadatajson.write_to_file(data, path)
        print("Done.")
        return total_throughput

    def get_dir_size(self, dir_path):
        set_list = []

        dir_size = 0

        for file in os.listdir(dir_path):
            file_path=os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                dir_size += os.path.getsize(file_path)
            set_list.append(dir_path)
            set_list.append(dir_size)

        print(set_list)
        return set_list

    def scan_dir(src_path, dest_path, dir_list):
 
            Prepares a list of directories that will be bundled with os.scandir
            Recursively call itself until it gets all directories

            Arguments:
                src_path           -- path to scan
                dest_path          -- destination path added to tuple
                dir_list           -- tuple with source dir and destination


        set_list = []
        for entry in os.scandir(src_path):
            if entry.is_dir(follow_symlinks=False):
                set_list.append(entry.path)
                set_list.append(dest_path)
                dir_list.append(set_list)
                set_list = []
                yield from scan_scandir2(entry.path, dest_path, dir_list)

    def get_dirs_tuple(self):
        
            Prepares a list of directories that will be bundled

            Returns
                dir_list    -- tuple with source dir and destination
        
        print("path: %s" %self.src_path)
        start = time.time()
        dir_list = []
        set_list = []

        #addind the root path to the tuple
        set_list.append(self.src_path)
        set_list.append(self.dest_path)
        dir_list.append(set_list)

        #scan the given src_path for all directories
        for entry in scan_dir(self.src_path, self.dest_path, dir_list):
            print(entry)

        end = time.time()
        elapsed = end - start
        print("Time to gather all files: %s" %elapsed)
        return dir_list


'''
