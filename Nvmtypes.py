def load_type_cfg(filename):
    f = open(filename, "r")
    cfile = f.read()
    f.close()
    lines = cfile.split('\t')
    profiles = []
    for line in lines:
        print(line)
        profiles.append(eval(line))
    print(profiles)
    return profiles


    
