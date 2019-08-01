import sys
import os
import subprocess
import time
#Grab all .star files and backup to SP server using dsmc
#delete all .star files from scratch

class DsmcBackup():
    def backup_to_sp(self, backup_path):

        cmd = "dsmc incremental " + backup_path
        print(cmd)

        start = time.time()

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while p.poll() is None:
            time.sleep(0.5)

        if p.returncode != 0:
            print(p.stdout.read())
        end = time.time()

        elapsed_proc_time = end - start

        out, err = p.communicate()

        print(out)


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

    main(sys.argv[1:])
