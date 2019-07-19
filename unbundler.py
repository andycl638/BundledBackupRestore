import subprocess
import os
import time
from os.path import getsize
from multiprocessing import Pool

def build_list(src_list, dest):
    print("building out list to unbundle")
    unbundle_list = []
    temp = []
    for src in src_list:
        temp.append(src)
        temp.append(dest)
        unbundle_list.append(temp)
        temp = []
    print(unbundle_list)
    return unbundle_list

def parallel_unbundle(unbundle_list):
    print("\nStarting parallel unbundler")
    start = time.time()

    with Pool(16) as p:
        messages = p.map(unbundle_func, unbundle_list)

    for message in messages:
        print(message)

    end = time.time()
    elapsed = end - start
    print("Total Time elapsed: %s" %elapsed)

def unbundle_func(unbundle_list):
    start = time.time()

    cmd, bundle_size = unbundle(unbundle_list[0], unbundle_list[1])

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

    message = result_str + cmd_str + bundle_size_str + throughput_str + elapsed_str
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

    print (out)
    return cmd, bundle_size

def get_bundle_size(src):
    bundle_size = os.path.getsize(src)

    return bundle_size

if __name__ == '__main__':
    src_list = ["sd","sdsd","12d"]
    unbundle_list = build_list(src_list, "/vz8")
    parallel_unbundle(unbundle_list)
    #unbundle(src_list, "/vz8")
