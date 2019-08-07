from multiprocessing import Pool
import time

class ParallelMgmt():

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
        print("\nStarting parallel bundler")
        start = time.time()

        with Pool(procs) as p:
            if mode == 'backup':
                proc_obj = p.map(obj.bundled_func, list)
            elif mode == 'restore':
                proc_obj = p.map(obj.unbundle_func, list)

        end = time.time()
        elapsed = end - start
        return proc_obj
