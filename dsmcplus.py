#Main script
import argparse, os, sys, errno, time

from bundler import Bundler
from dsmcbackup import DsmcBackup
from unbundler import Unbundler
from dsmcrestore import DsmcRestore
from parallelmgmt import ParallelMgmt
from metadatajson import MetadataJson
from stats import Stats

def dsmcplus():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['backup', 'restore'], help='backup to tsm server or restore to filer')
    parser.add_argument('source', help='source path to backup or restore')
    parser.add_argument('destination', help='destination path to backup or restore')
    parser.add_argument('optfile', help='option file path')
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
    #Init bundler object
    bundler = Bundler(args.source, args.destination, args.optfile)

    dest_path = bundler.create_vol()

    #update the destination path with new volume path
    bundler.dest_path = dest_path

    if args.scratch:
        print("filer to scratch only")
        dir_list, total_size = bundler.get_all_dirs()

        proc_obj, elapsed = ParallelMgmt.parallel_proc(bundler, dir_list, args.mode, int(args.parallelism))

        bundler.parallel_bundler(proc_obj, total_size, dir_list[0], elapsed)
        bundler.delete_bundle()
        sys.exit()

    if args.dsmc:
        print("scratch to dsmc only")
        dsmc_backup = DsmcBackup(dest_path, args.resourceutilization)
        dsmc_backup.backup()
        sys.exit()

    start = time.time()
    dir_list, total_size = bundler.get_all_dirs()

    proc_obj, elapsed = ParallelMgmt.parallel_proc(bundler, dir_list, args.mode, int(args.parallelism))

    total_throughput = bundler.parallel_bundler(proc_obj, total_size, dir_list[0], elapsed)

    dsmc_backup = DsmcBackup(dest_path, args.resourceutilization)
    transfer_rate = dsmc_backup.backup()

    bundler.delete_bundle()
    end = time.time()

    total_elapsed_time = end-start
    Stats.overall_stats(total_elapsed_time, transfer_rate, total_throughput)
    '''transfer_rate_mib = float(transfer_rate)/1024

    aggregate = (total_throughput + transfer_rate_mib)/2

    #add total_throughput with dsmc transfer and divide by 2 for total throughput
    print("Total Elapsed Time: %s" %total_elapsed_time)
    print("Total Aggregate transfer rate: %s" %aggregate)'''

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

    start = time.time()
    unbundler = Unbundler(args.source, args.destination, args.optfile)
    source_path = unbundler.create_vol()

    #update the destination path with new volume path
    unbundler.src_path = source_path

    dsmc_restore = DsmcRestore(unbundler.src_path)
    transfer_rate = dsmc_restore.restore()

    #data = metadatajson.deserialize_json(json_file_path)
    #unbundler = Unbundler(unbundler.src_path, args.destination)
    restore_list = unbundler.get_all_volume()
    #restore_list = get_restore_list(data)
    if len(restore_list) == 0:
        print("No files were found to restore")
        sys.exit()

    unbundle_list = unbundler.build_list(restore_list)
    proc_obj, elapsed = ParallelMgmt.parallel_proc(unbundler, unbundle_list, args.mode, int(args.parallelism))
    total_throughput = unbundler.parallel_unbundle(proc_obj, args.parallelism, elapsed)

    unbundler.delete_bundle()

    end = time.time()

    total_elapsed_time = end - start
    Stats.overall_stats(total_elapsed_time, transfer_rate, total_throughput)
    '''transfer_rate_mib = float(transfer_rate)/1024

    aggregate = (total_throughput + transfer_rate_mib)/2

    #add total_throughput with dsmc transfer and divide by 2 for total throughput
    print("Total Elapsed Time: %s" %total_elapsed_time)
    print("Total Aggregate transfer rate: %s" %aggregate)'''

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
    if os.path.exists(args.optfile):
        print("Option file path: %s" %args.optfile)
    else:
        print("Option file path is not valid: %s" %args.optfile)
        sys.exit()

if __name__ == '__main__':
    dsmcplus()

    #python3 dsmcplus.py backup /Users/andy/Documents/tester/ /Users/andy/Documents/tester/ /Users/andy/Documents/tester/optfile.json -p 16 -r 10 -s
    #python3 dsmcplus.py backup /vz9/vz8 /scale01/scratch/ /scale01/scratch/optfile.json -p 16 -r 10
    #python3 dsmcplus.py restore /scale01/scratch/ / /scale01/scratch/optfile.json -p 16

    #python3 dsmcplus.py restore /scale01/scratch/ /vz9 -p 8
    #python3 dsmcplus.py backup /vz8 /scale01/scratch/ -p 8
