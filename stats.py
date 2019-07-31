
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

    def calculate_throughput(self, star_size, elapsed_time):
        return ""

    def calculate_size_gb(self, star_size):
        self.star_size = star_size/1024/1024/1024

    def capture_stats(self, elapsed_time, star_size, file_count, star_name, process_id, cmd):
        self.elapsed_time = elapsed_time
        self.star_size = star_size
        self.file_count = file_count
        self.star_name = star_name
        self.process_id = process_id
        size_mib = star_size/1024/1024
        throughput = size_mib / elapsed_time
        self.throughput = throughput
        self.cmd = cmd

    def display_stats(self):
        result_str = "\nResults:"
        size_str = "\nSize of tar director in GiB: " + str(self.star_size/1024/1024/1024)
        elapsed_str = "\nTime elapsed per process: %s" %self.elapsed_time
        throughput_str = "\nThroughput (MiB/sec): " + str(self.throughput)
        display_message = result_str + self.cmd + size_str + elapsed_str + throughput_str
        print(display_message)
