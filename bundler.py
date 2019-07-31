import os
import sys
import time
from shutil import copy
from multiprocessing import Pool
import subprocess
from os.path import join, getsize
from metadatajson import MetadataJson
from stats import Stats
import json

metadatajson = MetadataJson()

def get_all_dirs(src_path, dest_path):
    print("\nget a list of all the files that needs to be backed up")
    print("path: %s" %src_path)
    start = time.time()
    dir_list = []
    set_list = []
    multi_set = []
    dir_size = 0
    total_size = 0

    for root, dirs, files in os.walk(src_path):
        for dir in dirs:
            dir_path=os.path.join(root, dir)

            for file in os.listdir(dir_path):
                file_path=os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    dir_size += os.path.getsize(file_path)

            set_list.append(dir_path)
            set_list.append(dest_path)
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

def get_dir_size(dir_path):
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

def parallel_bundler(dir_list, total_size, procs):
    print("\nStarting parallel bundler")
    start = time.time()
    data = {}
    star_file_arr = []
    total_data_transferred = 0
    with Pool(procs) as p:
        proc_obj = p.map(bundled_func, dir_list)

    for star_file_data, stat in proc_obj:
        star_file_arr.append(star_file_data)
        stat.display_stats_bundle()
        total_data_transferred += stat.star_size

    end = time.time()
    elapsed = end - start


    data['total_size'] = total_size
    data['star_files'] = star_file_arr

    total_data_transferred_mib = total_data_transferred/1024/1024
    total_throughput = total_data_transferred_mib/elapsed
    day_normalization = elapsed/86400
    tb_normalization = total_data_transferred_mib/1000000
    days = day_normalization*15

    normalization_throughput = tb_normalization / days

    goal_throughput = 25/15
    print("\nTotal Time elapsed (sec): %s" %elapsed)
    print("Total data transferred (MiB): " + str(total_data_transferred_mib))
    print("Aggregate Throughput (MiB/sec): " + str(total_throughput))

    print("Normalize day: " + str(day_normalization))
    print("Normalize tb: " + str(tb_normalization))
    print("Normalize throughput (TB/15days): " + str(normalization_throughput))
    print("Goal: " + str(goal_throughput))
    print("\nCreating json metadata file")
    metadatajson.write_to_file(data, dir_list[0])
    print("Done.")

def bundled_func(dir_list):
    stat = Stats()
    start = time.time()

    cmd, elapsed_proc_time, tar_path = bundle_file_set(dir_list[0], dir_list[1])

    end = time.time()
    elapsed = end - start
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

def bundle_file_set(src_path, dest_path):
    print("bundle the file set into tar")

    static_tar_name = "vzStar"
    unique_name = static_tar_name + str(time.time()) + ".star"

    tar_name_str = "\ntarname: %s" %unique_name
    tar_path = os.path.join(dest_path, unique_name)
    cmd = "time star -c -f \"" + tar_path + "\" fs=32m bs=64K pat=*.* " + src_path + "/*.*"
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


def log_progress():
    print("calculate progress")

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

    main(sys.argv[1:])
