#!/usr/bin/python
__author__='tongqg'

import xml.etree.ElementTree as ET
import unittest
import json

"""
This tool is to transform a json string to xml. 
This is an example
{"root":{"__type":"value", "sub":[{"__text":"text"}, {"__type":"value", "__text":"text"}], "sub2":"value"}}
=>
<root type=value><sub>text</sub><sub type=value>text</sub><sub2>value</sub2></root>
"""

def jsonToXML(jsonObject):
	rootStr = jsonObject.keys()[0]
	root = ET.Element(rootStr)
	jsonToDocument(root, jsonObject[rootStr])
	return root

def jsonToDocument(parent, jsonObject):
	if type(jsonObject) == dict:
		for k in jsonObject:
			v = jsonObject[k]
			if k.find('__')>=0:
				if k.find('__text')>=0:
					parent.text = v
				else:
					parent.set(k[2:], v)
			elif type(v) == list:
				for o in v:
					eSub = ET.SubElement(parent, k)
					jsonToDocument(eSub, o)
			else:
				eSub = ET.SubElement(parent, k)
				jsonToDocument(eSub, v)
	else:
		parent.text = jsonObject
	return

class UnitTest(unittest.TestCase):
	def test_case1(self):
		jsono = {"root":{"__type":"value", "sub":[{"__text":"text"}, {"__type":"value", "__text":"text"}], "sub2":"value"}}
		print ET.dump(jsonToXML(jsono))


if __name__ == "__main__":
	unittest.main()
