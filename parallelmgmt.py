import multiprocessing as mp
import time, os
from stats import Stats
from metadatajson import MetadataJson

#metadatajson = MetadataJson()

class ParallelMgmt():

    def __init__(self, procs, src_path, dest_path):
        self.procs = procs
        self.src_path = src_path
        self.dest_path = dest_path

    def producer(self, queue):
        print("Producer")
        start = time.time()
        dir_list = []
        set_list = []

        for root, dirs, files in os.walk(self.src_path):
            set_list.append(root)
            set_list.append(self.dest_path)

            dir_list.append(set_list)
            set_list = []
            if len(dir_list) == self.procs:
                queue.put(dir_list)
                dir_list = []

        #adding remaining dirs to queue
        if len(dir_list) != 0:
            queue.put(dir_list)
            dir_list = []

        #poisonpill
        if len(dir_list) == 0:
            queue.put(None)

        #print("No more dirs")
        end = time.time()
        elapsed = end - start
        print("Time to gather all files: %s" %elapsed)
        return "producer done"

    def consumer(self, queue, bundler, dsmc, return_q):
        print("Consumer")
        backup_time = time.time()
        results = []
        while True:
            list = queue.get()
            print(list)

            if list is None:
                #print("list is none")
                break

            try:
                start = time.time()
                with mp.Pool(self.procs) as pool:
                    proc_obj = pool.map(bundler.bundle_func, list)

                end = time.time()
                elapsed = end - start
                backup_list = ''
                data = {}
                bundled_file_arr = []
                total_data_transferred = 0

                for bundled_file_data, stat, tar_path in proc_obj:
                    backup_list = backup_list + str(tar_path) + ' '
                    bundled_file_arr.append(bundled_file_data)
                    stat.display_stats_bundle()
                    total_data_transferred += stat.bundled_size

                data['bundled_files'] = bundled_file_arr
                data['backup_time'] = backup_time

                total_throughput, mib = Stats.display_total_stats(total_data_transferred, elapsed)
                dsmc.write_virtualmnt()
                backup = dsmc.backup(backup_list)

                #transfer_rate = dsmc.cmd(backup)
                transfer_rate = 10000
                transfer_rate_mib = float(transfer_rate)/1024
                aggregate = (total_throughput + transfer_rate_mib)/2

                results = (float(aggregate), mib, data)
                return_q.put(results)
            finally:
                queue.task_done()

    def start_controller(self, bundler, dsmc):
        start = time.time()
        return_q = mp.Queue()
        with mp.Pool(3) as pool:
            data_q = mp.JoinableQueue()
            c = pool.Process(target=ParallelMgmt.consumer, args=(self, data_q, bundler, dsmc, return_q, ))
            p = pool.Process(target=ParallelMgmt.producer, args=(self, data_q, ))
            c.start()
            p.start()

            p.join()
            c.join()
        end = time.time()

        elapsed = end-start
        return return_q, elapsed

    @staticmethod
    def parallel_proc(obj, list, mode, procs):
        '''
            Conducts the bundle function in parallel
            Displays results of the bundle process
            A json file is created containing metadata that were archived
            The json file can be used to backup specific directories

            Arguments:
                dir_list    -- list of directories that will be bundled
                total_size  -- the total size of data that will be backed up
                                used to calculate results
                proc        -- Number of processor used to perform bundling
        '''
        print("\nStarting parallel func")
        start = time.time()

        with mp.Pool(procs) as pool:
            if mode == 'backup':
                proc_obj = pool.map(obj.bundle_func, list)
            elif mode == 'restore':
                proc_obj = pool.map(obj.unbundle_func, list)

        end = time.time()
        elapsed = end - start
        return proc_obj, elapsed
