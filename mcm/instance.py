#!/usr/bin/python
__author__='tongqg'

import unittest
import libvirt
import domain
from util import xmltool
import logging

log = logging.getLogger('instance')

class HyperVisor():
	def __init__(self, hostname, username):
		self.hostname = hostname
		self.username = username
		try:
			self.conn = self.__connect(hostname, username)		
		except:
			self.conn = None

	def __connect(self, hostname, username):
		return libvirt.open("qemu+ssh://{0}@{1}/system".format(username, hostname))

	def close(self):
		if self.conn is not None:
			self.conn.close()

	def defineDomain(self, xmlstr):
		if self.conn is not None:
			self.conn.defineXML(xmlstr)
		return

	def undefineDomain(self, name):
		list = self.listDefinedDomain()
		for d in list:
			if (d == name):
				self.lookupDomain(name).undefine()
		return 		

	def listDefinedDomain(self):
		if self.conn is not None:
			return self.conn.listDefinedDomains()
		else:
			return []

	def listActiveDomain(self):
		if self.conn is not None:
			return self.conn.listDomainsID()
		else:
			return []

	def lookupDomain(self, name):
		if self.conn is not None:
			return self.conn.lookupByName(name)
		return

	def startDomain(self, name):
		if self.conn is not None:
			dom = self.lookupDomain(name)
			if (dom is not None):
				print dom.create()
			else:
				log.error("Can't find domain " + name + ". Please define it first")
		return

	def stopDomain(self, name):
		if self.conn is not None:
			dom = self.lookupDomain(name)
			if (dom is not None):
				print dom.shutdown()
			else:
				log.error("Can't find domain " + name)
		return

	def destroyDomain(self, name):
		if self.conn is not None:
			dom = self.lookupDomain(name)
			if (dom is not None):
				print dom.destroy()
			else:
				log.error("Can't find domain " + name)
		return


class UnitTest(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)
	def test_list_domains(self):
		h = HyperVisor('192.168.10.107', 'root')
		print h.listDefinedDomain()
		h.close

	def test_start_domain(self):
		h = HyperVisor('192.168.10.107', 'root')
		h.defineDomain(xmltool.jsonToXMLStr(domain.gen('a', 2, 256, 'MiB', '/home/tongqg/vm/hda.qcow2')))
		h.startDomain('a')
		# h.stopDomain('a')
		# h.undefineDomain('a')
		h.close()


if __name__ == "__main__":
	unittest.main()
