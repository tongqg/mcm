#!/usr/bin/python

from mcm import config
import sys, getopt,json

def main():
	def usage():
		return "getconfig.py -j <simple json> -o <json file used for mcm> -i <instanceid>"
	infile = ''
	outfile = ''
	instanceid = ""
	managementsite = ""
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hj:o:i:m:")
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print usage()
			sys.exit()
		if opt == "-j":
			infile = arg
		elif opt == "-o":
			outfile = arg
		elif opt == "-i":
			instanceid = arg
		elif opt == "-m":
			managementsite = arg

	if (infile == '' or outfile == '' or instanceid == '' or managementsite == ''):
		print usage()
	else:
		transform(infile, outfile,instanceid, managementsite)

def transform (infile, outfile, instanceid, mgmtst):
	print infile+outfile
	inj = config.loadConfig(infile)
	outj = {"hypervisors":[]}
	network= inj["network-prefix"] + "." + instanceid
	for ihyper in inj["hypervisors"]:
		ohyper = {}
		ohyper["name"] = ihyper["name"]
		ohyper["hostname"] = network + "." + ihyper["hostip"]
		ohyper["username"] = "root"
		ohyper["emulator"] = "/usr/libexec/qemu-kvm"
		ohyper["arch"] = "x86_64"
		ohyper["machine"] = "rhel6.5.0"
		ohyper["vmpath"] = "/disk1/cd/vms"
		ohyper["image"] = ihyper["image"]
		oservers = []
		for ihost in ihyper["hosts"]:
			ohost = {}
			ohost["name"] = ihost["name"]
			ohost["vcpu"] = ihost["vcpu"]
			ohost["mem"] = ihost["mem"]
			ohost["memunit"] = ihost["memunit"]
			ohost["hostname"] = mgmtst+ihost["name"]+"000ccz00"+instanceid
			onic = []
			onic1 = {}
			onic1["id"] = "1"
			onic1["ip"] = network + "." + ihost["hostip"]
			onic1["netmask"] = "255.255.255.0"
			onic1["gateway"] = network + ".1"
			onic.append(onic1)
			ohost["nic"] = onic
			oservers.append(ohost)
		ohyper["servers"] = oservers
		outj["hypervisors"].append(ohyper)
	f = open (outfile, 'w')
	f.write(json.dumps(outj, sort_keys=True,indent=4, separators=(',', ': ')))

if __name__ == "__main__":
	main()
