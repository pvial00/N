import subprocess, yaml

def getfreespace_remote_report_hyper(hypers, vols):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'disk.usage']
    out = subprocess.check_output(salt_cmd)
    report = {}
    v = yaml.load(out)
    for key in v.keys():
        for subkey in v[key].keys():
            if subkey in vols:
                report[key] = {}
                report[key][subkey]= v[key][subkey]
    return report

def getfreespace_remote_report(hypers, vols):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'disk.usage']
    out = subprocess.check_output(salt_cmd)
    report = {}
    v = yaml.load(out)
    for key in v.keys():
        if type(v[key]) != str:
            for subkey in v[key].keys():
                if subkey in vols:
                    report[subkey] = v[key][subkey]
    return report

def gettotalfreespace_remote(hypers, vols):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'disk.usage']
    out = subprocess.check_output(salt_cmd)
    report = {}
    v = yaml.load(out)
    report = {}
    for key in v.keys():
        total = 0
        if type(v[key]) != str:
            for subkey in v[key].keys():
                if subkey in vols:
                    total += int(v[key][subkey]['available'])
                    report[key] = total
    return report

def getfreespace_local_report(hypers, vols):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'disk.usage']
    out = subprocess.check_output(salt_cmd)
    reports = {}
    v = yaml.load(out)
    for key in v.keys():
        if type(v[key]) != str:
            for subkey in v[key].keys():
                if subkey in vols and v[key][subkey]['filesystem'][:4] == "/dev":
                    reports[key] = {}
                    reports[key][subkey]= v[key][subkey]
    return reports

def getfreespace_remote(hypers, vols):
    reports = getfreespace_remote_report(hypers, vols)
    used = 0
    avail = 0
    for key in reports.keys():
        used += int(reports[key]['used'])
        avail += int(reports[key]['available'])
    return avail, used

def getstats_remote(hypers, vols):
    reports = getfreespace_remote_report(hypers, vols)
    sr = {}
    for key in reports.keys():
        sr[key] = {}
        sr[key]['used'] = int(reports[key]['used'])
        sr[key]['available'] = int(reports[key]['available'])
    return sr

def getstats_local(hypers, vols):
    reports = getfreespace_local_report(hypers, vols)
    sr = {}
    for hyper in reports.keys():
        for key in reports[hyper].keys():
            sr[key] = {}
            sr[key]['used'] = int(reports[hyper][key]['used'])
            sr[key]['available'] = int(reports[hyper][key]['available'])
    return sr

def getfreespace_local(hypers, vols):
    reports = getstats_local(hypers, vols)
    avail = 0
    used = 0
    for key in reports.keys():
        avail += reports[key]['available']
        used += reports[key]['used']
    return avail, used

def volume_list(hypers, vols):
    sr = getstats_remote(hypers, vols)
    return sr

def volume_mount_nfs(hypers, server, vol, mnt):
    mkdir_cmd = "mkdir -p " + mnt
    mount_cmd = "mount " + server + ":" + vol + " " + mnt
    saltmkdir_cmd = ['salt', hypers, 'cmd.run', mkdir_cmd]
    salt_cmd = ['salt', hypers, 'cmd.run', mount_cmd]
    out = subprocess.check_output(saltmkdir_cmd)
    out = subprocess.check_output(salt_cmd)

def volume_attach(hypers, vmname, volname, size, vols):
    from Nresource_mgr import select_avail_storage
    from Nvminit import gethyperbyvmname
    hyper = gethyperbyvmname(hypers, vmname)
    vol = select_avail_storage(hypers, vols)
    path = vol + "/" + volname + ".img"
    qemu_img_cmd = ['qemu-img', 'create', path, size]
    out = subprocess.check_output(qemu_img_cmd)
    from os import chmod
    chmod(path, 0o777)
    virsh_cmd = "virsh attach-disk " + vmname + " " + path + " vdb --cache none"
    salt_cmd = ['salt', hyper, 'cmd.run', virsh_cmd]
    out = subprocess.check_output(salt_cmd)

def volume_detach(hypers, vmname, volname):
    from Nresource_mgr import select_avail_storage
    from Nvminit import gethyperbyvmname
    hyper = gethyperbyvmname(hypers, vmname)
    vols = volumes_list(hyper, vmname)
    for vol in vols:
        if vol == volname:
            virsh_cmd = "virsh detach-disk --domain " + vmname + " " + vols[vol]
            salt_cmd = ['salt', hyper, 'cmd.run', virsh_cmd]
            out = subprocess.check_output(salt_cmd)
            return vols[vol]
    return False

def volume_delete(hypers, volpath):
    from os import remove
    remove(volpath)

def volumes_list(hypers, vmname):
    from Nvminit import gethyperbyvmname
    hyper = gethyperbyvmname(hypers, vmname)
    if hyper == None:
        return None
    virsh_cmd = "virsh domblklist " + vmname
    salt_cmd = ['salt', '--out', 'yaml', hyper, 'cmd.run', virsh_cmd]
    out = subprocess.check_output(salt_cmd)
    vollist = yaml.load(out)
    vols = {}
    tmp = vollist[hyper].split('\n')
    for x in range(2):
        tmp.pop(0)
    for element in tmp:
        dev = element.split()[0]
        path = element.split()[1]
        vols[dev] = path
    return vols
