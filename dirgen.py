import os

def generate_dir(level3Name, level3Num, level4Name, level4Num, level5Name, level5Num, root):
    """
    Generate a 5 level nested directory structure
    """

    import shutil
    """
    Creating initial directory structure that will be copied for other directories
    5 levels
    """
    initDir = os.path.join(root, level3Name + str(1), level4Name + str(1))
    level3Dir = os.path.join(root, level3Name + str(1))
    level4Dir = os.path.join(level3Dir, level4Name + str(1))
    print("Initial Dir3: %s" %level3Dir)
    print("Initial Dir4: %s" %level4Dir)

    os.makedirs(initDir)
    level3Num -= 1
    level4Num -= 1

    for num in range(1, level5Num+1):
        os.makedirs(os.path.join(initDir, level5Name + str(num)))
        print("making lvl 5 dirs")
        print(os.path.join(level4Dir, level5Name + str(num)))

    """
    Copy initial directory structure to level 4 directory
    """
    for num in range(2, level4Num + 2):
        print("copy level 4 dir tree")
        print("copy %s" %level4Dir)
        s = os.path.join(level3Dir, level4Name + str(num))
        print("to %s" %s)
        shutil.copytree(level4Dir, os.path.join(level3Dir, level4Name + str(num)))

    for num in range(2, level3Num + 2):
        print("copy level 3 dir tree")
        print("copy %s" %level3Dir)
        s = os.path.join(root, level3Name + str(num))
        print("to %s" %s)
        shutil.copytree(level3Dir, os.path.join(root, level3Name + str(num)))

def generate_dir_list(foldernum):
    file = open("directory list", "w")

    for num in range(1, foldernum+1):
        for root, dirs, files in os.walk('Lvl3 folder' + str(num), topdown=False):
            for name in dirs:
                print(os.path.join(root, name))
                file.write(os.path.join(root, name) + '\n')

    file.close()

if __name__ == '__main__':
    root = "/vz9"
    level3Name = "L3-"
    level3Num = 10
    level4Name = "L4-"
    level4Num = 10
    level5Name = "L5-"
    level5Num = 8
    generate_dir(level3Name, level3Num, level4Name, level4Num, level5Name, level5Num, root)
"""
    root = "/vsnap/vpool1/vz7"
    level3Name = "Level3-"
    level3Num = 4
    level4Name = "Level4-"
    level4Num = 8
    level5Name = "Level5-"
    level5Num = 16"""
