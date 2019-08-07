import sys
import os
import subprocess
import time

#Grab all .star files and backup to SP server using dsmc
#delete all .star files from scratch

class DsmcBackup():
    def __init__(self, backup_path, resource_utilization, test):
        self.backup_path = backup_path
        self.resource_utilization = resource_utilization
        self.test = test

    def backup(self):


        cmd = "dsmc selective '" + self.backup_path + "*'" #-resourceutilization=10"
        #cmd = "dsmc selective '" + self.backup_path + "*' -resourceutilization=" + self.resource_utilization
        #cmd = "dsmc q v"
        '''if self.test:
            cmd = "ping google.com -c 3"'''

        print(cmd)

        start = time.time()
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

        while True:
            out = p.stderr.readline()
            if p.poll() != None:
                break

            sys.stdout.write(out.decode('utf-8'))
            sys.stdout.flush()

        print ("dsmc: finished")

        end = time.time()

        elapsed_proc_time = end - start

'''
def main(argv):
    #backup_path
    if len(argv) < 1:
        print("Not enough arguments. Need one arguments.")
        print("Syntax: python3 backupsp.py <backup path>")
        sys.exit()
    if len(argv) > 2:
        print("Too many arguments. Need one arguments.")
        print("Syntax: python3 backupsp.py <backup path>")
        sys.exit()

    backup_path = argv[0]

    if os.path.exists(backup_path):
        print("Backup Path: %s" %backup_path)
    else:
        print("Backup path is not valid: %s" %backup_path)
        sys.exit()

    DsmcBackup().backup_to_sp(backup_path)

if __name__ == '__main__':
    print("starting script\n")

    main(sys.argv[1:])'''
