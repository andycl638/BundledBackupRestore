import time, subprocess

class ExternalCommand():

    @staticmethod
    def ext_cmd(cmd, dest):
        print(cmd)
        start = time.time()

        if dest is None:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=dest)

        while p.poll() is None:
            time.sleep(0.5)

        if p.returncode != 0:
            print(p.stdout.read())

        end = time.time()

        return end-start
