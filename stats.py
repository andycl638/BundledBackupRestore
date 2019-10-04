import time

class Stats:
    '''
        This class is used to capture statistics of each process for backup and restore
    '''

    def __init__(self):
        '''
            initialize Stats
        '''
        self.elapsed_time = 0
        self.bundled_size = 0
        self.file_count = 0
        self.bundled_name = ""
        self.throughput = 0
        self.process_id = 0
        self.cmd = ""
        self.dest = ""

    def calculate_throughput(self, bundled_size, elapsed_time):
        return ""

    def calculate_size_gb(self, bundled_size):
        self.bundled_size = bundled_size/1024/1024/1024

    def capture_stats(self, elapsed_time, bundled_size, file_count, bundled_name, process_id, cmd, dest):
        self.elapsed_time = elapsed_time
        self.bundled_size = bundled_size
        self.file_count = file_count
        self.bundled_name = bundled_name
        self.process_id = process_id
        size_mib = bundled_size/1024/1024
        throughput = size_mib / elapsed_time
        self.throughput = throughput
        self.cmd = cmd
        self.dest = dest

    def display_stats_bundle(self):
        process = "\nBundling with process: " + self.process_id
        time = "\nTimestamp: " + time.ctime()
        result_str = "\nResults:"
        size_str = "\nSize of tar director in GiB: " + str(self.bundled_size/1024/1024/1024)
        elapsed_str = "\nTime elapsed per process: %s" %self.elapsed_time
        throughput_str = "\nThroughput (MiB/sec): " + str(self.throughput)
        display_message = process + time + result_str + self.cmd + size_str + elapsed_str + throughput_str
        print(display_message)

    def display_stats_unbundle(self):
        process = "\nBundling with process: " + self.process_id
        time = "\nTimestamp: " + time.ctime()
        result_str = "\nResults:"
        cmd_str = "\nUnbundle cmd: %s" %self.cmd
        dest_str = "\nDestination Path: %s" %self.dest
        bundle_size_str = "\nSize of bundle: " + str(self.bundled_size/1024/1024/1024)
        elapsed_str = "\nTime elapsed per process: %s" %self.elapsed_time
        throughput_str = "\nThroughput (MiB/sec): " + str(self.throughput)
        display_message = process + time + result_str + cmd_str + dest_str + bundle_size_str + throughput_str  + elapsed_str
        print(display_message)

    @staticmethod
    def display_total_stats(total_data_transferred, elapsed):
        total_data_transferred_mib = total_data_transferred/1024/1024
        total_throughput = total_data_transferred_mib/elapsed

        print("\nTotal Time elapsed (sec): %s" %elapsed)
        print("Total data transferred (MiB): " + str(total_data_transferred_mib))
        print("Aggregate Throughput (MiB/sec): " + str(total_throughput))

        Stats.display_gib_stats(total_data_transferred_mib, elapsed)

        return total_throughput, total_data_transferred_mib

    @staticmethod
    def display_gib_stats(total_data_transferred_mib, elapsed_sec):
        print('\nNormalize to GiB and Hours')
        gib = total_data_transferred_mib/1024
        hr = elapsed_sec/60/60
        total_throughput = gib/hr

        print("\nTotal Time elapsed (Hr): %s" %hr)
        print("Total data transferred (GiB): " + str(gib))
        print("Aggregate Throughput (GiB/Hr): " + str(total_throughput))
        print('\n')

    @staticmethod
    def overall_stats(total_elapsed_time, transfer_rate, total_throughput):
        transfer_rate_mib = float(transfer_rate)/1024
        aggregate = (total_throughput + transfer_rate_mib)/2

        print("Total Elapsed Time: %s" %total_elapsed_time)
        print("Total Aggregate transfer rate: %s" %aggregate)
        return aggregate

    @staticmethod
    def overall_backup_stats(elapsed, aggregate):
        print("Total Elapsed Time: %s" %elapsed)
        print("Aggregate transfer rate (MiB/sec): %s" %aggregate)

    @staticmethod
    def normalize_gib(elapsed, aggregate):
        print('Normalize to GiB and Hours')
        convert_to_gib = aggregate/1024
        print('Aggregate in GiB: ' + str(convert_to_gib))
        convert_to_hr = elapsed/60/60
        print('Hour: ' + str(convert_to_hr))


    @staticmethod
    def poc_proof(elapsed, aggregate):
        print('POC PROOF')
        convert_to_tib = aggregate/1024/1024
        print('Aggregate in TiB: ' + str(convert_to_tib))
        convert_to_day = elapsed/60/60/24
        print('Time as Day: ' + str(convert_to_day))

        tib_goal = convert_to_tib * 25
        time_goal = convert_to_day * 15
        transfer_rate_goal = tib_goal/time_goal

        print('Aggregate in TiB (25TB): ' + str(tib_goal))
        print('Time as Days (15): ' + str(time_goal))
        print('Transfer rate (25TiB/15day): ' + str(transfer_rate_goal))
