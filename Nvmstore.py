import glob

def vmstorelist(storedir):
    path = storedir + "/" + "*.img"
    imgs = glob.glob(path)
    print(imgs)
