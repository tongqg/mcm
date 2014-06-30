#!/usr/bin/python

from mcm import config, instance, domain
import logging, sys, getopt

configFile = config.loadConfig("servers.conf")

hosts = configFile['hypervisors']

log = logging.getLogger("main")

def defineAll():
	for host in hosts:
		hv = instance.HyperVisor(host['hostname'], host['username'])
		df = domain.DomainFactory(host['emulator'], host['arch'], host['machine'])
		for server in host['servers']:
			__defineServer(hv, server, df)


def startAll():
	for host in hosts:
		hv = instance.HyperVisor(host['hostname'], host['username'])
		for server in host['servers']:
			hv.startDomain(server['name'])

def stopServer(hypername, servername):
	for host in hosts:
		if (host['name'] == hypername):
			hv = instance.HyperVisor(host['hostname'], host['username'])
			for server in host['servers']:
				if (server['name'] == servername):
					hv.stopDomain(server['name'])
				else:
					log.debug("can't find server " + servername + " in host " + hypername)
		else:
			log.debug("can't find host " + hypername)

def bootServer(hypername, servername):
	for host in hosts:
		if (host['name'] == hypername):
			hv = instance.HyperVisor(host['hostname'], host['username'])
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
	hypervisor.defineDomain(serverjson['name'], df.gen(serverjson['name'], serverjson['vcpu'], serverjson['mem'], serverjson['memunit'], serverjson['vda']))

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
	print opts
	for opt, arg in opts:
		print opt
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
   		stopServer(hyper, server)

if __name__ == "__main__":
   	main()