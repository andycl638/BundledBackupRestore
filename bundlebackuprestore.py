#Main script
import argparse, os, sys, errno, time

from bundler import Bundler
from unbundler import Unbundler
from parallelmgmt import ParallelMgmt
from metadatajson import MetadataJson
from stats import Stats

metadatajson = MetadataJson()
def bundlebackuprestore():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['backup', 'incr', 'restore'], help='backup or restore data')
    parser.add_argument('source', help='source path of data to backup or restore')
    parser.add_argument('destination', help='destination path of data to backup or restore')
    parser.add_argument('-p', '--parallelism', type=int, default=20, help='number of processor used to backup or restore')

    args = parser.parse_args()

    check_input(args)

    print("Mode: " + args.mode)
    if args.mode == 'backup':
        mainbackup(args)
    elif args.mode == 'restore':
        mainrestore(args)
    #elif args.mode == 'incr':
        #mainincr(args)

def mainbackup(args):
    #Init bundler object
    bundler = Bundler(args.source, args.destination)

    start = time.time()

    controller = ParallelMgmt(int(args.parallelism), args.source, args.destination)

    backup_time = time.time()
    return_q, elapsed = controller.start_controller(bundler)

    aggregate = 0.0
    mib = 0
    #data = {}
    bundled_file_arr = []
    while not return_q.empty():
        results = return_q.get()
        aggregate = aggregate + results[0]
        mib = mib + results[1]

    bundler.delete_star()

    end = time.time()
    total_elapsed_time = end-start
    data = metadatajson.create_obj(backup_time, bundled_file_arr)

    print(total_elapsed_time)

 

def mainrestore(args):
    start = time.time()
    unbundler = Unbundler(args.source, args.destination)

    restore_list = unbundler.get_all_volume()
    #restore_list = get_restore_list(data)
    if len(restore_list) == 0:
        print("No files were found to restore")
        sys.exit()

    unbundle_list = unbundler.build_list(restore_list)
    proc_obj = ParallelMgmt.parallel_proc(unbundler, unbundle_list, args.mode, int(args.parallelism))

    end = time.time()
    total_elapsed_time = end-start

    unbundler.parallel_unbundle(proc_obj, total_elapsed_time)

'''
def mainincr(args):
    #Init bundler object
    bundler = Bundler(args.source, args.destination)

    dest_path, dsm_opt, virtual_mnt_pt = bundler.create_vol()

   
    #update the destination path with new volume path
    bundler.dest_path = dest_path

    start = time.time()

    metadata_file = metadatajson.get_metadata_file(dest_path)

    data = metadatajson.deserialize_json(metadata_file)

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

    aggregate = 0.0
    mib = 0

    bundler.delete_star()

    end = time.time()
    total_elapsed_time = end-start
'''
def check_input(args):
    print("\nInput Variables\n")
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
    print("Parallelism: %s" %args.parallelism)
  
    print("\n")


def set_parallelism(args):
    if args.parallelism == 0 or args.parallelism == None:
        print("using default value: 20")
        return 20
    return int(args.parallelism)

if __name__ == '__main__':
    bundlebackuprestore()

    #python3 bundlebackuprestore.py backup /Users/andy/Documents/tester/ /Users/andy/Documents/tester/ -p 16 -r 10 -s
    #python3 bundlebackuprestore.py backup /vz9/vz8 /scale01/scratch/  -p 16 -r 10
    #python3 bundlebackuprestore.py restore /scale01/scratch/ / -p 16

    #python3 bundlebackuprestore.py restore /scale01/scratch/ /vz9 -p 8
    #python3 bundlebackuprestore.py backup /vz8 /scale01/scratch/ -p 8

    #python3 bundlebackuprestore.py restore /scale01/scratch/ / -p 16
    #python3 bundlebackuprestore.py backup /vz8 /scale01/scratch/ -p 8 -r 10
