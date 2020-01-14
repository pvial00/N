def cmdlist():
    cmds = ['vmcreate', 'vmlist', 'vmstart', 'vmshutdown', 'vmdelete', 'vmmac', 'vmip', 'vmlistfull', 'freecpus', 'freemem', 'capacity', 'vmatrest', 'vmos', 'vmhalt', 'vmstartall', 'vmshutdownall']
    for cmd in cmds:
        print(cmd)
