
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
        self.process_id = 0

    def capture_stats(self, elapsed_time, star_size, file_count, star_name, process_id):
        self.elapsed_time = elapsed_time
        self.star_size = star_size
        self.file_count = file_count
        self.star_name = star_name
        self.process_id = process_id

    def display_stats(self):
        display_message = ""

        print(display_message)

    
