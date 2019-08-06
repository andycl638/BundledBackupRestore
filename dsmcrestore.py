import sys
import os
import subprocess
import time
#dsmc restore /scale01/scratch/ -subdir=yes

class DsmcRestore():

    def __init__(self, restore_path):
        self.restore_path = restore_path

    def restore(self):
        cmd = "dsmc restore " + self.restore_path
        #cmd = "ls -l " + self.restore_path
        print(cmd)

        start = time.time()

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while p.poll() is None:
            time.sleep(0.5)

        if p.returncode != 0:
            print(p.stdout.read())
            print("Error in the subprocess cmd")
        else:
            for line in p.stdout:
                print (line.rstrip())

        end = time.time()

        elapsed_proc_time = end - start

        out, err = p.communicate()

'''
def main(argv):
    #restore_path
    if len(argv) < 1:
        print("Not enough arguments. Need one arguments.")
        print("Syntax: python3 restoresp.py <restore path>")
        sys.exit()
    if len(argv) > 2:
        print("Too many arguments. Need one arguments.")
        print("Syntax: python3 restoresp.py <restore path>")
        sys.exit()

    restore_path = argv[0]

    if os.path.isdir(restore_path):
        print("Restore Path: %s" %restore_path)
    else:
        print("Restore path is not valid: %s" %restore_path)
        sys.exit()

    DsmcRestore().restore_from_sp(restore_path)

if __name__ == '__main__':
    print("starting script\n")

    main(sys.argv[1:])'''