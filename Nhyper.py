import subprocess, yaml

def hyperreboot(hyper):
    salt_cmd = ['salt', '--out', 'yaml', hyper, 'cmd.run', 'reboot']

def hyperloadavg(hypers):
    salt_cmd = ['salt', '--out', 'yaml', hypers, 'status.loadavg']
    out = subprocess.check_output(salt_cmd)
    loads = yaml.load(out)
    print(loads)
    load = 0
    for key in loads.keys():
        load += loads[key]
    return load
