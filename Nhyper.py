def hyperreboot(hyper):
    salt_cmd = ['salt', '--out', 'yaml', hyper, 'cmd.run', 'reboot']
