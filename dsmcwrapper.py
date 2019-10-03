import sys, os, subprocess, time, re

#Grab all .star files and backup to SP server using dsmc

class DsmcWrapper():
    def __init__(self, backup_path, resource_utilization, dsm_opt, virtual_mnt_pt, restore_path):
        self.backup_path = backup_path
        self.resource_utilization = resource_utilization
        self.dsm_opt = dsm_opt
        self.virtual_mnt_pt = virtual_mnt_pt
        self.restore_path = restore_path

    def __str__(self):
        return 'Backup path: ' + self.backup_path + '\nRU: ' + str(self.resource_utilization) + '\nDSM OPT: ' + self.dsm_opt + '\nvmp: ' + self.virtual_mnt_pt + '\nRestore Path: ' + self.restore_path

    def backup(self, backup_list):
        #cmd = "dsmc selective '" + os.path.join(self.backup_path, '*') + "' -resourceutilization=" + str(self.resource_utilization)
        cmd = "dsmc selective " + backup_list + " -resourceutilization=" + str(self.resource_utilization)

        print(cmd)
        return cmd

    def restore(self):
        cmd = "dsmc restore " + self.restore_path + "/ -sub=yes -resourceutilization=" + str(self.resource_utilization)

        print(cmd)
        return cmd

    def cmd(self, cmd, queue):
        transfer_rate_arr = []

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        while True:
            output = p.stdout.readline().decode('utf-8')
            if p.poll() != None:
                break

            if output:
                print (output.strip())
                if "Aggregate data transfer rate:" in output:
                    transfer_rate_arr = re.findall('\d*\.?\d+', output)
                elif "[Done]" in output:
                    queue.put(output)

        print ("dsmc: finished")

        transfer_rate = ""
        for num in transfer_rate_arr:
            transfer_rate = transfer_rate + num

        return transfer_rate

    def write_virtualmnt(self):
        newfile = []
        with open(self.dsm_opt, 'r') as file:
            lines = file.readlines()

            for line in lines:
                if "virtualmountpoint" in line:
                    line = line.replace(line, "virtualmountpoint "  + self.virtual_mnt_pt + "\n")
                newfile.append(line)

        with open(self.dsm_opt, 'w') as file:
            file.writelines(newfile)
