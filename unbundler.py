import subprocess
import os
import time
from os.path import getsize
from multiprocessing import Pool

def build_list(src_list, dest):
    print("building out list to unbundle")
    unbundle_list = []
    temp = []
    for src in src_list:
        temp.append(src)
        temp.append(dest)
        unbundle_list.append(temp)
        temp = []
    print(unbundle_list)
    return unbundle_list

def parallel_unbundle(unbundle_list):
    print("\nStarting parallel unbundler")
    start = time.time()

    with Pool(16) as p:
        messages = p.map(unbundle_func, unbundle_list)

    for message in messages:
        print(message)

    end = time.time()
    elapsed = end - start
    print("Total Time elapsed: %s" %elapsed)

def unbundle_func(unbundle_list):
    start = time.time()

    cmd, bundle_size = unbundle(unbundle_list[0], unbundle_list[1])

    end = time.time()
    elapsed = end - start

    bundle_size_mib = bundle_size/1024/1024
    bundle_size_gib = bundle_size_mib/1024
    throughput = bundle_size_mib / elapsed

    result_str = "\nResults:"
    cmd_str = "\nUnbundle cmd: %s" %cmd
    bundle_size_str = "\nSize of bundle: " + str(bundle_size_gib)
    throughput_str = "\nThroughput (MiB/sec): " + str(throughput)
    elapsed_str = "\nTime elapsed per process: %s" %elapsed

    message = result_str + cmd_str + bundle_size_str + throughput_str + elapsed_str
    return message

def unbundle(src, dest):

    bundle_size = get_bundle_size(src)

    cmd = "star -x -v -f " + src

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=dest)

    while p.poll() is None:
        time.sleep(0.5)

    if p.returncode != 0:
        print(p.stdout.read())

    out, err = p.communicate()

    print (out)
    return cmd, bundle_size

def get_bundle_size(src):
    bundle_size = os.path.getsize(src)

    return bundle_size

