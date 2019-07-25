import subprocess
import sys
import os
import time
from os.path import getsize
from multiprocessing import Pool
from metadatajson import MetadataJson

metadatajson = MetadataJson()

def build_list(src_list, dest):
    print("building out list to unbundle")

    unbundle_list = []
    temp = []
    for src in src_list:
        temp.append(src)
        temp.append(dest)
        unbundle_list.append(temp)
        temp = []

    return unbundle_list

def parallel_unbundle(unbundle_list, procs):
    print("\nStarting parallel unbundler")
    start = time.time()

    with Pool(procs) as p:
        messages = p.map(unbundle_func, unbundle_list)

    for message in messages:
        print(message)

    end = time.time()
    elapsed = end - start
    print("Total Time elapsed: %s" %elapsed)

def unbundle_func(unbundle_list):
    start = time.time()

    cmd, bundle_size = unbundle(unbundle_list[0], unbundle_list[1])
    delete_message = delete_star(unbundle_list[0])

    end = time.time()
    elapsed = end - start

    bundle_size_mib = bundle_size/1024/1024
    bundle_size_gib = bundle_size_mib/1024
    throughput = bundle_size_mib / elapsed

    result_str = "\nResults:"
    cmd_str = "\nUnbundle cmd: %s" %cmd
    bundle_size_str = "\nSize of bundle: " + str(bundle_size_gib)
    throughput_str = "\nThroughput (MiB/sec): " + str(throughput)
    elapsed_str = "\nTime elapsed per process: %s" %elapsed

    message = result_str + cmd_str + bundle_size_str + throughput_str + delete_message + elapsed_str
    return message

def unbundle(src, dest):

    bundle_size = get_bundle_size(src)

    cmd = "star -x -v -f " + src

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=dest)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

    out, err = p.communicate()

    #print (out)
    return cmd, bundle_size

def get_bundle_size(src):
    bundle_size = os.path.getsize(src)

    return bundle_size

def get_restore_list(data):
    restore_list = []
    star_files_arr = data['star_files']

    for star_file_data in star_files_arr:
        restore_list.append(star_file_data['name'])

    return restore_list

def delete_star(src):
    try:
        os.remove(src)
        message = "\nDeleted star: " + src
    except:
        message = "\nError while deleting file: " + src
    return message

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
