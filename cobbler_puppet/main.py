#!/usr/bin/env python

import yaml
import sys
import subprocess
import errors
from config import Config
from cobbler_system import CobblerSystem
from optparse import OptionParser, OptionGroup

usage = "usage: %prog [options]"

Parser = OptionParser(usage=usage)

Parser.add_option("-m","--many", dest="do_many", action="store_true", default=False, help="Use node_lister and do multiple machines")
Parser.add_option("-s","--search", dest="search_string", default="", metavar="STRING", help="Search string to pass to node_lister")

Parser.add_option("-n","--hostname", dest="hostname",  default="", metavar="STRING", help="Target System Hostname")

(options, args) = Parser.parse_args()

# Either one or the other methods

if (not options.__dict__["do_many"] and not options.__dict__["hostname"]) or (options.__dict__["do_many"] and options.__dict__["hostname"]):
    Parser.print_help()
    print "\n*** Invalid Options: Either --many or --hostname required (and not both)"
    sys.exit(1)

config = Config()

# Assembly the query and the cmd
if options.__dict__["do_many"]:
    cmd = config.node_lister
    if options.__dict__["search_string"]:
        query = options.search_string
    else:
        query = None
else:
    cmd = config.external_nodes
    query = options.hostname

# Run query and the cmd
output = subprocess.check_output([cmd, query])
documents = yaml.load_all(output)

for system in documents:
    min_params = [ "cobbler_hostname", "cobbler_profile" ]

    if system["parameters"]:
        for param in min_params:
            if system["parameters"].has_key(param) is False:
                print "Invalid System Definition! Details:\n %s\n" % system
                continue
    
        system = CobblerSystem()
        system.
    else:
        print "Invalid System Definition! Details:\n %s\n" % system

