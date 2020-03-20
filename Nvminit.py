import os, subprocess
import xml.etree.ElementTree as ET
import yaml, requests, time
from binascii import hexlify
from Nloop import *

def mount_img_freebsd(imgpath, mntpath, device):
    losetup_cmd = ['losetup', device, imgpath]
    out = subprocess.check_output(losetup_cmd)
    kpartx_cmd = ['kpartx', '-av', device]
    out = subprocess.check_output(kpartx_cmd)
    zpool_import_cmd = ['zpool', 'import', '-R', mntpath, '-d', '/dev/mapper']
    out = subprocess.check_output(zpool_import_cmd)
    lines = out.decode('utf-8').split('\n')
    for line in lines:
        if "id:" in line:
            _id = line.split(':')[1].strip()
    zpool_import_cmd2 = ['zpool', 'import', '-f', '-d', '/dev/mapper', _id, 'zroot', '-R', mntpath]
    out = subprocess.check_output(zpool_import_cmd2)
    zfs_mount_cmd = ['zfs', 'mount', 'zroot/ROOT/default']
    out = subprocess.check_output(zfs_mount_cmd)
    tmpworkdir = mntpath + mntpath + "/default"
    return tmpworkdir

def umount_img_freebsd(device):
    umount_cmd = ['zpool', 'export', 'zroot']
    out = subprocess.check_output(umount_cmd)
    kpartx_cmd = ['kpartx', '-dv', device]
    out = subprocess.check_output(kpartx_cmd)
    losetup_cmd = ['losetup', '-d', device]
    out = subprocess.check_output(losetup_cmd)

def mount_img_solaris(imgpath, mntpath, device):
    losetup_cmd = ['losetup', device, imgpath]
    out = subprocess.check_output(losetup_cmd)
    kpartx_cmd = ['kpartx', '-av', device]
    out = subprocess.check_output(kpartx_cmd)
    zpool_import_cmd = ['zpool', 'import', '-f', '-R', mntpath, '-d', '/dev/mapper']
    out = subprocess.check_output(zpool_import_cmd)
    lines = out.decode('utf-8').split('\n')
    for line in lines:
        if "id:" in line:
            _id = line.split(':')[1].strip()
    zpool_import_cmd2 = ['zpool', 'import', '-f', '-d', '/dev/mapper', _id, 'zroot', '-R', mntpath]
    out = subprocess.check_output(zpool_import_cmd2)
    zfs_mount_cmd = ['zfs', 'mount', 'zroot/ROOT/default']
    out = subprocess.check_output(zfs_mount_cmd)
    tmpworkdir = mntpath + mntpath + "/default"
    return tmpworkdir

def umount_img_solaris(device):
    umount_cmd = ['zpool', 'export', 'zroot']
    out = subprocess.check_output(umount_cmd)
    kpartx_cmd = ['kpartx', '-dv', device]
    out = subprocess.check_output(kpartx_cmd)
    losetup_cmd = ['losetup', '-d', device]
    out = subprocess.check_output(losetup_cmd)