if __name__ == '__main__':
    src_list = ["/scale01/scratch/vzStar1563898168.9314256.star",
    "/scale01/scratch/vzStar1563898660.0732245.star",
    "/scale01/scratch/vzStar1563899542.2173061.star",
    "/scale01/scratch/vzStar1563900375.2915883.star",
    "/scale01/scratch/vzStar1563898168.9315033.star",
    "/scale01/scratch/vzStar1563898667.5462172.star",
    "/scale01/scratch/vzStar1563899543.2184606.star",
    "/scale01/scratch/vzStar1563900400.3252447.star",
    "/scale01/scratch/vzStar1563898168.9320197.star",
    "/scale01/scratch/vzStar1563898669.5491428.star",
    "/scale01/scratch/vzStar1563899554.732258.star",
    "/scale01/scratch/vzStar1563900400.8261027.star",
    "/scale01/scratch/vzStar1563898168.932067.star",
    "/scale01/scratch/vzStar1563898671.077238.star",
    "/scale01/scratch/vzStar1563899554.7473142.star",
    "/scale01/scratch/vzStar1563900405.832033.star",
    "/scale01/scratch/vzStar1563898168.932367.star",
    "/scale01/scratch/vzStar1563898671.1070988.star",
    "/scale01/scratch/vzStar1563899561.7412028.star",
    "/scale01/scratch/vzStar1563900410.338482.star",
    "/scale01/scratch/vzStar1563898168.9324036.star",
    "/scale01/scratch/vzStar1563898679.063191.star",
    "/scale01/scratch/vzStar1563899568.250424.star",
    "/scale01/scratch/vzStar1563900513.4653091.star",
    "/scale01/scratch/vzStar1563898168.9324696.star",
    "/scale01/scratch/vzStar1563898684.0690181.star",
    "/scale01/scratch/vzStar1563899658.3614728.star",
    "/scale01/scratch/vzStar1563900618.5916538.star",
    "/scale01/scratch/vzStar1563898168.932494.star",
    "/scale01/scratch/vzStar1563898846.7943053.star",
    "/scale01/scratch/vzStar1563899766.001946.star",
    "/scale01/scratch/vzStar1563900640.6190276.star",
    "/scale01/scratch/vzStar1563898225.4994745.star",
    "/scale01/scratch/vzStar1563898952.9444523.star",
    "/scale01/scratch/vzStar1563899789.5253575.star",
    "/scale01/scratch/vzStar1563900641.131416.star",
    "/scale01/scratch/vzStar1563898268.548686.star",
    "/scale01/scratch/vzStar1563898965.9441857.star",
    "/scale01/scratch/vzStar1563899790.0258825.star",
    "/scale01/scratch/vzStar1563900659.1556644.star",
    "/scale01/scratch/vzStar1563898275.0573308.star",
    "/scale01/scratch/vzStar1563898968.948298.star",
    "/scale01/scratch/vzStar1563899804.542481.star",
    "/scale01/scratch/vzStar1563900660.6553316.star",
    "/scale01/scratch/vzStar1563898280.5665874.star",
    "/scale01/scratch/vzStar1563898974.9832745.star",
    "/scale01/scratch/vzStar1563899805.0682147.star",
    "/scale01/scratch/vzStar1563900679.7234008.star",
    "/scale01/scratch/vzStar1563898281.5663767.star",
    "/scale01/scratch/vzStar1563898976.4587739.star",
    "/scale01/scratch/vzStar1563899814.05399.star",
    "/scale01/scratch/vzStar1563900693.186593.star",
    "/scale01/scratch/vzStar1563898281.5665224.star",
    "/scale01/scratch/vzStar1563898979.9602585.star",
    "/scale01/scratch/vzStar1563899819.5612411.star",
    "/scale01/scratch/vzStar1563900830.8559275.star",
    "/scale01/scratch/vzStar1563898292.079809.star",
    "/scale01/scratch/vzStar1563898985.9713569.star",
    "/scale01/scratch/vzStar1563899925.6987214.star",
    "/scale01/scratch/vzStar1563900942.5186968.star",
    "/scale01/scratch/vzStar1563898293.5816634.star",
    "/scale01/scratch/vzStar1563899095.1250556.star",
    "/scale01/scratch/vzStar1563900058.8820891.star",
    "/scale01/scratch/vzStar1563900977.0619419.star",
    "/scale01/scratch/vzStar1563898439.3079588.star",
    "/scale01/scratch/vzStar1563899217.8047557.star",
    "/scale01/scratch/vzStar1563900098.4318357.star",
    "/scale01/scratch/vzStar1563900978.570927.star",
    "/scale01/scratch/vzStar1563898544.939556.star",
    "/scale01/scratch/vzStar1563899236.7924023.star",
    "/scale01/scratch/vzStar1563900098.912711.star",
    "/scale01/scratch/vzStar1563901008.5836225.star",
    "/scale01/scratch/vzStar1563898561.4164238.star",
    "/scale01/scratch/vzStar1563899237.293348.star",
    "/scale01/scratch/vzStar1563900116.9498248.star",
    "/scale01/scratch/vzStar1563901008.5860481.star",
    "/scale01/scratch/vzStar1563898565.42105.star",
    "/scale01/scratch/vzStar1563899261.8731096.star",
    "/scale01/scratch/vzStar1563900117.4607596.star",
    "/scale01/scratch/vzStar1563901008.65003.star",
    "/scale01/scratch/vzStar1563898567.4542563.star",
    "/scale01/scratch/vzStar1563899265.866861.star",
    "/scale01/scratch/vzStar1563900125.9728992.star",
    "/scale01/scratch/vzStar1563901014.1093218.star",
    "/scale01/scratch/vzStar1563898567.4820929.star",
    "/scale01/scratch/vzStar1563899278.3892581.star",
    "/scale01/scratch/vzStar1563900130.4643707.star",
    "/scale01/scratch/vzStar1563901124.2335207.star",
    "/scale01/scratch/vzStar1563898573.4305146.star",
    "/scale01/scratch/vzStar1563899285.8584895.star",
    "/scale01/scratch/vzStar1563900239.6215637.star",  
    "/scale01/scratch/vzStar1563901300.9884758.star",
    "/scale01/scratch/vzStar1563898575.4329424.star",
    "/scale01/scratch/vzStar1563899429.573806.star",
    "/scale01/scratch/vzStar1563900342.7479224.star",
    "/scale01/scratch/vzStar1563901335.5393004.star",
    "/scale01/scratch/vzStar1563898614.5165956.star",
    "/scale01/scratch/vzStar1563899527.1992764.star",
    "/scale01/scratch/vzStar1563900374.7918627.star",
    "/scale01/scratch/vzStar1563901364.0837162.star",]
    unbundle_list = build_list(src_list, "/vz9")
    parallel_unbundle(unbundle_list)
    #unbundle(src_list, "/vz8")
