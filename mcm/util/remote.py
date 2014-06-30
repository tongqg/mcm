#!/usr/bin/python
__author__='tongqg'

import logging
import unittest
import paramiko
from paramiko import SSHClient
from scp import SCPClient


def copy(hostname, username, filepath, remotefile):
	ssh = SSHClient()
	# ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname, username=username)
	ssh.exec_command("mkdir -p " + remotefile[0:remotefile.rindex('/')])
	# SCPCLient takes a paramiko get_transportt as its only argument
	scp = SCPClient(ssh.get_transport())
	scp.put(filepath, remotefile)

def run(hostname, username, command):
	ssh = SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname, username=username)
	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
	return ssh_stdout


class UnitTest(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)
	def test1(self):
		copy('192.168.10.107', 'root', '/tmp/config.iso', '/tmp/config.iso')

	def test2(self):
		print run('192.168.10.107', 'root', 'ls /tmp')

if __name__ == "__main__":
	unittest.main()
