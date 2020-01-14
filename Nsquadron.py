from Nvminit import *
from Ndefaults import *
from Nsquads import *
from Nresource_mgr import *

def vmcreate_squad(hypers, vols, vmcfgdir, target):
    for squad in squads:
        for sqname in squad.keys():
            if sqname == target:
                for name in squad[sqname].keys():
                    print(name)
                    vmtype = squad[sqname][name]
                    virt_details = virt_types[vmtype]
                    cpus = virt_types[vmtype]['vcpus']
                    mem = virt_types[vmtype]['memory']
                    osname = virt_types[vmtype]['ostype']
                    ostype = ostypes[osname]
                    disk = storagetypes[ostype]

                    hypers = select_avail_hyper(hypers, int(cpus), int(mem), hyper_select, remote_storage_vols)
                    vmdir= select_avail_storage(hypers, vols)

                    if ostype == 0:
                        vminit_debian(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir)
                        vmstart(hypers, vmcfgdir, name)
                    elif ostype == 1:
                        vminit_freebsd(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir)
                        vmstart(hypers, vmcfgdir, name)
                    elif ostype == 2:
                        vminit_solaris(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir)
                        vmstart(hypers, vmcfgdir, name)
                    elif ostype == 3:
                        vminit_openbsd(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir)
                        vmstart(hypers, vmcfgdir, name)
                    elif ostype == 4:
                        vminit_netbsd(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir)
                        vmstart(hypers, vmcfgdir, name)
                    elif ostype == 5:
                        vminit_minix(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir)
                        vmstart(hypers, vmcfgdir, name)
                    elif ostype == 6:
                        vminit_windows(workdir, builddir, vmdir, name, cpus, mem, rootparts[ostype], xmltemplates[ostype], vmimages[ostype], mac_prefix, vmcfgdir)
                        vmstart(hypers, vmcfgdir, name)

def vmdelete_squad(hypers, vmcfgdir, target):
    for squad in squads:
        for sqname in squad.keys():
            if sqname == target:
                for name in squad[sqname].keys():
                    print(name)
                    if isVMactive(hypers, name):
                        vmhalt(hypers, name)
                    vmdelete(hypers, vmcfgdir, name)
