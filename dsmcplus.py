#Main script
import argparse
import os
import sys
from bundler import Bundler
from dsmcbackup import DsmcBackup
from unbundler import Unbundler
from dsmcrestore import DsmcRestore

def dsmcplus():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['backup', 'restore'], help='backup to tsm server or restore to filer')
    parser.add_argument('source', help='source path to backup or restore')
    parser.add_argument('destination', help='destination path to backup or restore')
    parser.add_argument('-p', '--parallelism', type=int, default=4, help='number of processor used to backup or restore')
    parser.add_argument('-r', '--resourceutilization', type=int, help='dsmc backup sessions controlled by resource utilization ')
    parser.add_argument('-b', '--bundlersize', type=int, help='Average size in Gb of each bundler being backup to dsmc')

    '''TESTING PARAMETERS'''
    parser.add_argument('-s', '--scratch', action='store_true', help='run backup or restore to scratch space only')
    parser.add_argument('-d', '--dsmc', action='store_true', help='run backup or restore to dsmc only')
    parser.add_argument('-t', '--test', action='store_true', help='run os cmd')


    args = parser.parse_args()

    print("mode: " + args.mode)
    if args.mode == 'backup':

        if os.path.isdir(args.source):
            print("Source Path: %s" %args.source)
        else:
            print("Source path is not valid: %s" %args.source)
            sys.exit()
        if os.path.isdir(args.destination):
            print("Destination Path: %s" %args.destination)
        else:
            print("Destination path is not valid: %s" %args.destination)
            sys.exit()

        if args.scratch:
            print("filer to scratch only")
            bundler = Bundler(args.source, args.destination, args.test)

            dir_list, total_size = bundler.get_all_dirs()
            bundler.parallel_bundler(dir_list, total_size, int(args.parallelism))
            sys.exit()

        if args.dsmc:
            print("scratch to dsmc only")
            dsmc_backup = DsmcBackup(args.destination, args.test)
            dsmc_backup.backup()
            sys.exit()

        bundler = Bundler(args.source, args.destination, args.test)

        dir_list, total_size = bundler.get_all_dirs()
        bundler.parallel_bundler(dir_list, total_size, int(args.parallelism))

        dsmc_backup = DsmcBackup(args.destination, args.test)
        dsmc_backup.backup()


    elif args.mode == 'restore':
        if os.path.isdir(args.source):
            print("Source Path: %s" %args.source)
        else:
            print("Source path is not valid: %s" %args.source)
            sys.exit()
        if os.path.isdir(args.destination):
            print("Destination Path: %s" %args.destination)
        else:
            print("Destination path is not valid: %s" %args.destination)
            sys.exit()

        if args.dsmc:
            print("restore dsmc to scratch")
            dsmc_restore = DsmcRestore(args.source, args.test)
            dsmc_restore.restore()
            sys.exit()

        if args.scratch:
            print("restore scratch to filer")
            #data = metadatajson.deserialize_json(json_file_path)
            unbundler = Unbundler(args.source, args.destination, args.test)
            restore_list = unbundler.get_all_volume()
            #restore_list = get_restore_list(data)
            if len(restore_list) == 0:
                print("No files were found to restore")
                sys.exit()

            unbundle_list = unbundler.build_list(restore_list)
            unbundler.parallel_unbundle(unbundle_list, args.parallelism)
            sys.exit()


        dsmc_restore = DsmcRestore(args.source, args.test)
        dsmc_restore.restore()

        #data = metadatajson.deserialize_json(json_file_path)
        unbundler = Unbundler(args.source, args.destination, args.test)
        restore_list = unbundler.get_all_volume()
        #restore_list = get_restore_list(data)
        if len(restore_list) == 0:
            print("No files were found to restore")
            sys.exit()

        unbundle_list = unbundler.build_list(restore_list)
        unbundler.parallel_unbundle(unbundle_list, args.parallelism)

if __name__ == '__main__':
    dsmcplus()

    #python3 dsmcplus.py backup /Users/andy/Documents/tester/ /Users/andy/Documents/tester/ -p 16 -t
    #python3 dsmcplus.py restore /Users/andy/Documents/tester/ /Users/andy/Documents/tester/ -p 16 -t

    #python3 dsmcplus.py restore /scale01/scratch/ /vz8 -p 8
    #python3 dsmcplus.py backup /vz8 /scale01/scratch/ -p 8
