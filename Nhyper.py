import subprocess, yaml

def hyperreboot(hyper):
    salt_cmd = ['salt', '--out', 'yaml', hyper, 'cmd.run', 'reboot']
    out = subprocess.check_output(salt_cmd)

def hyperhalt(hyper):
    salt_cmd = ['salt', '--out', 'yaml', hyper, 'cmd.run', '/usr/sbin/halt -p']
    out = subprocess.check_output(salt_cmd)

def hyperloadavg(hypers):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'status.loadavg']
    out = subprocess.check_output(salt_cmd)
    loads = yaml.load(out)
    load1 = 0
    load5 = 0
    load15 = 0
    for key in loads.keys():
        load1 += loads[key]['1-min']
        load5 += loads[key]['5-min']
        load15 += loads[key]['15-min']
    return [load1, load5, load15]
