#!/usr/bin/python
__author__='tongqg'

import logging
import unittest
import os
import shutil
import uuid
import json

def createCD(directoryPath, targetFile='/tmp/config.iso'):
	"""
	this is to create an iso file 
	"""
	os.system("mkisofs -r -J -o "+ targetFile + " " + directoryPath)
	os.system("chcon -t virt_content_t "+ targetFile)

def buildCDStructure(rootPath):
	"""
	create config driver directory structure. the structure is like 
	/openstack
		/latest
			meta_data.json
			user_data
	"""
	if os.path.exists(rootPath):
		shutil.rmtree(rootPath)
	os.makedirs(rootPath+'/openstack/latest')
	os.makedirs(rootPath+'/openstack/content')

def createMetaDataFile(configDriveRoot, name, hostname, eth0, eth0mask, eth0gateway, eth1=None, eth1mask=None, eth1gateway=None):
	metadata = {}
	metadata['hostname'] = hostname
	metadata['name'] = name
	metadata['launch_index'] = 0
	metadata['uuid'] = str(uuid.uuid1())
	metadata['public_key'] = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyNkH1qAgUbAM1dgOxwz+P0hrnKgV1Bdi6QKyB6PrwvdCPsyO18Wrwq5gTOEMnrfGzEMlRqRDbyvoLE7ooWx+x0XVH2IeZVBSaJ27CvMSROU8o1Ef7Usi6ujOk6FgQySZAcC1LJ+61UoyipeDzXJ5EzjWKIlqEK/YKwStS/8O0r+2U3ia0eDmMw/RXz/nowLDwr3hIIIMh/Pk7DcNaRrdN8IacrsyV0Ht23U5vHBNMjyfDC8BcZJC5Mgdc3DBc0waHpvDeJiQMCYvVDdpTAj5GijjzCAGl5f0bqpfZ2FHxrWHsC59ve1GREdiQkFOsa4EvYVG8KOwwiYbR9/jMoVNYQ== generated'
	files = []
	if (eth0 != None):
		files.append(configureContentFileForNetwork(configDriveRoot, 0, eth0, eth0mask, eth0gateway))
	if (eth1 != None):
		files.append(configureContentFileForNetwork(configDriveRoot, 1, eth1, eth1mask, eth1gateway))
	metadata['files'] = files
	f = open(configDriveRoot+"/openstack/latest/meta_data.json", "w")
	f.write(json.dumps(metadata)+"\n")
	f.close()



def configureContentFileForNetwork(configDriveRoot, numofnic, ip, mask, gateway):
	contentpath = "/content/ifcfg-eth"+ str(numofnic)
	f = open(configDriveRoot+'/openstack'+contentpath, 'w')
	f.write(ifcfg_script(numofnic, ip, mask, gateway))
	f.close
	meta = {}
	meta['content_path'] = contentpath
	meta['path'] = '/etc/sysconfig/network-scripts/ifcfg-eth' + str(numofnic)
	return meta


def ifcfg_script(numofnic, ip, mask, gateway):
	return ("DEVICE=eth{0}\n"+
	"TYPE=Ethernet\n"+
	"BOOTPROTO=static\n"+
	"ONBOOT=yes\n"+
	"NM_CONTROLLED=no\n"+
	"IPADDR={1}\n"+
	"NETMASK={2}\n"+
	"GATEWAY={3}\n").format(numofnic, ip, mask, gateway)


def createUserDataFile(configDriveRoot, eth0, eth1):
	metadata = "#cloud-config\n\nruncmd:\n"
	if eth0 is not None:
		metadata = metadata + " - ip addr add {0} dev eth0\n".format(eth0)
	if eth1 is not None:
		metadata = metadata + " - ip addr add {0} dev eth1\n".format(eth1)
	f = open(configDriveRoot+"/openstack/latest/user_data", "w")
	f.write(metadata)
	f.close()

class UnitTest(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)

	def test_cd(self):
		configDriveRoot = '/tmp/cd'
		buildCDStructure(configDriveRoot)
		createMetaDataFile(configDriveRoot, 'testname', 'test.host', None, None, None, 'ip', 'mask','gateway')
		createUserDataFile(configDriveRoot, 'ip0', 'ip1')
		createCD(configDriveRoot)
		os.system("mount -o loop -t iso9660 /tmp/config.iso /mnt")
		os.system("ls /mnt/openstack/")
		os.system("ls /mnt/openstack/content")
		os.system("cat /mnt/openstack/content/ifcfg-eth0")
		os.system("ls /mnt/openstack/latest")
		os.system("cat /mnt/openstack/latest/meta_data.json")
		os.system("cat /mnt/openstack/latest/user_data")
		os.system("umount /mnt")

if __name__ == "__main__":
	unittest.main()
