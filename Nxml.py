import os, subprocess
import xml.etree.ElementTree as ET
import yaml, requests

def chg_cfg_xml_vmpath(vol, filename, hostname, vmpath):
    tree = ET.parse(filename)
    root = tree.getroot()
    for devs in root.iter('disk'):
        devs[0].attrib['file'] = vmpath
    tree.write(outfilename)

def add_disk(vmname, vmpath, path):
    tree = ET.parse(filename)
    root = tree.getroot()