def cp_new_img_macos(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def cp_new_img_windows(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def cp_new_img_netbsd(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def cp_new_img_openbsd(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def cp_new_img_freebsd(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def cp_new_img_solaris(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def cp_new_img_minix(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def cp_new_img_debian(vmdir, hostname, img):
    newimg = vmdir + "/" + hostname + ".img"
    cp_cmd = ['cp', img, newimg]
    out = subprocess.check_output(cp_cmd)

def mountos_img_debian(imgpath, mntpath, device, part):
    fulldevice = device + part
    losetup_cmd = ['losetup', '-P', device, imgpath]
    out = subprocess.check_output(losetup_cmd)
    mnt_cmd = ['mount', fulldevice, mntpath]
    out = subprocess.check_output(mnt_cmd)

def umountos_img_debian(mntpath, device):
    umount_cmd = ['umount', mntpath]
    out = subprocess.check_output(umount_cmd)
    losetup_cmd = ['losetup', '-d', device]
    out = subprocess.check_output(losetup_cmd)

def mountos_img_oracle_linux(imgpath, mntpath, device, part):
    fulldevice = device + part
    losetup_cmd = ['losetup', '-P', device, imgpath]
    out = subprocess.check_output(losetup_cmd)
    vg_cmd = ['vgchange', '-ay']
    out = subprocess.check_output(vg_cmd)
    mnt_cmd = ['mount', '/dev/ol/root', mntpath]
    out = subprocess.check_output(mnt_cmd)

def umountos_img_oracle_linux(mntpath, device):
    umount_cmd = ['umount', mntpath]
    out = subprocess.check_output(umount_cmd)
    vg_cmd = ['vgchange', '-a', 'n', 'ol']
    out = subprocess.check_output(vg_cmd)
    losetup_cmd = ['losetup', '-d', device]
    out = subprocess.check_output(losetup_cmd)

def gen_salt_keys(path, hostname):
    gk = "--gen-keys=" + hostname
    gkdir = "--gen-keys-dir=" + "/tmp"
    salt_key_cmd = ['salt-key', gk, gkdir]
    out = subprocess.check_output(salt_key_cmd)
    src_pem_file = "/tmp/" + hostname + ".pem"
    src_pub_file = "/tmp/" + hostname + ".pub"
    minpath_pem = path + "/etc/salt/pki/minion/minion.pem"
    minpath_pub = path + "/etc/salt/pki/minion/minion.pub"
    srvpath_pub = "/etc/salt/pki/master/minions/" + hostname
    cp_pem_cmd = ['cp', src_pem_file, minpath_pem]
    cp_pub_cmd = ['cp', src_pub_file, minpath_pub]
    cp_srv_pub_cmd = ['cp', src_pub_file, srvpath_pub]
    out = subprocess.check_output(cp_pem_cmd)
    out = subprocess.check_output(cp_pub_cmd)
    out = subprocess.check_output(cp_srv_pub_cmd)
    minid_path = path + "/etc/salt/minion_id"
    f = open(minid_path, "w")
    f.write(hostname)
    f.close()

def gen_salt_keys_freebsd(path, hostname):
    gk = "--gen-keys=" + hostname
    gkdir = "--gen-keys-dir=" + "/tmp"
    salt_key_cmd = ['salt-key', gk, gkdir]
    out = subprocess.check_output(salt_key_cmd)
    src_pem_file = "/tmp/" + hostname + ".pem"
    src_pub_file = "/tmp/" + hostname + ".pub"
    minpath_pem = path + "/usr/local/etc/salt/pki/minion/minion.pem"
    minpath_pub = path + "/usr/local/etc/salt/pki/minion/minion.pub"
    srvpath_pub = "/etc/salt/pki/master/minions/" + hostname
    cp_pem_cmd = ['cp', src_pem_file, minpath_pem]
    cp_pub_cmd = ['cp', src_pub_file, minpath_pub]
    cp_srv_pub_cmd = ['cp', src_pub_file, srvpath_pub]
    out = subprocess.check_output(cp_pem_cmd)
    out = subprocess.check_output(cp_pub_cmd)
    out = subprocess.check_output(cp_srv_pub_cmd)
    minid_path = path + "/usr/local/etc/salt/minion_id"
    f = open(minid_path, "w")
    f.write(hostname)
    f.close()

def sethostname_freebsd(path, hostname):
    path += "/etc/rc.conf"
    hostnameline = "hostname=\"" + hostname + "\""
    f = open(path, "r")
    conf = f.read()
    f.close()
    lines = conf.split('\n')
    lines.pop(0)
    lines.insert(0, hostnameline)
    _file = ""
    for line in lines:
        _file += line + "\n"
    f = open(path, "w")
    f.write(_file)
    f.close()

def sethostname_debian(path, hostname):
    path += "/etc/hostname"
    f = open(path, "w")
    f.write(hostname)
    f.close()

def sethostfile_debian(path, hostname):
    path += "/etc/hosts"
    line1 = "127.0.0.1    localhost\n"
    line2 = "127.0.1.1    " + hostname
    hostfile = line1 + line2
    f = open(path, "w")
    f.write(hostfile)
    f.close()

def sethostfile_oracle(path, hostname):
    path += "/etc/hosts"
    line1 = "127.0.0.1    localhost\n"
    line2 = "127.0.0.1    " + hostname
    hostfile = line1 + line2
    f = open(path, "w")
    f.write(hostfile)
    f.close()

def gensshkeys_debian(path):
    ecdsa_path = path + "/etc/ssh/ssh_host_ecdsa_key"
    ecdsa_path_pub = path + "/etc/ssh/ssh_host_ecdsa_key.pub"
    os.remove(ecdsa_path)
    os.remove(ecdsa_path_pub)

    rsa_path = path + "/etc/ssh/ssh_host_rsa_key"
    rsa_path_pub = path + "/etc/ssh/ssh_host_rsa_key.pub"
    os.remove(rsa_path)
    os.remove(rsa_path_pub)
    
    ed_path = path + "/etc/ssh/ssh_host_ed25519_key"
    ed_path_pub = path + "/etc/ssh/ssh_host_ed25519_key.pub"
    os.remove(ed_path)
    os.remove(ed_path_pub)
    #ssh_cmd = ['chroot', path, 'dpkg-reconfigure', 'openssh-server']
    #out = subprocess.check_output(ssh_cmd)
    ssh_cmd = ['chroot', path, 'ssh-keygen', '-A']
    out = subprocess.check_output(ssh_cmd)

def gensshkeys_freebsd(path):
    dsa_path = path + "/etc/ssh/ssh_host_dsa_key"
    dsa_path_pub = path + "/etc/ssh/ssh_host_dsa_key.pub"

    ecdsa_path = path + "/etc/ssh/ssh_host_ecdsa_key"
    ecdsa_path_pub = path + "/etc/ssh/ssh_host_ecdsa_key.pub"

    rsa_path = path + "/etc/ssh/ssh_host_rsa_key"
    rsa_path_pub = path + "/etc/ssh/ssh_host_rsa_key.pub"
    
    ed_path = path + "/etc/ssh/ssh_host_ed25519_key"
    ed_path_pub = path + "/etc/ssh/ssh_host_ed25519_key.pub"
    path += "/etc/ssh"
    dsa_cmd = "ssh-keygen -t dsa -f " + dsa_path + " -q -N \'\'"
    os.system(dsa_cmd)
    ecdsa_cmd = "ssh-keygen -t ecdsa -f " + ecdsa_path + " -q -N \'\'"
    os.system(ecdsa_cmd)
    rsa_cmd = "ssh-keygen -t rsa -f " + rsa_path + " -q -N \'\'"
    os.system(rsa_cmd)
    ed_cmd = "ssh-keygen -t rsa -f " + ed_path + " -q -N \'\'"
    os.system(ed_cmd)

def preseed_salt_minion_keys_debian(hostname, mntpath):
    genkeys = "--gen-keys=" + hostname
    salt_cmd = ['salt-key', genkeys]
    out = subprocess.check_output(salt_cmd)
    cpcmd = "cp " + hostname + ".pub /etc/salt/pki/master/minions/" + hostname
    os.system(cpcmd)

def preseed_salt_minion_keys_freebsd(hostname, mntpath):
    genkeys = "--gen-keys=" + hostname
    salt_cmd = ['salt-key', genkeys]
    out = subprocess.check_output(salt_cmd)
    cpcmd = "cp " + hostname + ".pub /etc/salt/pki/master/minions/" + hostname
    os.system(cpcmd)

def gen_random_mac(mac_prefix):
    m = mac_prefix
    tmp = os.urandom(5)
    for b in tmp:
        m += str(hexlify(b.to_bytes(1, byteorder='big')).decode('utf-8')) + ":"
    return m[:len(m) - 1]

def cfg_xml(path, filename, hostname, mac_addr, vmpath, cpus, mem):
    outfilename = path + "/" + hostname + ".xml"
    tree = ET.parse(filename)
    root = tree.getroot()
    for name in root.iter('name'):
        name.text = hostname
    for name in root.iter('vcpu'):
        name.text = str(cpus)
    for name in root.iter('memory'):
        name.text = str(mem)
    for devs in root.iter('interface'):
        devs[0].attrib['address'] = mac_addr
    for devs in root.iter('disk'):
        devs[0].attrib['file'] = vmpath
    tree.write(outfilename)

def load_xml(hostname, filename):
    cfg = {}
    cfg[hostname] = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    for name in root.iter('name'):
        cfg[hostname]['name'] = name.text
    for name in root.iter('vcpu'):
        cfg[hostname]['vcpu'] = name.text
    for name in root.iter('memory'):
        cfg[hostname]['memory'] = name.text
    for devs in root.iter('interface'):
        cfg[hostname]['mac'] = devs[0].attrib['address']
    for devs in root.iter('disk'):
        cfg[hostname]['disk'] = devs[0].attrib['file']
    return cfg

def load_resources_from_xml(hypers, hostname, vmcfgdir):
    filename = vmcfgdir + "/" + hostname + ".xml"
    cfg = load_xml(hostname, filename)
    cpu = int(cfg[hostname]['vcpu'])
    mem = int(cfg[hostname]['memory']) / 1024
    return cpu, mem, vmcfgdir

def vminit_krypto(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    device = select_avail_loop()
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_debian(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mountos_img_debian(imgpath, workdir, device, part)
    gen_salt_keys(workdir, hostname)
    sethostname_debian(workdir, hostname)
    sethostfile_debian(workdir, hostname)
    gensshkeys_debian(workdir)
    umountos_img_debian(workdir, device)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_freebsd_salt(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    device = select_avail_loop()
    if device != None:
        imgpath = vmdir + "/" + hostname + ".img"
        cp_new_img_freebsd(vmdir, hostname, img)
        os.chmod(imgpath, 0o777)
        tmpworkdir = mount_img_freebsd(imgpath, workdir, device)
        gen_salt_keys_freebsd(tmpworkdir, hostname)
        sethostname_freebsd(tmpworkdir, hostname)
        gensshkeys_freebsd(tmpworkdir)
        umount_img_freebsd(device)
        mac_addr = gen_random_mac(mac_prefix)
        cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)
    else:
        print("Unable to select loop device")

def vminit_oracle_linux_salt(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    device = select_avail_loop()
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_debian(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mountos_img_oracle_linux(imgpath, workdir, device, part)
    sethostname_debian(workdir, hostname)
    sethostfile_oracle(workdir, hostname)
    gen_salt_keys(workdir, hostname)
    umountos_img_oracle_linux(workdir, device)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_oracle_linux(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    device = select_avail_loop()
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_debian(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mountos_img_oracle_linux(imgpath, workdir, device, part)
    sethostname_debian(workdir, hostname)
    sethostfile_oracle(workdir, hostname)
    umountos_img_oracle_linux(workdir, device)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_debian(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    device = select_avail_loop()
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_debian(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mountos_img_debian(imgpath, workdir, device, part)
    sethostname_debian(workdir, hostname)
    sethostfile_debian(workdir, hostname)
    gensshkeys_debian(workdir)
    umountos_img_debian(workdir, device)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_freebsd(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    device = select_avail_loop()
    if device != None:
        imgpath = vmdir + "/" + hostname + ".img"
        cp_new_img_freebsd(vmdir, hostname, img)
        os.chmod(imgpath, 0o777)
        tmpworkdir = mount_img_freebsd(imgpath, workdir, device)
        sethostname_freebsd(tmpworkdir, hostname)
        gensshkeys_freebsd(tmpworkdir)
        umount_img_freebsd(device)
        mac_addr = gen_random_mac(mac_prefix)
        cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)
    else:
        print("Unable to select loop device")

def vminit_solaris(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    device = select_avail_loop()
    if device != None:
        imgpath = vmdir + "/" + hostname + ".img"
        cp_new_img_freebsd(vmdir, hostname, img)
        os.chmod(imgpath, 0o777)
        #tmpworkdir = mount_img_solaris(imgpath, workdir, device)
        #umount_img_solaris(device)
        mac_addr = gen_random_mac(mac_prefix)
        cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)
    else:
        print("Unable to select loop device")

def vminit_openbsd(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_openbsd(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_netbsd(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_netbsd(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_minix(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgidr, storage_default):
    memkb = int(mem) * 1024
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_minix(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_windows(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir, storage_default):
    memkb = int(mem) * 1024
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_windows(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)

def vminit_macos(workdir, builddir, vmdir, hostname, cpus, mem, part, template, img, mac_prefix, vmcfgdir,storage_default):
    memkb = int(mem) * 1024
    imgpath = vmdir + "/" + hostname + ".img"
    cp_new_img_macos(vmdir, hostname, img)
    os.chmod(imgpath, 0o777)
    mac_addr = gen_random_mac(mac_prefix)
    cfg_xml(vmcfgdir, template, hostname, mac_addr, imgpath, cpus, memkb)


def vmstart(hyper, vmcfgdir, hostname):
    if vmcfgdir[:len(vmcfgdir) -1] == "/":
        xmlfile = vmcfgdir + hostname + ".xml"
    else:
        xmlfile = vmcfgdir + "/" + hostname + ".xml"
    virsh_cmd = ['salt', hyper, 'virt.create_xml_path', xmlfile]
    out = subprocess.check_output(virsh_cmd)
    print(out)

def vmstartatrest(hypers, hostname, vols, mode=None):
    hyper, vol = getvmlocationatrest(hypers, hostname, vols)
    vmstart(vol, hostname, hyper)

def getfreecpus(hypers):
    salt_cmd = ['salt', hypers, 'virt.freecpu']
    out = subprocess.check_output(salt_cmd)
    cpus = yaml.load(out)
    freecpus = {}
    for key in cpus.keys():
        if type(cpus[key]) != str:
            freecpus[key] = cpus[key]
    return freecpus

def getfreemems(hypers):
    salt_cmd = ['salt', hypers, 'virt.freemem']
    out = subprocess.check_output(salt_cmd)
    fms = yaml.load(out)
    freemems = {}
    for key in fms.keys():
        if type(fms[key]) != str:
            freemems[key] = fms[key]
    return freemems

def getactivevms(hypers):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'virt.list_active_vms']
    out = subprocess.check_output(salt_cmd)
    vms = yaml.load(out)
    activevms = {}
    c = 0
    for key in vms.keys():
        if vms[key] != [] and type(vms[key]) != str:
            activevms[key] = vms[key]
            c += 1
    if c <= 0:
        return None
    else:
        return activevms

def isVMactive(hypers, hostname):
    vms = getactivevms(hypers)
    if vms != None:
        if len(vms) > 0:
            for key in vms.keys():
                if hostname in vms[key]:
                        return True
    return False

def getdiskspace(hypers, volume):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'disk.usage']
    out = subprocess.check_output(salt_cmd)
    disks = yaml.load(out)
    ds = []
    for key in disks.keys():
        for subkey in disks[key].keys():
            if subkey == volume:
                ds.append(disks[key][subkey])
    return ds

def gethyperbyvmname(hypers, vmname):
    vms = getactivevms(hypers)
    for key in vms.keys():
        tmp = vms[key]
        for v in tmp:
            if v == vmname:
                return key
    return None

def getvmid(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    vcmd = ['salt', hyper, 'cmd.run', 'virsh list']
    out = subprocess.check_output(vcmd)

def getvmmac(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    if hyper != None:
        salt_cmd = ['salt', hyper, 'virt.get_macs', hostname]
        out = subprocess.check_output(salt_cmd)
        macs = yaml.load(out)
        if len(macs) > 0:
            return macs[macs.keys()[0]][0]
        else:
            return None
    return None

def getvmip(hypers, hostname, server):
    if isVMactive(hypers, hostname):
        server_url = "http://" + server + "/ip"
        mac = getvmmac(hypers, hostname)
        r = requests.post(server_url, json={"mac":mac})
        return r.text, mac
    else:
        return None, None

def gethyperos(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    salt_cmd = ['salt', '--out', 'yaml', hyper, 'grains.items']
    out = subprocess.check_output(salt_cmd)
    oses = yaml.load(out)
    for key in oses.keys():
        osfullname = oses[key]['osfullname']
    return osfullname

def vmhalt(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    destroy = "virsh destroy " + hostname
    if hyper != None:
        salt_cmd = ['salt', hyper, 'cmd.run', destroy]
        out = subprocess.check_output(salt_cmd)
    else:
        print("VM not found")

def vmshutdown(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    destroy = "virsh shutdown " + hostname
    if hyper != None:
        salt_cmd = ['salt', hyper, 'cmd.run', destroy]
        out = subprocess.check_output(salt_cmd)
    else:
        print("VM not found")

def vmreboot(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    destroy = "virsh reboot " + hostname
    if hyper != None:
        salt_cmd = ['salt', hyper, 'cmd.run', destroy]
        out = subprocess.check_output(salt_cmd)
    else:
        print("VM not found")

def vmreset(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    destroy = "virsh reset " + hostname
    if hyper != None:
        salt_cmd = ['salt', hyper, 'cmd.run', destroy]
        out = subprocess.check_output(salt_cmd)
    else:
        print("VM not found")

def vmdelete(hypers, vmcfgdir, hostname):
    xmlpath = vmcfgdir + "/" + hostname + ".xml"
    saltkeypath = "/etc/salt/pki/master/minions/" + hostname
    if os.path.exists(saltkeypath):
        os.remove(saltkeypath)
    if os.path.exists(xmlpath):
        cfg = load_xml(hostname, xmlpath)
        imgpath = cfg[hostname]['disk']
        try:
            os.remove(imgpath)
            os.remove(xmlpath)
        except OSError as oer:
            print(oer)
        else:
            print(None)

def vmlistfull(hypers, server):
    vms = getactivevms(hypers)
    v = {}
    for key in vms.keys():
        numitems = len(vms[key])
        v[key] = []
        for x in range(numitems):
            name = vms[key][x]
            ip = getvmip(key, name, server)
            v[key].append({name:ip})
    print(v)

def hyperlist_list(hypers):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'test.ping']
    out = subprocess.check_output(salt_cmd)
    hl = yaml.load(out)
    h = []
    for key in hl.keys():
        if hl[key] == True:
            h.append(key)
    return h

def vmsatrest(hypers, vmcfgdir):
    vmlist = {}
    activevms = getactivevms(hypers)
    vmcfgdirl = "*.xml"
    listcmd = ['ls', vmcfgdir]
    hyperlist = hyperlist_list(hypers)
    hyper = hyperlist[0]
    os.chdir(vmcfgdir)
    tmplist = []
    out = subprocess.check_output(listcmd)
    for f in out.decode('utf-8').split():
        ext = f[len(f) - 4:]
        if ext == ".xml":
            name = f[:len(f) - 4]
            if activevms != None:
                for key in activevms.keys():
                    if name not in activevms[key] and name not in tmplist:
                        tmplist.append(name)
            else:
                tmplist.append(name)
        if len(tmplist) > 0:
            vmlist[vmcfgdir] = tmplist
    if len(vmlist) > 0:
        return vmlist
    else:
        return None

def getvmlocationatrest(hypers, hostname, vols):
    atrest = vmsatrest(hypers, vols)
    if atrest != None:
        for key in atrest.keys():
            names = atrest[key]
            for name in names:
                if hostname == name:
                   print(key)
                   return name, key
    return None, None

def getvmxmlfile(hostname, mode="local", vmdir=None):
    if mode == "local":
        xmlfile = vmdir + "/" + hostname + ".xml"
        try:
            tree = ET.parse(xmlfile)
        except FileNotFoundError as fer:
            return None
        root = tree.getroot()
    return root

def getvmos(hypers, hostname, xmlmode, vmdir):
    hyper = gethyperbyvmname(hypers, hostname)
    root = getvmxmlfile(hostname, xmlmode, vmdir)
    for desc in root.iter('description'):
        osname = desc.text
    return osname

def vmstatus(hypers, hostname):
    hyper = gethyperbyvmname(hypers, hostname)
    if hyper != None:
        salt_cmd = ['salt', '--out', 'yaml', hyper, 'virt.vm_info']
        out = subprocess.check_output(salt_cmd)
        vms = yaml.load(out)
        for key in vms[hyper].keys():
            if key == hostname:
                return {hyper:vms[hyper][hostname]['state']}
    return None

def vmmigrate_shared_storage(hypers, hostname, dest_hyper, vmcfgdir, timeout):
    hyper = gethyperbyvmname(hypers, hostname)
    if hyper != dest_hyper:
        vmshutdown(hypers, hostname)
        while isVMactive(hypers, hostname):
            time.sleep(timeout)
            print("Waiting...")
        #chk1, vol = getvmlocationatrest(hypers, hostname, vmcfgdir)
        vmstart(dest_hyper, vmcfgdir, hostname)
    else:
        print("VM already running on host: ", dest_hyper)
