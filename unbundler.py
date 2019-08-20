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
            total_data_transferred += stat.star_size

        Stats.display_total_stats(total_data_transferred, elapsed)

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

        cmd, bundle_size, elapsed_proc = Unbundler.unbundle(unbundle_list[0], unbundle_list[1])
        #delete_message = Unbundler.delete_star(unbundle_list[0])

        end = time.time()
        elapsed = end - start
        stat.capture_stats(elapsed_proc, bundle_size, 0, "", 0, cmd)

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

        return cmd, bundle_size, elapsed

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
        #bundle_size = 1000
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
        star_files_arr = data['star_files']

        for star_file_data in star_files_arr:
            restore_list.append(star_file_data['name'])

        return restore_list

    def get_all_volume(self):
        '''
            Get a list of all star files that needs to be restored for a volume

            Returns:
                restore_list    -- List with full path of all archive files
        '''
        restore_list = []
        restore_list = glob.glob(os.path.join(self.src_path, "*.star"))
        print(restore_list)
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
        except OSError as e: # this would be "except OSError, e:" before Python 2.6
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred

    def create_vol(self):
        optfiledata = MetadataJson.deserialize_json(self.optfile)
        group = optfiledata['group']
        filer = optfiledata['filer']
        volume = optfiledata['volume']
        path = os.path.join(self.src_path, group, filer, volume)
        print(path)
        return path

'''
def main(argv):
    #json file
    #dest
    #parallel process #
    if len(argv) < 2:
        print("Not enough arguments. Need at least two arguments.")
        print("Syntax: python3 unbundler.py <json file> <dest path>")
        sys.exit()
    if len(argv) > 3:
        print("Too many arguments. Need at least two arguments.")
        print("Syntax: python3 unbundler.py <json file> <dest path>")
        sys.exit()
    if len(argv) != 3:
        print("Using default number of parallelism: 8")
        print("Syntax: python3 unbundler.py <json file> <dest path> <parallel process>")
        procs = 8
    else:
        procs = argv[2]

    try:
        int(procs)
    except ValueError:
        print("Third value needs to be an integer")
        sys.exit()

    json_file_path = argv[0]
    dest_path = argv[1]

    if os.path.isfile(json_file_path):
        print("Json file : %s" %json_file_path)
    else:
        print("Json file path is not valid: %s" %json_file_path)
        sys.exit()
    if os.path.isdir(dest_path):
        print("Destination Path: %s" %dest_path)
    else:
        print("Destination path is not valid: %s" %dest_path)
        sys.exit()

    print("Using parallelism: " + str(procs))

    data = metadatajson.deserialize_json(json_file_path)

    restore_list = get_restore_list(data)
    unbundle_list = build_list(restore_list, dest_path)
    parallel_unbundle(unbundle_list, int(procs))

if __name__ == '__main__':
    print("starting restore script\n")

    main(sys.argv[1:])
'''
