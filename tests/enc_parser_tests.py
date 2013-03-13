import sys
import yaml
import unittest

# Load Module
sys.path.append('../src')
import cobbler_puppet

class EncParserTests(unittest.TestCase):

    def setUp(self):
        self.enc = cobbler_puppet.EncParser(yaml.load('---\nclasses:\n  ntp:\n  foobar:\n  whatever:\nparameters:\n  cobbler_system_name: web.example.com\n  cobbler_hostname: web.example.com\n  cobbler_profile: default\n  cobbler_kernel_opts:\n    aspci: "off"\n    quiet: None\n  cobbler_ks_meta:\n    location: Atlanta\n  cobbler_interfaces:\n    eth0:\n      mac: DE:AD:DE:AD:BE:EF\n      ipaddress: 192.168.2.2\n      netmask: 255.255.255.0\n      gateway: 192.168.2.1'))


    def testParsing(self):
        self.assertEqual(self.enc.hostname, "web.example.com")
        self.assertEqual(self.enc.system_name, "web.example.com")
        self.assertEqual(self.enc.profile, "default")
        self.assertEqual(self.enc.kernel_opts["aspci"], "off")
        self.assertEqual(self.enc.kernel_opts["quiet"], 'None')
        self.assertEqual(self.enc.ks_meta["location"], "Atlanta")
        self.assertEqual(self.enc.interfaces["eth0"]["mac"], "DE:AD:DE:AD:BE:EF")
        self.assertEqual(self.enc.interfaces["eth0"]["ipaddress"], "192.168.2.2")
        self.assertEqual(self.enc.interfaces["eth0"]["netmask"], "255.255.255.0")
        self.assertEqual(self.enc.interfaces["eth0"]["gateway"], "192.168.2.1")

    def testMissing(self):
        try:
            self.enc.boogers
        except cobbler_puppet.EncParameterNotFound:
            pass
        else:
            self.fail("EncParameterNotFound not thrown.")


if __name__ == "__main__":
    unittest.main()

