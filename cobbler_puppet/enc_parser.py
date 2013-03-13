#!/usr/bin/enc python

import yaml
import unittest
import exceptions
from custom_exceptions import *

class EncParser:
    """
    This is the class that parses your ENC output.  The default way of accessing
    the data is in paramters: of your ENC YAML, prefixed by "cobbler_".  E.g.,:
    cobbler_system_name can be retrieved by grabbing .system_name.  You can customize
    this class to support a different "schema," if you wish, simply by changing
    the getters.
    """

    def __init__(self, enc):
        self._enc = enc
        self._definition = {}

    def fetch_param(self, param):
        """
        Assumes a normal method of accessing the parameter.  Key in enc["parameters"]
        prefixed by cobbler.
        """

        if not self._definition.has_key(param):
            try:
                self._definition[param] = self._enc["parameters"]["cobbler_%s" % param]
            except KeyError:
                self.missing(param)

        return self._definition[param]

    def get_raw(self):
        return yaml.dump(self._enc)

    def get_system_name(self):
        """
        Getter for system profile name
        """
        return self.fetch_param("system_name")

    def get_hostname(self):
        """
        Getter for hostname
        """
        return self.fetch_param("hostname")

    def get_profile(self):
        """
        Getter for profile
        """
        return self.fetch_param("profile")

    def get_kernel_opts(self):
        """
        Getter for kernel opts
        """
        return self.fetch_param("kernel_opts")

    def get_ks_meta(self):
        """
        Getter for ks meta
        """
        return self.fetch_param("ks_meta")

    def get_interfaces(self):
        """
        Getter for network interfaces
        """
        return self.fetch_param("interfaces")

    def get_netboot(self):
        """
        Getter for netboot
        """
        return self.fetch_param("netboot")

    def missing(self, param):
        raise EncParameterNotFound(param)

    def __getattr__(self, name):
        """
        For nice looking access to definition.
        """
        if "get_" not in name:
            try:
                return getattr(self, "get_" + name)()
            except TypeError:
                self.missing(name)

class EncParserTests(unittest.TestCase):

    def setUp(self):
        self.enc = EncParser(yaml.load('---\nclasses:\n  ntp:\n  foobar:\n  whatever:\nparameters:\n  cobbler_system_name: web.example.com\n  cobbler_hostname: web.example.com\n  cobbler_profile: default\n  cobbler_kernel_opts:\n    aspci: "off"\n    quiet: None\n  cobbler_ks_meta:\n    location: Atlanta\n  cobbler_interfaces:\n    eth0:\n      mac: DE:AD:DE:AD:BE:EF\n      ipaddress: 192.168.2.2\n      netmask: 255.255.255.0\n      gateway: 192.168.2.1'))


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
        except EncParameterNotFound:
            pass
        else:
            self.fail("MissingRequiredCobblerParamter not thrown.")


if __name__ == "__main__":
    unittest.main()
