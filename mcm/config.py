#!/usr/bin/python
__author__='tongqg'

import logging
import unittest
import json

def loadConfig(filename='servers.conf'):
	return json.loads(loadFile(filename))

def loadFile(filename):
    f = open(filename, 'r')
    __conf = f.read()
    f.close()
    return __conf


class UnitTest(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)
	def test1(self):
		print loadConfig('../servers.conf')

if __name__ == "__main__":
	unittest.main()
