#Main script
import argparse
import os
import sys
from bundler import Bundler
from dsmcbackup import DsmcBackup
from unbundler import Unbundler
from dsmcrestore import DsmcRestore
from parallelmgmt import ParallelMgmt

def dsmcplus():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['backup', 'restore'], help='backup to tsm server or restore to filer')
    parser.add_argument('source', help='source path to backup or restore')
    parser.add_argument('destination', help='destination path to backup or restore')
    #parser.add_argument('optfile', help='option file path')
    parser.add_argument('-p', '--parallelism', type=int, default=4, help='number of processor used to backup or restore')
    parser.add_argument('-r', '--resourceutilization', type=int, help='dsmc backup sessions controlled by resource utilization ')
    parser.add_argument('-b', '--bundlersize', type=int, help='Average size in Gb of each bundler being backup to dsmc')

    '''TESTING PARAMETERS'''
    parser.add_argument('-s', '--scratch', action='store_true', help='run backup or restore to scratch space only')
    parser.add_argument('-d', '--dsmc', action='store_true', help='run backup or restore to dsmc only')

    args = parser.parse_args()

    check_input(args)

    print("mode: " + args.mode)
    if args.mode == 'backup':
        mainbackup(args)

    elif args.mode == 'restore':
        mainrestore(args)

def mainbackup(args):
    if args.scratch:
        print("filer to scratch only")
        bundler = Bundler(args.source, args.destination)
        dir_list, total_size = bundler.get_all_dirs()

        proc_obj = ParallelMgmt.parallel_proc(bundler, dir_list, args.mode, int(args.parallelism))

        bundler.parallel_bundler(proc_obj, total_size, dir_list[0])
        sys.exit()

    if args.dsmc:
        print("scratch to dsmc only")
        dsmc_backup = DsmcBackup(args.destination, args.resourceutilization)
        dsmc_backup.backup()
        sys.exit()

    #optfiledata = metadatajson.deserialize_json(args.optfile)
    #volume = optfiledata['volume']
    #path = os.path.join(args.destination, volume)
    #print(path)
    #os.mkdir(path)
    #Init bundler object
    bundler = Bundler(args.source, args.destination)
    dir_list, total_size = bundler.get_all_dirs()

    proc_obj = ParallelMgmt.parallel_proc(bundler, dir_list, args.mode, int(args.parallelism))

    bundler.parallel_bundler(proc_obj, total_size, dir_list[0])

    dsmc_backup = DsmcBackup(args.destination, args.resourceutilization)
    dsmc_backup.backup()

def mainrestore(args):
    if args.dsmc:
        print("restore dsmc to scratch")
        dsmc_restore = DsmcRestore(args.source)
        dsmc_restore.restore()
        sys.exit()

    if args.scratch:
        print("restore scratch to filer")
        #data = metadatajson.deserialize_json(json_file_path)
        unbundler = Unbundler(args.source, args.destination)
        restore_list = unbundler.get_all_volume()
        #restore_list = get_restore_list(data)
        if len(restore_list) == 0:
            print("No files were found to restore")
            sys.exit()

        unbundle_list = unbundler.build_list(restore_list)
        proc_obj = ParallelMgmt.parallel_proc(unbundler, unbundle_list, args.mode, int(args.parallelism))
        unbundler.parallel_unbundle(proc_obj, args.parallelism)
        sys.exit()

    dsmc_restore = DsmcRestore(args.source)
    dsmc_restore.restore()

    #data = metadatajson.deserialize_json(json_file_path)
    unbundler = Unbundler(args.source, args.destination)
    restore_list = unbundler.get_all_volume()
    #restore_list = get_restore_list(data)
    if len(restore_list) == 0:
        print("No files were found to restore")
        sys.exit()

    unbundle_list = unbundler.build_list(restore_list)
    proc_obj = ParallelMgmt.parallel_proc(unbundler, unbundle_list, args.mode, int(args.parallelism))
    unbundler.parallel_unbundle(proc_obj, args.parallelism)

def check_input(args):
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
    '''if os.path.exists(args.optifle):
        print("Option file path: %s" %args.optifle)
    else:
        print("Option file path is not valid: %s" %args.optfile)
        sys.exit()'''

if __name__ == '__main__':
    dsmcplus()

    #python3 dsmcplus.py backup /Users/andy/Documents/tester/ /Users/andy/Documents/tester/ -p 16 -t
    #python3 dsmcplus.py restore /Users/andy/Documents/tester/ /Users/andy/Documents/tester/ -p 16 -t

    #python3 dsmcplus.py restore /scale01/scratch/ /vz9 -p 8
    #python3 dsmcplus.py backup /vz8 /scale01/scratch/ -p 8
