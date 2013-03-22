#!/usr/bin/env python

"""
CobblerSystem Class

Does the actual interaction with Cobbler.
"""

from config import Config
import xmlrpclib


class CobblerSystem:

    def __init__(self):
        config = Config()
        self._cobbler = xmlrpclib.Server(config.api_url)
        self._token = self._cobbler.login(config.username, config.password)
        self._system = self._cobbler.new_system(self._token)

    def _modify(self, key, value):
        self._cobbler.modify_system(self._system, key, value, self._token)

    def save(self):
        self._cobbler.save_system(self._system, self._token)

    def sync(self):
        self._cobbler.sync(self._token)

    def commit(self):
        self.save()
        self.sync()

    def set_hostname(self, hostname):
        """
        Sets the cobbler system hostname
        """
        self._modify("hostname", hostname)

    def set_system_name(self, system_name):
        """
        Sets the cobbler system name
        """
        self._modify("name", system_name)

    def set_profile(self, profile):
        """
        Sets the cobbler system profile name
        """
        self._modify("profile", profile)

    def set_kernel_opts(self, **kwargs):
        """
        Sets kernel options.  Pass them as named keywords.  E.g.,
        set_kernel_ops(self, foo=bar) For kernel opts without values, set it to
        None. e.g. set _kernel_opts(self, quiet=None)
        """
        self._modify("kernel_options", kwargs)

    def set_ks_meta(self, **kwargs):
        """
        Sets kickstart metadata   Pass as named keywords.  E.g.,
        set_ks_meta(self, foo=bar)
        """
        self._modify("ks_meta", kwargs)

    def set_interfaces(self, **kwargs):
        """ Parses any interfaces in a puppet create_resources style
        format """
        for interface, config in kwargs.iteritems():
            config["interface"] = interface
            self.set_interface(**config)

    def set_interface(self, **kwargs):
        """
        Creates a network interface:
        Expects keyword arguments:
        { 'interface': 'eth0',
           'macaddress': 'DE:AD:DE:AD:BE:EF',
           'ipaddress': '192.168.1.2',
           'subnet':    '255.255.255.0',
           'gateway':   '192.168.1.1',
           'static':    True
        }
        """

        interface = {}

        # Make a cobbler friendly dict -- e.g. 'ipaddress-eth0'
        skip = ['interface', 'gateway']
        for k, v in kwargs.iteritems():
            if k not in skip:
                interface['%s-%s' % (k, kwargs['interface'])] = v

        if "gateway" in kwargs:
            self._modify("gateway", kwargs["gateway"])

        self._modify("modify_interface", interface)

    def set_netboot(self, netboot):
        self._modify("netboot_enabled", netboot)
