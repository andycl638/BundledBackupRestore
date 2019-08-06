import sys
import os
import subprocess
import time
#Grab all .star files and backup to SP server using dsmc
#delete all .star files from scratch

class DsmcBackup():
    def __init__(self, backup_path):
        self.backup_path = backup_path

    def backup(self):

        cmd = "dsmc selective '" + self.backup_path + "*'"
        #cmd = "dsmc q v"
        #cmd = "netstat"
        print(cmd)

        start = time.time()
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)

        while True:
            out = p.stderr.read(1)
            if out == '' and p.pool() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()
        print ("dsmc: finished")

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
