#!/usr/bin/env python
__author__='tongqg'

import logging
import uuid
import unittest
import xml.etree.ElementTree as ET

log = logging.getLogger('domain')

def gen(name, vcpu, mem, memunit):
	root = ET.Element('domain')
	root.set('type', 'kvm')
	eName = ET.SubElement(root, 'name')
	eName.text = name
	eUUID = ET.SubElement(root, 'uuid')
	eUUID.text = str(uuid.uuid1())
	eMemory = ET.SubElement(root, 'memory')
	eMemory.set('unit', memunit)
	eMemory.text = str(mem)
	eVCPU = ET.SubElement(root, 'vcpu')
	eVCPU.text = str(vcpu)
	return root


class UnitTest(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)
	def test_gen(self):
		ET.dump(gen('a', 2, 2, 'KiB'))

if __name__ == "__main__":
	unittest.main()
