from Nvminit import *
from Nresource_mgr import *
from Ndefaults import *
from Nos import *
from Nvmstore import *
from Ncmd import *
from Nstorage import *
from Nhyper import *
from Nvmtypes import *
from Nsquadron import *
import sys, getopt

def vmcreate_usage():
    print("N.py vmcreate -c 1 -m 1572864 -n vmname")

def vmdeploy_usage():
    print("N.py vmdeploy -h hypervisor -n vmname")

def vmlist_usage():
    print("N.py vmlist")

def vmdelete_usage():
    print("N.py vmdelete vmname")

cmd = sys.argv[1]
if cmd == "vmcreate":
    hypers = None
    target_squad = None
    name = sys.argv[2]
    try:
        opts, args = getopt.getopt(sys.argv[3:],"?:c:m:h:o:t:s:",["help", "cpus=", "mem=", "name="])
    except getopt.GetoptError as err:
        print(err)
        vmcreate_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-?':
            vmcreate_usage()
            sys.exit(0)
        elif opt in ("-h", "--hyper"):
            hyper_prefix = arg
        elif opt in ("-c", "--cpu"):
            cpus = arg
        elif opt in ("-m", "--mem"):
            mem = arg
        elif opt in ("-o", "--os"):
            osname = arg
            ostype = ostypes[osname]
            disk = storagetypes[ostype]
        elif opt in ("-t", "--type"):
            vmtype = arg
            for td in virt_types:
                for key in td.keys():
                    if vmtype == key:
                        cpus = td[key]['vcpus']
                        mem = td
        elif opt in ("-s", "--squad"):
            target_squad = arg
    if target_squad == None:
        if not isCapacity(hyper_prefix, int(cpus), int(mem), disk, remote_storage_vols):
            print("Not enough capacity")
            sys.exit(3)
        if hypers == None:
            hypers = select_avail_hyper(hyper_prefix, int(cpus), int(mem), hyper_select, remote_storage_vols)
        if storage_default == "remote":
            vmdir= select_avail_storage(hypers, remote_storage_vols)
        elif storage_default == "local":
            vmdir= select_avail_storage(hypers, local_storage_vols)

        if ostype == 0:
            vminit_debian(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 1:
            vminit_freebsd(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 2:
            vminit_solaris(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 3:
            vminit_openbsd(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 4:
            vminit_netbsd(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 5:
            vminit_minix(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 6:
            vminit_windows(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 7:
            vminit_macos(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 8:
            vminit_krypto(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 9:
            vminit_freebsd_salt(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 10:
            vminit_oracle_linux(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 11:
            vminit_oracle_linux_salt(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 12:
            vminit_oracle_linux_salt(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 13:
            vminit_oracle_linux_salt(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)
        elif ostype == 14:
            vminit_solaris(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir, storage_default)
            vmstart(hypers, vmcfgdir, name)

elif cmd == "vmdelete":
    force = False
    name = sys.argv[2]
    try:
        opts, args = getopt.getopt(sys.argv[2:],"f:",["help", "cpus=", "mem=", "name="])
    except getopt.GetoptError as err:
        print(err)
        vmdeploy_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-?':
            vmdeploy_usage()
            sys.exit(0)
        elif opt in ("-f", "--force"):
            force = True
    if force == False:
        warn = "Warning: You are about to delete VM " + name + " Confirm Y/N"
        q = input(warn)
        if q == "y" or q == "Y":
            if isVMactive(hyper_prefix, name) == True:
                vmhalt(hyper_prefix, name)
            vmdelete(hyper_prefix, vmcfgdir, name)
        elif q == "n" or q == "N":
            pass
    else:
        if isVMactive(hyper_prefix, name) == True:
            vmhalt(hyper_prefix, name)
        vmdelete(hyper_prefix, vmcfgdir, name)
elif cmd == "vmstart":
    hypers = None
    name = sys.argv[2]
    try:
        opts, args = getopt.getopt(sys.argv[3:],"h:n:",["help", "cpus=", "mem=", "name="])
    except getopt.GetoptError as err:
        print(err)
        vmdeploy_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-?':
            vmdeploy_usage()
            sys.exit(0)
        elif opt in ("-h", "--hypervisor"):
            hypers = arg
    cpus, mem, vol = load_resources_from_xml(hyper_prefix, name, vmcfgdir)
    if hypers == None:
        hyper = select_avail_hyper(hyper_prefix, int(cpus), int(mem), hyper_select, list(vol))
        if isVMactive(hyper_prefix, name) == False:
            vmstart(hyper, vol, name)
        else:
            print("VM is already active")
    else:
        if isVMactive(hyper_prefix, name) == False:
            vmstart(hypers, vol, name)
        else:
            print("VM is already active")
elif cmd == "vmhalt":
    name = sys.argv[2]
    vmhalt(hyper_prefix, name)
elif cmd == "vmshutdown":
    name = sys.argv[2]
    vmshutdown(hyper_prefix, name)
elif cmd == "vmreboot":
    name = sys.argv[2]
    vmreboot(hyper_prefix, name)
elif cmd == "vmreset":
    name = sys.argv[2]
    vmreboot(hyper_prefix, name)
elif cmd == "vmlist":
    try:
        hyper_prefix = sys.argv[2]
    except IndexError as ier:
        pass
    vms = getactivevms(hyper_prefix)
    print(vms)
elif cmd == "freecpus":
    try:
        hyper_prefix = sys.argv[2]
    except IndexError as ier:
        pass
    cpus = getfreecpus(hyper_prefix)
    print(cpus)
elif cmd == "freemem":
    try:
        hyper_prefix = sys.argv[2]
    except IndexError as ier:
        pass
    mems = getfreemems(hyper_prefix)
    print(mems)
elif cmd == "hyperusage":
    h = getfreeresourceshyper(hyper_prefix, remote_storage_vols)
    print(h)
elif cmd == "capacity":
    try:
        hyper_prefix = sys.argv[2]
    except IndexError as ier:
        pass
    cpufree, memfree, totalcpus, totalmem, usedcpus, usedmem, availdisk, useddisk, totaldisk, freedisk = getcapacity(hyper_prefix, remote_storage_vols)
    print("Total CPUs: ", totalcpus)
    print("Available CPUs: ", usedcpus)
    print("Available Memory in MB: ", usedmem)
    print("Total Memory in MB: ", totalmem)
    print("% of CPUs free: ", cpufree)
    print("% of Memory free: ", memfree)
    print("% of Disk Space free: ", freedisk)
    print("Total storage space in MB:", totaldisk)
    print("Available storage space in MB: ", availdisk)
    print("Used storage space in MB: ", useddisk)
elif cmd == "vmmac":
    mac = getvmmac(hyper_prefix, sys.argv[2])
    print(mac)
elif cmd == "vmip":
    ip, mac = getvmip(hyper_prefix, sys.argv[2], Nnet_server)
    print(ip)
elif cmd == "vmlistfull":
    vmlistfull(hyper_prefix, Nnet_server)
elif cmd == "preseed_debian":
    preseed_debian(osworkdir, isomntdir, debian_iso, debian_kustom_iso, debian_seed)
elif cmd == "vmatrest":
    vmlist = vmsatrest(hyper_prefix, vmcfgdir)
    print(vmlist)
elif cmd == "vmos":
    osname = getvmos(hyper_prefix, sys.argv[2], xmlfetch_mode, vmdir)
    print(osname)
elif cmd == "help":
    cmdlist()
elif cmd == "hyperreboot":
    warn = "Warning: You are about to reboot " + sys.argv[2] + " Confirm Y/N"
    q = input(warn)
    if q == "y" or q == "Y":
        hyperreboot(sys.argv[2])
elif cmd == "hyperhalt":
    warn = "Warning: You are about to halt " + sys.argv[2] + " Confirm Y/N"
    q = input(warn)
    if q == "y" or q == "Y":
        hyperhalt(sys.argv[2])
elif cmd == "freestorage":
    try:
        hyper_prefix = sys.argv[2]
    except IndexError as ier:
        pass
    report = getfreespace_remote(hyper_prefix, remote_storage_vols)
    print(report)
elif cmd == "vols":
    sr = volume_list(hyper_prefix, remote_storage_vols)
    print(sr)
elif cmd == "volslocal":
    report = getfreespace_local_report(hyper_prefix, local_storage_vols)
    print(report)
elif cmd == "freelocal":
    avail = getfreespace_local(hyper_prefix, local_storage_vols)
    print(avail)
elif cmd == "hyperselect":
    hypers = None
    try:
        opts, args = getopt.getopt(sys.argv[2:],"?:c:m:h:o:",["help", "cpus=", "mem=", "name="])
    except getopt.GetoptError as err:
        print(err)
        vmcreate_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-?':
            vmcreate_usage()
            sys.exit(0)
        elif opt in ("-h", "--hyper"):
            hyper_prefix = arg
        elif opt in ("-c", "--cpu"):
            cpus = arg
        elif opt in ("-m", "--mem"):
            mem = arg
        elif opt in ("-o", "--os"):
            osname = arg
    ostype = ostypes[osname]
    disk = storagetypes[ostype]
    if not isCapacity(hyper_prefix, int(cpus), int(mem), disk, remote_storage_vols):
        print("Not enough capacity")
        sys.exit(3)
    if hypers == None:
        hypers = select_avail_hyper(hyper_prefix, int(cpus), int(mem), hyper_select, remote_storage_vols)
        print(hypers)
elif cmd == "hyperlist":
    hypers = hyperlist_list(hyper_prefix)
    print(hypers)
elif cmd == "mountvol":
    volume_mount_nfs(hyper_prefix, sys.argv[2], sys.argv[3], sys.argv[4]) 
elif cmd == "vmstatus":
    state = vmstatus(hyper_prefix, sys.argv[2])
    print(state)
elif cmd == "storselect":
    vol = select_avail_storage(sys.argv[2], remote_storage_vols)
    print(vol)
elif cmd == "vmstartall":
    out = vmstartall(hyper_prefix, remote_storage_vols, hyper_select, vmcfgdir)
elif cmd == "vmshutdownall":
    try:
        opts, args = getopt.getopt(sys.argv[2:],"?:c:m:h:o:",["help", "cpus=", "mem=", "name="])
    except getopt.GetoptError as err:
        print(err)
        vmcreate_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-?':
            vmcreate_usage()
            sys.exit(0)
        elif opt in ("-h", "--hyper"):
            hyper_prefix = arg
    out = vmshutdownall(hyper_prefix, remote_storage_vols, hyper_select, vmcfgdir)
elif cmd == "vmmigrate":
    try:
        opts, args = getopt.getopt(sys.argv[2:],":h:",[])
    except getopt.GetoptError as err:
        print(err)
        vmcreate_usage()
        sys.exit(2)
    for opt, arg in opts:
        print(arg)
        if opt == '-?':
            vmcreate_usage()
            sys.exit(0)
        elif opt in ("-h", "--hyper"):
            dest_hyper = arg
    out = vmmigrate_shared_storage(hyper_prefix, sys.argv[2], sys.argv[3], vmcfgdir, 8)
elif cmd == "loadavg":
   loadavg = hyperloadavg(hyper_prefix)
   print(loadavg)
elif cmd == "loadcfg":
   load_type_cfg(server_profiles)
elif cmd == "squaddeploy":
    squad = sys.argv[2]
    squaddeploy(hyper_prefix, remote_storage, vmcfg, squad)
elif cmd == "squadcreate":
    target_squad = sys.argv[2]
    vmcreate_squad(hyper_prefix, remote_storage_vols, vmcfgdir, target_squad)
elif cmd == "squaddelete":
    target_squad = sys.argv[2]
    vmdelete_squad(hyper_prefix, vmcfgdir, target_squad)
elif cmd == "volattach":
    volume_attach(hyper_prefix, sys.argv[2], sys.argv[3], sys.argv[4], remote_storage_vols)
elif cmd == "voldetach":
    result = volume_detach(hyper_prefix, sys.argv[2], sys.argv[3])
    if result == "False":
        print("Unable to find volume", sys.argv[2])
    else:
        print("Success")
elif cmd == "voldelete":
    volume_delete(hyper_prefix, sys.argv[2])
elif cmd == "vollist":
    vols = volumes_list(hyper_prefix, sys.argv[2])
    print(vols)
else:
    print("Command not found")

