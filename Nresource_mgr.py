from Nvminit import *
from Nstorage import *
import yaml, subprocess, random

def getfreeresourceshyper(hypers, vols):
    hlist = hyperlist_list(hypers)
    cpus = getfreecpus(hypers)
    mems = getfreemems(hypers)
    disks = gettotalfreespace_remote(hypers, vols)
    h = {}
    for key in hlist:
        h[key] = [cpus[key], mems[key], disks[key]]
    return h

def getfreeresourcesraw(hypers, vols):
    cpus = getfreecpus(hypers)
    mems = getfreemems(hypers)
    availdisk, useddisk = getfreespace_remote(hypers, vols)
    availdisk_local, useddisk_local = getfreespace_local(hypers, vols)
    c = 0
    for key in cpus.keys():
        if type(cpus[key]) == int:
            c += cpus[key]
    m = 0
    for key in mems.keys():
        if type(mems[key]) == int or type(mems[key]) == float:
            m += mems[key]
    return c, m, (availdisk_local+availdisk), (useddisk_local+useddisk), (availdisk+useddisk+availdisk_local+useddisk_local)

def gettotalnumcpus(hypers):
    salt_cmd = ['salt', hypers, 'status.nproc']
    out = subprocess.check_output(salt_cmd)
    cpus = yaml.load(out)
    c = 0
    for key in cpus.keys():
        if type(cpus[key]) == int:
            c += cpus[key]
    return c

def gettotalmem(hypers):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'grains.item', 'mem_total']
    out = subprocess.check_output(salt_cmd)
    mems = yaml.load(out)
    m = 0
    for key in mems.keys():
        try:
            if type(mems[key]['mem_total']) == int or type(mems[key]['mem_total']) == float:
                m += mems[key]['mem_total']
        except TypeError as ter:
            pass
    return m

def getcapacity(hypers, vols):
    availcpu, availmem, availdisk, useddisk, totaldisk = getfreeresourcesraw(hypers, vols)
    totalcpus = gettotalnumcpus(hypers)
    totalmem = gettotalmem(hypers)
    cpufree = round(float(float(availcpu) / float(totalcpus)) * 100, 2)
    memfree = round(float(float(availmem) / float(totalmem)) * 100, 2)
    availdisk = availdisk / 1024
    useddisk = useddisk / 1024
    totaldisk = totaldisk / 1024
    diskfree = round(float(float(availdisk) / float(totaldisk)) * 100, 2)
    return cpufree, memfree, totalcpus, totalmem, availcpu, availmem, availdisk,useddisk, totaldisk, diskfree

def isCapacity(hypers, cpu, mem, disk, vols):
    availcpu, availmem, availdisk, useddisk, totaldisk = getfreeresourcesraw(hypers, vols)
    if availcpu < cpu or availmem < mem or availdisk < disk:
        return False
    else:
        return True

def select_avail_hyper(hypers, cpu, mem, mode, vols, storage=None):
    hypes = []
    if mode == "random":
        h = getfreeresourceshyper(hypers, vols)
        for key in h.keys():
            if h[key][0] >= cpu and h[key][1] >= mem:
                hypes.append([key, h[key][0], h[key][1]])
        return random.choice(hypes)
    elif mode == "least":
        last = [None, 0, 0]
        h = getfreeresourceshyper(hypers, vols)
        for key in h.keys():
            if h[key][0] >= cpu and h[key][1] >= mem:
                item = [key, h[key][0], h[key][1]]
                if item[1] > last[1] and item[2] > last[2]:
                    last = list(item)
                #else:
                #    last = [key, h[key][0], h[key][1]]
        if last[0] == None:
            raise ValueError('Hyper cannot be selected.  Possible out of capacity.')
        return last[0]

def select_avail_storage(hyper, vols):
    stats = getstats_remote(hyper, vols)
    last = 0
    vol = None
    for key in stats.keys():
        if stats[key]['available'] > last:
            last = stats[key]['available']
            vol = key
    return vol

def vmstartall(hypers, vols, hyper_select, vmcfgdir):
    atrest = vmsatrest(hypers, vmcfgdir)
    for key in atrest.keys():
        for name in atrest[key]:
            if hypers != None:
                cpus, mem, vol = load_resources_from_xml(hypers, name, vmcfgdir)
                hyper = select_avail_hyper(hypers, int(cpus), int(mem), hyper_select, vols)
                vmstart(hyper, vmcfgdir, name)
                print("Starting...", name)
    print("done")

def vmshutdownall(hypers, vols, hyper_select, vmcfgdir):
    vms = getactivevms(hypers)
    for key in vms.keys():
        for name in vms[key]:
            if hypers != None:
                vmshutdown(key, name)
                print("Shutting down...", name)
    print("done")
