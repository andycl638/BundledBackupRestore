
class Stats:
    '''
        This class is used to capture statistics of each process for backup and restore
    '''

    def __init__(self):
        '''
            initialize Stats
        '''
        self.elapsed_time = 0
        self.star_size = 0
        self.file_count = 0
        self.star_name = ""
        self.throughput = 0
        self.process_id = 0
        self.cmd = ""
        self.dest = ""

    def calculate_throughput(self, star_size, elapsed_time):
        return ""

    def calculate_size_gb(self, star_size):
        self.star_size = star_size/1024/1024/1024

    def capture_stats(self, elapsed_time, star_size, file_count, star_name, process_id, cmd, dest):
        self.elapsed_time = elapsed_time
        self.star_size = star_size
        self.file_count = file_count
        self.star_name = star_name
        self.process_id = process_id
        size_mib = star_size/1024/1024
        throughput = size_mib / elapsed_time
        self.throughput = throughput
        self.cmd = cmd
        self.dest = dest

    def display_stats_bundle(self):
        result_str = "\nResults:"
        size_str = "\nSize of tar director in GiB: " + str(self.star_size/1024/1024/1024)
        elapsed_str = "\nTime elapsed per process: %s" %self.elapsed_time
        throughput_str = "\nThroughput (MiB/sec): " + str(self.throughput)
        display_message = result_str + self.cmd + size_str + elapsed_str + throughput_str
        print(display_message)

    def display_stats_unbundle(self):
        result_str = "\nResults:"
        cmd_str = "\nUnbundle cmd: %s" %self.cmd
        dest_str = "\nDestination Path: %s" %self.dest
        bundle_size_str = "\nSize of bundle: " + str(self.star_size/1024/1024/1024)
        elapsed_str = "\nTime elapsed per process: %s" %self.elapsed_time
        throughput_str = "\nThroughput (MiB/sec): " + str(self.throughput)
        display_message = result_str + cmd_str + dest_str + bundle_size_str + throughput_str  + elapsed_str
        print(display_message)

    @staticmethod
    def display_total_stats(total_data_transferred, elapsed):
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
        print("Goal throughput (25TB/15days): " + str(goal_throughput))

        return total_throughput

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
        print("Total Aggregate transfer rate: %s" %aggregate)

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
