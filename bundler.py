import os, sys, time, errno
import json, subprocess
from shutil import copy, rmtree
from multiprocessing import Pool

from os.path import join, getsize
from metadatajson import MetadataJson
from stats import Stats


metadatajson = MetadataJson()

class Bundler():
    ''' Bundler class
        Bundles files into .star files from filer to scratch space
        Currently: Uses directories to bundle to decrease the count of files
        Bundle: grouping large amount of files together to get archived
        Star: linux unique standard tape archiver
    '''

    def __init__(self, src_path, dest_path, optfile):
        '''
            Initialize Bundler object

            Instance Variable:
                src_path    -- The filer path containing volumes/files that need to be backed up
                dest_path   -- The scratch path where the bundled files will be sent to
        '''
        self.src_path = src_path
        self.dest_path = dest_path
        self.optfile = optfile
        self.size = 0

    def get_all_dirs(self):
        '''
            Prepares a list of directories that will be bundled

            Returns
                dir_list    -- list of directories
                total_size  -- the total size of data that will be backed up
        '''
        print("\nget a list of all the dirs that needs to be backed up")
        print("path: %s" %self.src_path)
        start = time.time()
        dir_list = []
        set_list = []
        multi_set = []
        dir_size = 0
        total_size = 0

        for root, dirs, files in os.walk(self.src_path):
            for dir in dirs:
                dir_path=os.path.join(root, dir)

                for file in os.listdir(dir_path):
                    file_path=os.path.join(dir_path, file)
                    if os.path.isfile(file_path):
                        dir_size += os.path.getsize(file_path)

                set_list.append(dir_path)
                set_list.append(self.dest_path)
                set_list.append(dir_size)
                dir_list.append(set_list)
                set_list = []
                total_size += dir_size
                dir_size = 0

        end = time.time()
        elapsed = end - start
        print("Time to gather all files: %s" %elapsed)
        print("Got all dirs and size")
        return dir_list, total_size

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

    @classmethod
    def parallel_bundler(self, proc_obj, total_size, path, elapsed):
        '''
            Conducts the bundle function in parallel
            Displays results of the bundle process
            A json file is created containing metadata that were archived
            The json file can be used to backup specific directories

            Arguments:
                dir_list    -- list of directories that will be bundled
                total_size  -- the total size of data that will be backed up
                                used to calculate results
                proc        -- Number of processor used to perform bundling
        '''

        data = {}
        star_file_arr = []
        total_data_transferred = 0

        for star_file_data, stat in proc_obj:
            star_file_arr.append(star_file_data)
            stat.display_stats_bundle()
            total_data_transferred += stat.star_size

        data['total_size'] = total_size
        data['star_files'] = star_file_arr

        Stats.display_total_stats(total_data_transferred, elapsed)

        print("\nCreating json metadata file")
        metadatajson.write_to_file(data, path)
        print("Done.")

    def bundled_func(self, dir_list):
        '''
            Function called in parallel_bundler() which gives it an array containing
            src_path and dest_path
            Generates json object and captures stats of each process

            Arguments:
                dir_list        -- Array containing src_path and dest_path

            Returns:
                star_file_data  -- Json object of archive file
                stat            -- Stat object of the process
        '''
        stat = Stats()
        start = time.time()
        backup_list = []
        bundle_size = 0
        cmd, elapsed_proc_time, tar_path = Bundler.bundle_file_set(dir_list[0], dir_list[1])

        end = time.time()
        elapsed = end - start

        backup_list.append(tar_path)
        self.size += Bundler.get_bundle_size(tar_path)
        print("BUNDLE")
        print(self.size)

        #if bundle_size >= 20000000000:
            #print("LIST")
            #print (backup_list)
            #bundle_size = 0

        star_file_data = {}
        volume_path_arr = []

        star_file_data['name'] = tar_path
        star_file_data['size'] =  dir_list[2]
        star_file_data['volume_paths'] = volume_path_arr
        volume_path_arr.append(dir_list[0])

        size_mib = dir_list[2]/1024/1024
        size_gib = size_mib/1024

        throughput = size_mib / elapsed_proc_time

        stat.capture_stats(elapsed_proc_time, dir_list[2], 0, tar_path, 0, cmd)

        return  star_file_data, stat

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

        print("bundle the file set into tar")

        static_tar_name = "vzStar"
        unique_name = static_tar_name + str(time.time()) + ".star"

        tar_name_str = "\ntarname: %s" %unique_name
        tar_path = os.path.join(dest_path, unique_name)
        cmd = "time star -c -f \"" + tar_path + "\" fs=32m bs=64K pat=*.* " + src_path + "/*.*"

        #cmd = "ls -l " + src_path

        start = time.time()

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while p.poll() is None:
            time.sleep(0.5)

        if p.returncode != 0:
            print(p.stdout.read())

        end = time.time()


        elapsed_proc_time = end - start
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

    def create_vol(self):
        optfiledata = MetadataJson.deserialize_json(self.optfile)
        group = optfiledata['group']
        filer = optfiledata['filer']
        volume = optfiledata['volume']
        path = os.path.join(self.dest_path, group, filer, volume)
        print(path)
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
        return path

    def delete_bundle(self):
        '''
            Delete all archive files from scratch once backup is complete

            Arguments:
                src         -- Archive file Path

            Returns:
                message     -- Message display whether files were deleted or not
        '''
        try:
            rmtree(self.dest_path)
            message = "\nDeleted bundle: " + self.dest_path
        except OSError as e: # this would be "except OSError, e:" before Python 2.6
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred
'''
def main(argv):
    #src
    #dest
    #parallel process #
    if len(argv) < 2:
        print("Not enough arguments. Need at least two arguments.")
        print("Syntax: python3 bundler.py <src path> <dest path>")
        sys.exit()
    if len(argv) > 3:
        print("Too many arguments. Need at least two arguments.")
        print("Syntax: python3 bundler.py <src path> <dest path>")
        sys.exit()
    if len(argv) != 3:
        print("Using default number of parallelism: 8")
        print("Syntax: python3 bundler.py <src path> <dest path> <parallel process>")
        procs = 8
    else:
        procs = argv[2]

    try:
        int(procs)
    except ValueError:
        print("Third value needs to be an integer")
        sys.exit()

    src_path = argv[0]
    dest_path = argv[1]

    if os.path.isdir(src_path):
        print("Source Path: %s" %src_path)
    else:
        print("Source path is not valid: %s" %src_path)
        sys.exit()
    if os.path.isdir(dest_path):
        print("Destination Path: %s" %dest_path)
    else:
        print("Destination path is not valid: %s" %dest_path)
        sys.exit()

    print("Using parallelism: " + str(procs))

    dir_list, total_size = get_all_dirs(src_path, dest_path)
    parallel_bundler(dir_list, total_size, int(procs))

if __name__ == '__main__':
    print("starting script\n")

    main(sys.argv[1:])'''
