#Main script
import argparse, os, sys, errno, time

from bundler import Bundler
from unbundler import Unbundler
from dsmcwrapper import DsmcWrapper
from parallelmgmt import ParallelMgmt
from metadatajson import MetadataJson
from stats import Stats

metadatajson = MetadataJson()
def dsmcplus():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['backup', 'incr', 'restore'], help='backup to tsm server or restore to filer')
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
    elif args.mode == 'incr':
        mainincr(args)

def mainbackup(args):
    #Init bundler object
    bundler = Bundler(args.source, args.destination, args.optfile)

    dest_path, dsm_opt, virtual_mnt_pt = bundler.create_vol()

    #update the destination path with new volume path
    bundler.dest_path = dest_path

    start = time.time()

    controller = ParallelMgmt(int(args.parallelism), args.source, dest_path)
    dsmc = DsmcWrapper(dest_path, args.resourceutilization, dsm_opt, virtual_mnt_pt, '')
    backup_time = time.time()
    return_q, elapsed = controller.start_controller(bundler, dsmc)

    aggregate = 0.0
    mib = 0
    data = {}
    bundled_file_arr = []
    while not return_q.empty():
        results = return_q.get()
        aggregate = aggregate + results[0]
        mib = mib + results[1]
        for result in results[2]:
            bundled_file_arr.append(result)

    bundler.delete_star()

    end = time.time()
    total_elapsed_time = end-start
    data = metadatajson.create_obj(backup_time, bundled_file_arr)
    #data['bundled_files'] = bundled_file_arr
    #data['backup_time'] = backup_time

    print("\nCreating json metadata file")
    print("backup time: %s" % time.ctime(backup_time))
    metadatajson.write_to_file(data, bundler.dest_path)

    #Stats.overall_backup_stats(elapsed, aggregate)
    Stats.display_gib_stats(mib, elapsed)
    #Stats.normalize_gib(elapsed, aggregate)

def mainrestore(args):
    start = time.time()
    unbundler = Unbundler(args.source, args.destination, args.optfile)
    source_path = unbundler.create_vol()

    #update the destination path with new volume path
    unbundler.src_path = source_path

    dsmc = DsmcWrapper('', args.resourceutilization, '', '', unbundler.src_path)
    controller = ParallelMgmt(int(args.parallelism), args.destination, source_path)
    return_q, elapsed = controller.start_controller_res(unbundler, dsmc)
    aggregate = 0.0
    mib = 0
    while not return_q.empty():
        results = return_q.get()
        print (results)
        mib = mib + results

    Stats.display_gib_stats(mib, elapsed)
    #restore = dsmc.restore()
#    transfer_rate = dsmc.cmd(restore)

    #data = metadatajson.deserialize_json(json_file_path)
    #unbundler = Unbundler(unbundler.src_path, args.destination)
    #restore_list = unbundler.get_all_volume()
    #restore_list = get_restore_list(data)
    #if len(restore_list) == 0:
        #print("No files were found to restore")
        #sys.exit()

    #unbundle_list = unbundler.build_list(restore_list)
    #proc_obj, elapsed = ParallelMgmt.parallel_proc(unbundler, unbundle_list, args.mode, int(args.parallelism))
    #total_throughput = unbundler.parallel_unbundle(proc_obj, args.parallelism, elapsed)

    unbundler.delete_bundle()

    end = time.time()

    total_elapsed_time = end - start
    #aggregate = Stats.overall_stats(total_elapsed_time, transfer_rate, total_throughput)
    #Stats.poc_proof(total_elapsed_time, aggregate)

def mainincr(args):
    #Init bundler object
    bundler = Bundler(args.source, args.destination, args.optfile)

    dest_path, dsm_opt, virtual_mnt_pt = bundler.create_vol()

    dsmc = DsmcWrapper(dest_path, args.resourceutilization, dsm_opt, virtual_mnt_pt, '')
    #update the destination path with new volume path
    bundler.dest_path = dest_path

    start = time.time()

    metadata_file = metadatajson.get_metadata_file(dest_path)

    data = metadatajson.deserialize_json(metadata_file)
    #print(data)
    #controller = ParallelMgmt(int(args.parallelism), args.source, dest_path)
    #dsmc = DsmcWrapper(dest_path, args.resourceutilization, dsm_opt, virtual_mnt_pt, '')
    #return_q, elapsed = controller.start_controller(bundler, dsmc)
    backup_time = data['backup_time']
    print(time.ctime(backup_time))

    mod_files = []
    dir_list = bundler.get_dirs()
    for dir in dir_list:
        for file in os.listdir(dir):
            file_path = os.path.join(dir,file)
            if os.path.isfile(file_path):
                if os.path.getctime(file_path) > backup_time:
                    mod_files.append(file_path)
                    print(file_path)
                    print(time.ctime(os.path.getctime(file_path)))

    message_cmd, elapsed_proc_time, tar_path = Bundler.incr_bundle_set(mod_files, dest_path)
    backup = dsmc.backup(tar_path)

    transfer_rate = dsmc.cmd(backup)

    aggregate = 0.0
    mib = 0

    bundler.delete_star()

    end = time.time()
    total_elapsed_time = end-start

    #Stats.overall_backup_stats(elapsed, aggregate)
    #Stats.display_gib_stats(mib, elapsed)
    #Stats.normalize_gib(elapsed, aggregate)

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

    #python3 dsmcplus.py restore /scale01/scratch/ / /scale01/scratch/optfile.json -p 16
    #python3 dsmcplus.py backup /vz8 /scale01/scratch/ /scale01/scratch/optfile.json -p 8 -r 10
