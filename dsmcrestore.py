import sys, os, subprocess, time


class DsmcRestore():

    def __init__(self, restore_path):
        self.restore_path = restore_path

    def restore(self):
        cmd = "dsmc restore " + self.restore_path + "/"

        print(cmd)

        transfer_rate_arr = []

        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

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
