import multiprocessing as mp
import time
import os

def producer(queue):
    print("Producer")
    start = time.time()
    dir_list = []
    set_list = []
    src_path = '/vz6'

    for root, dirs, files in os.walk(src_path):
        set_list.append(root)
        set_list.append('/scratch')

        dir_list.append(set_list)
        set_list = []
        if len(dir_list) == 10:
            queue.put(dir_list)
            dir_list = []

    #adding remaining dirs to queue
    if len(dir_list) != 0:
        queue.put(dir_list)
        dir_list = []

    #poisonpill
    if len(dir_list) == 0:
        queue.put(None)

    print("No more dirs")
    end = time.time()
    elapsed = end - start
    print("Time to gather all files: %s" %elapsed)

def consumer(queue):
    print("Consumer")
    while True:
        list = queue.get()
        print(list)

        if list is None:
            print("list is none")
            break

        try:
            with mp.Pool(8) as pool:
                proc_obj = pool.map(bundle_func, list)
            print(proc_obj)
        finally:
            print("enter finally")
            queue.task_done()
        #print(len(queue))

def bundle_func(list):
    src_path = list[0]
    dest_path = list[1]
    static_tar_name = "vzStar"
    unique_name = static_tar_name + str(time.time()) + ".star"

    tar_name_str = "\ntarname: %s" %unique_name
    tar_path = os.path.join(dest_path, unique_name)
    cmd = "time star -c -f \"" + tar_path + "\" fs=32m bs=64K pat=*.* " + src_path + "/*.*"
    print('\n' + cmd)
    return "done"

if __name__ == '__main__':
    start = time.time()
    with mp.Pool(3) as pool:
        data_q = mp.JoinableQueue()
        p = pool.Process(target=consumer, args=(data_q, ))
        c = pool.Process(target=producer, args=(data_q, ))
        c.start()
        p.start()

        p.join()
        c.join()
    end = time.time()

    elapsed = end-start
    print('END')
    print(elapsed)
