"""
config.py has the configuration for the cobbler-puppet integration tool.

Copyright 2012, Stephen Benjamin
Stephen Benjamin <skbenja@gmail.com>

"""

import os
import sys
import ConfigParser


class Config:

    def __init__(self, configFile="/etc/cobbler-puppet.conf"):
        self._cp = ConfigParser.ConfigParser()
        self._cp.readfp(open(configFile))

        self._config = {}

        # Get cobbler configuration
        if self._cp.getboolean("cobbler", "use_rhn_auth"):
            self.get_rhn_credentials()
        elif self._cp.getboolean("cobbler", "use_shared_secret"):
            self.get_shared_secret()
        else:
            self._config['username'] = self._cp.get("cobbler", "username")
            self._config['password'] = self._cp.get("cobbler", "password")

        self._config['api_url'] = self._cp.get("cobbler", "api_url")

        # Get Puppet ENC Configuration
        self._config['node_lister'] = self._cp.get("puppet", "node_lister")
        self._config['external_nodes'] = self._cp.get("puppet",
                                                      "external_nodes")

    def get_rhn_credentials(self):
        """
        If we're using the rhn authorization module, we get the taskomatic
        user's password by importing the spacewalk modules
        """
        sys.path.append('/usr/share/rhn')
        try:
            from spacewalk.common.rhnConfig import initCFG, CFG
        except ImportError:
            raise ConfigError("This is not a Spacewalk server, but the" +
                              "configuration says I am.")

        initCFG()
        self._config['username'] = 'taskomatic_user'
        self._config['password'] = CFG.SESSION_SECRET_1

    def get_shared_secret(self):
        """
        Use cobbler shared secret for auth
        """
        fd = open("/var/lib/cobbler/web.ss")
        secret = fd.read()

        self._config['username'] = ""
        self._config['password'] = secret

    def __getattr__(self, name):
        return self._config[name]


class ConfigError(Exception):
    """
    Exception when there's a problem with the configuration.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    config = Config("../etc/cobbler-puppet.conf")
    print config.username
    print config.password
    print config.api_url
    print config.external_nodes
    print config.node_lister
