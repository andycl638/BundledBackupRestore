import sys, os, subprocess, time, re

#Grab all .star files and backup to SP server using dsmc

class DsmcBackup():
    def __init__(self, backup_path, resource_utilization):
        self.backup_path = backup_path
        self.resource_utilization = resource_utilization

    def backup(self):
        cmd = "dsmc selective '" + os.path.join(self.backup_path, '*') + "' -resourceutilization=" + str(self.resource_utilization)

        print(cmd)

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        transfer_rate_arr = []

        while True:
            output = p.stdout.readline().decode('utf-8')
            if p.poll() != None:
                break

            if output:
                print (output.strip())
                if "Aggregate data transfer rate:" in output:
                    transfer_rate_arr = re.findall('\d*\.?\d+', output)

        print ("dsmc: finished")

        transfer_rate = ""
        for num in transfer_rate_arr:
            transfer_rate = transfer_rate + num

        print (transfer_rate)
        return transfer_rate


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
