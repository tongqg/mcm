#!/usr/bin/env python
__author__='tongqg'

import logging
import uuid
import unittest
import xml.etree.ElementTree as ET
from util import xmltool

log = logging.getLogger('domain')

def gen(name, vcpu, mem, memunit):
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

	jroot['domain']=jd

	return jroot


class UnitTest(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)
	def test_gen(self):
		print ET.dump(xmltool.jsonToXML(gen('a', 2, 2, 'KiB')))
		return

if __name__ == "__main__":
	unittest.main()
