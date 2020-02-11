import subprocess, random, glob

def isLoopBusy(devicename):
    cmd = ['losetup', '-a']
    out = subprocess.check_output(cmd)
    for line in out.decode('utf-8').split('\n'):
        if devicename in line:
            return True
    return False

def select_avail_loop():
    cmd = ['losetup', '-f']
    out = subprocess.check_output(cmd)
    dev = out.decode('utf-8').split('\n')[0]
    return dev
