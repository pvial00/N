hyper_prefix = "hyper*"
vmcfgdir = "/srv/vmcfg"
isodir = "/iso"
workdir = "/mnt/tmp"
isomntdir = "/mnt/iso"
builddir = "/build"
osworkdir = "/build/tmp"
vmdir = "/vm"
mac_prefix = "66:"
Nnet_server = "thrash.knet:5000"
default_user = "n"
hyper_select = "least"
xmlfetch_mode = "local"
debian_iso = "/iso/debian-10.2.0-amd64-netinst.iso"
debian_kustom_iso = "/build/debian-10.2.0-amd64-kustom.iso"
debian_seed = "/build/debian-preseed.cfg"
defaultos = 0
ostypes = {'debian':0, 'freebsd':1, 'solaris':2, 'openbsd':3, 'netbsd':4, 'minix':5,'windows-server':6,'macos':7, 'krypto':8, 'freebsd-salt':9}
xmltemplates = {0:'/build/debian-template.xml', 1:'/build/freebsd.xml', 2:'/build/solaris.xml', 3:'/build/openbsd.xml', 4:'/build/netbsd.xml', 5:'/build/minix.xml',6:'/build/windows.xml',7:'/build/macos.xml', 8:'/build/debian-template.xml', 9:'/build/freebsd.xml'}
vmimages = {0:'/build/debian.img', 1:'/build/freebsd.img', 2:'/build/solaris.img', 3:'/build/openbsd.img', 4:'/build/netbsd.img',5:'/build/minix.img',6:'/build/windows.img',7:'/build/macos.img', 8:'/build/debian-salt.img', 9:'/build/freebsd-salt.img'}
rootparts = {0:"p1", 1:"/dev/loop0p1", 2:"/dev/loop0p1", 3:"/dev/loop0p1", 4:"/dev/loop0p1", 5:"/dev/loop0p1",6:"changeme",7:"changeme", 8:"p1", 9:"changeme"}
storagetypes = {0:10000, 1:10000, 2:20000, 3:10000, 4:10000, 5:10000, 6:20000, 7:30000, 8:10000, 9:10000}
remote_storage_vols = ['/vm', '/cont1', '/cont2', '/cont3', '/cont4']
local_storage_vols = ['/']
storage_default = "remote"
availability_groups = ['*']
cli_mode = "developer"
server_profiles="server.profile"
virt_types={'virt-default-debian':{'ostype':'debian', 'vcpus':1, 'memory':2048, 'rootsize':10000, 'rootdisk':'/build/debian.img'},'virt-default-freebsd':{'ostype':'freebsd', 'vcpus':1, 'memory':2048, 'rootsize':10000, 'rootdisk':'/build/freebsd.img'}, 'virt-default-solaris':{'ostype':'solaris', 'vcpus':1, 'memory':4096, 'rootsize':20000, 'rootdisk':'/build/solaris.img'}, 'virt-default-netbsd':{'ostype':'netbsd', 'vcpus':1, 'memory':1024, 'rootsize':10000, 'rootdisk':'/build/netbsd.img'}, 'virt-default-openbsd':{'ostype':'openbsd', 'vcpus':1, 'memory':1024, 'rootsize':10000, 'rootdisk':'/build/openbsd.img'},'virt-default-minix':{'ostype':'minix', 'vcpus':1, 'memory':256, 'rootsize':10000, 'rootdisk':'/build/minix.img'}}
