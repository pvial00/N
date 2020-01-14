import subprocess, os

def preseed_debian(workdir, mntdir, src_iso, dst_iso, seed):
    #random_dir = os.random(16)

    workdir += "/"
    mnt_cmd = ['mount', src_iso, mntdir, '-o', 'loop']
    out = subprocess.check_output(mnt_cmd)
    cp_cmd = ['cp', '-rT', mntdir, workdir]
    out = subprocess.check_output(cp_cmd)
    umount_cmd = ['umount', mntdir]
    out = subprocess.check_output(umount_cmd)

    path1 = workdir + "install.amd/"
    chmod_cmd = ['chmod', '+w', '-R', path1]
    out = subprocess.check_output(chmod_cmd)
    path2 = path1 + "initrd.gz"
    gunzip_cmd = ['gunzip', path2]
    out = subprocess.check_output(gunzip_cmd)
    path3 = path1 + "initrd"
    longcmd = "echo " + seed + " | cpio -H newc -o -A -F " + workdir + "install.amd/initrd"
    os.system(longcmd)
    gzip_cmd = ['gzip', '-f', path3]
    chmod_cmd = ['chmod', '-w', '-R', path1]
    out = subprocess.check_output(chmod_cmd)

    md5_path = workdir + "md5sum.txt"
    chmod_cmd = ['chmod', '+w', md5_path]
    out = subprocess.check_output(chmod_cmd)
    os.chdir(workdir)
    md5_cmd = "md5sum `find -follow -type f` > " + workdir +"md5sum.txt"
    os.system(md5_cmd)
    chmod_cmd = ['chmod', '-w', md5_path]
    out = subprocess.check_output(chmod_cmd)

    gen_iso_cmd = ['genisoimage', '-r', '-J', '-b', 'isolinux/isolinux.bin', '-c', 'isolinux/boot.cat', '-no-emul-boot', '-boot-load-size', '4', '-boot-info-table', '-o', dst_iso, workdir]

    out = subprocess.check_output(gen_iso_cmd)
    allbuildfiles = workdir + "*"
    rm_cmd = ['rm', '-fR', allbuildfiles]
    out = subprocess.check_output(rm_cmd)

