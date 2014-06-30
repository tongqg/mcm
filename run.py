#!/usr/bin/python

from mcm import config, instance, domain
from mcm import configdrive as cd
from mcm.util import remote
import logging, sys, getopt

configFile = config.loadConfig("servers.conf")
hosts = configFile['hypervisors']
log = logging.getLogger("main")

# def defineAll():
# 	for host in hosts:
# 		hv = instance.HyperVisor(host['hostname'], host['username'])
# 		df = domain.DomainFactory(host['emulator'], host['arch'], host['machine'])
# 		for server in host['servers']:
# 			__defineServer(hv, server, df)


# def startAll():
# 	for host in hosts:
# 		hv = instance.HyperVisor(host['hostname'], host['username'])
# 		for server in host['servers']:
# 			hv.startDomain(server['name'])

def killServer(hypername, servername):
	for host in hosts:
		if (host['name'] == hypername):
			hv = instance.HyperVisor(host['hostname'], host['username'], host['vmpath'], host['image'])
			for server in host['servers']:
				if (server['name'] == servername):
					hv.destroyDomain(server['name'])
				else:
					log.debug("can't find server " + servername + " in host " + hypername)
		else:
			log.debug("can't find host " + hypername)

def bootServer(hypername, servername):
	for host in hosts:
		if (host['name'] == hypername):
			hv = instance.HyperVisor(host['hostname'], host['username'], host['vmpath'], host['image'])
			df = domain.DomainFactory(host['emulator'], host['arch'], host['machine'])
			for server in host['servers']:
				if (server['name'] == servername):
					__defineServer(hv, server, df)
					hv.startDomain(server['name'])
				else:
					log.debug("can't find server " + servername + " in host " + hypername)
		else:
			log.debug("can't find host " + hypername)

def __defineServer(hypervisor, serverjson, df):
	cdfile = __buildcdiso(hypervisor, serverjson)
	imagepath = serverjson['vda']
	if (hypervisor.image is not None):
		# replace vda setting in individual server
		imagename = hypervisor.image[hypervisor.image.rindex('/')+1:]
		imagepath = hypervisor.vmpath+"/"+serverjson['name']+"/" +imagename
		log.debug("copying file from {0} {1}".format(hypervisor.image, imagepath))
		remote.run(hypervisor.hostname, hypervisor.username, "cp {0} {1}".format(hypervisor.image, imagepath))
		log.debug("copied")
	consolefile = hypervisor.vmpath+"/"+serverjson['name']+"/console.log"
	domainxml = df.gen(serverjson['name'], serverjson['vcpu'], serverjson['mem'], serverjson['memunit'], imagepath, cdfile, consolefile)
	log.debug("server "+serverjson['name']+"\n\n" + domainxml +"\n")
	hypervisor.defineDomain(serverjson['name'], domainxml)


def __buildcdiso(hypervisor, serverjson):
	tmpfile = '/tmp/config.iso'
	configDriveRoot = '/tmp/cd'
	cd.buildCDStructure(configDriveRoot)
	eth0=None
	eth0mask=None
	eth0gateway=None
	eth1=None
	eth1mask=None
	eth1gateway=None

	for nic in serverjson['nic']:
		if nic['id'] == 0:
			eth0=nic['ip']
			eth0mask = nic['netmask']
			eth0gateway = nic['gateway']
		else:
			eth1=nic['ip']
			eth1mask = nic['netmask']
			eth1gateway = nic['gateway']
	cd.createMetaDataFile(configDriveRoot, serverjson['name'], serverjson['hostname'], eth0, eth0mask, eth0gateway, eth1, eth1mask, eth1gateway)
	cd.createUserDataFile(configDriveRoot, eth0, eth1)
	cd.createCD(configDriveRoot, tmpfile)
	remotefile = hypervisor.vmpath+"/"+serverjson['name']+"/config.iso"
	log.debug("created config drive locally. copy it to remote server {0} at path {1}".format(hypervisor.hostname, remotefile))
	remote.copy(hypervisor.hostname, hypervisor.username, tmpfile, remotefile)
	log.debug("copy finished")
	return remotefile

def main():
	def usage():
		return 'run.py -b/-k -r <kvm server> -s <vm name>'
	action = ''
	hyper=''
	server=''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hbkr:s:")
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print usage()
			sys.exit()
		elif opt == '-b':
			action = 'boot'
		elif opt == '-k':
			action = 'kill'
		elif opt == '-r':
			hyper = arg
		elif opt == '-s':
			server = arg

	if (hyper == '' or action == '') :
		print usage()
		sys.exit(2)

	if (action=='boot'):
   		bootServer(hyper, server)
   	elif (action == 'kill'):
   		killServer(hyper, server)

if __name__ == "__main__":
   	main()