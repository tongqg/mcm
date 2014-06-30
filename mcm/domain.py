#!/usr/bin/env python
__author__='tongqg'

import logging
import uuid
import unittest
import random
import xml.etree.ElementTree as ET
from xml.dom import minidom
from util import xmltool

log = logging.getLogger('domain')


class DomainFactory():
	# emulator = '/usr/libexec/qemu-kvm'
	emulator = '/usr/bin/kvm-spice'
	arch='x86_64'
	# machine="rhel6.5.0"
	machine='pc'

	def __init__(self, emulator = '/usr/libexec/qemu-kvm', arch='x86_64', machine='rhel6.5.0'):
		self.emulator = emulator
		self.arch = arch
		self.machine = machine

	def gen(self, name, vcpu, mem, memunit, vda, cdrom=None, logfile='mcm.log'):
		jroot = {}
		jd = {}
		jd['__type'] = 'kvm'
		jd['name'] = name
		jd['uuid']=str(uuid.uuid1())
		
		jmemory = {}
		jmemory['__unit'] = memunit
		jmemory['__text'] = str(mem)
		jd['memory']= jmemory
		
		jvcpu = {}
		jvcpu['__palcement'] = 'static'
		jvcpu['__text'] = str(vcpu)
		jd['vcpu'] = jvcpu
		
		jent = []
		jent.append({'__name':'manufacturer', '__text': 'IBM'})
		jent.append({'__name':'product','__text':'Zenith Controller'})
		jent.append({'__name':'verson', '__text':'2014.1-201403302302.ibm.el6.116'})
		jent.append({'__name':'serial', '__text':'00000000-0000-0000-0000-002590f137c2'})
		jsysinfo = {}
		jsysinfo['__type'] = 'smbios'
		jsysinfo['system'] = {'entry': jent}
		jd['sysinfo'] = jsysinfo	

		jd['os'] = {'type':{'__arch':self.arch, '__machine':self.machine, '__text':'hvm'}, 
					'boot':{'__dev':'hd'}, 'smbios':{'__mode':'sysinfo'}}
		jdevices = {'emulator':self.emulator}
		jharddisk = {'__type' : 'file', '__device':'disk', 
					'driver':{'__name':'qemu', '__type':'qcow2', '__cache':'none'},
					'source':{'__file':vda},
					'target':{'__dev':'vda', '__bus':'virtio'}}
		if cdrom is not None:
			jcdrom = {'__type' : 'file', '__device':'cdrom', 
					'driver':{'__name':'qemu', '__type':'raw'},
					'source':{'__file':cdrom},
					'target':{'__dev':'hda', '__bus':'ide'}}
			jdevices['disk'] = [jharddisk, jcdrom]
		else:
			jdevices['disk'] = jharddisk
		jd['devices'] = jdevices
		jd['interface'] = {'__type':'bridge', 'mac':{'__address':randomMAC()}, 'source':{'__bridge':'br0'},
							'model':{'__type':'virtio'}, 'fileterref':{'__fileter':'clean-traffic'}}
		jd['console'] = {'__type': 'file', 'source':{'__path':logfile}, 'target':{'__type':'serial', '__port':'0'}}
		jroot['domain']=jd

		return xmltool.jsonToXMLStr(jroot)

def randomMAC():
	mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac))

class UnitTest(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)
	def test_gen(self):
		d = DomainFactory()
		self.prettyprint(d.gen('a', 2, 2, 'KiB', 'filepath'))
		self.prettyprint(d.gen('a', 2, 2, 'KiB', 'filepath','isopath'))
		return

	def prettyprint(self, domstr):
		newdom = minidom.parseString(domstr)
		print newdom.toprettyxml(indent='  ')


if __name__ == "__main__":
	unittest.main()
