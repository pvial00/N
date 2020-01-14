import os, subprocess
import xml.etree.ElementTree as ET

def cp_new_img_debian(path, hostname):
    newimg = "/vm/" + hostname + ".img"
    cp_cmd = ['cp', '/vm/debian.img', newimg]
    out = subprocess.check_output(cp_cmd)

def mountos_img_debian(imgpath, mntpath, device):
    losetup_cmd = ['losetup', '-f', '-P', imgpath]
    out = subprocess.check_output(losetup_cmd)
    mnt_cmd = ['mount', device, mntpath]
    out = subprocess.check_output(mnt_cmd)

def umountos_img_debian(mntpath):
    umount_cmd = ['umount', mntpath]
    out = subprocess.check_output(umount_cmd)
    losetup_cmd = ['losetup', '-d', '/dev/loop0']
    out = subprocess.check_output(losetup_cmd)

def mountos_img_freebsd(imgpath, mntpath, device):
    losetup_cmd = ['losetup', '-f', '-P', imgpath]
    out = subprocess.check_output(losetup_cmd)
    #kpartx -av /dev/loop0
    #zpool import -R /mnt/tmp -d /dev/mapper
    #pool import -f -d /dev/mapper 4303737221853188784 zroot -R /mnt/tmp

def sethostname_debian(path, hostname):
    path += "/etc/hostname"
    f = open(path, "w")
    f.write(hostname)
    f.close()

def gensshkeys_debian(path):
    ecdsa_path = path + "/etc/ssh/ssh_host_ecdsa_key"
    ecdsa_path_pub = path + "/etc/ssh/ssh_host_ecdsa_key.pub"
    os.remove(ecdsa_path)
    os.remove(ecdsa_path_pub)
    ecdsa_cmd = ['ssh-keygen', '-N', '""', '-q', '-t', 'ecdsa', '-f', ecdsa_path]
    out = subprocess.check_output(ecdsa_cmd)

    rsa_path = path + "/etc/ssh/ssh_host_rsa_key"
    rsa_path_pub = path + "/etc/ssh/ssh_host_rsa_key.pub"
    os.remove(rsa_path)
    os.remove(rsa_path_pub)
    rsa_cmd = ['ssh-keygen', '-N', '""', '-q', '-t', 'rsa', '-f', rsa_path]
    out = subprocess.check_output(rsa_cmd)
    
    ed_path = path + "/etc/ssh/ssh_host_ed25519_key"
    ed_path_pub = path + "/etc/ssh/ssh_host_ed25519_key.pub"
    os.remove(ed_path)
    os.remove(ed_path_pub)
    ed_cmd = ['ssh-keygen', '-N', '""', '-q', '-t', 'ed25519', '-f', ed_path]
    out = subprocess.check_output(ed_cmd)

def gen_random_mac():
    tmp = os.urandom(6)
    m = ""
    for b in tmp:
        m += str(b.encode('hex')) + ":"
    m = m[:len(m) - 1]
    return m

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

def vminit_debian(path, hostname, cpus, mem, part):
    imgpath = "/vm/" + hostname + ".img"
    cp_new_img_debian(path, hostname)
    mountos_img_debian(imgpath, path, part)
    sethostname_debian(path, hostname)
    gensshkeys_debian(path)
    umountos_img_debian(path)
    mac_addr = gen_random_mac()
    cfg_xml("/vm", "debian-template.xml", hostname, mac_addr, imgpath, cpus, mem)

vminit_debian("/mnt/tmp", "testname", 1, 1572864, "/dev/loop0p1")
