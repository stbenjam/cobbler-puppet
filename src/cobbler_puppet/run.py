#!/usr/bin/env python

import sys
import json
import yaml
import subprocess
from custom_exceptions import *
from config import Config
from enc_parser import EncParser
from cobbler_system import CobblerSystem
from optparse import OptionParser, OptionGroup


def run():
    """ Guts of the user-facing portion """

    # Parse Command Line Options

    usage = "usage: %prog [options]"

    Parser = OptionParser(usage=usage)

    Parser.add_option("-m", "--many", dest="do_many", action="store_true",
                      default=False, help="Use node-lister to do multiple servers")

    Parser.add_option("-s", "--search", dest="search_string", default=None,
                      metavar="STRING", help="Search string (e.g., hostname)")

    Parser.add_option("-c", "--config", dest="config_file", default="/etc/cobbler-puppet.conf",
                      metavar="STRING", help="Config file (default: /etc/cobbler-puppet.conf)")

    (options, args) = Parser.parse_args()

    if len(sys.argv) == 1:
        Parser.print_help()
        sys.exit(1)

    config = Config(configFile=options.config_file)

    # Assemble the query and the cmd
    if options.__dict__["do_many"]:
        cmd = config.node_lister
    else:
        cmd = config.external_nodes

    query = options.search_string


    ##########################################################
    #
    # Get ENC documents
    #
    ##########################################################

    try:
        output = subprocess.check_output([cmd, query])
    except subprocess.CalledProcessError, e:
        print "\n*** Error running ENC command: %s" % e
        sys.exit(1)

    documents = yaml.load_all(output)

    for system in documents:
        print "-----------------------------------------------------------"
        enc = EncParser(system)

        try:
            required_options = [enc.system_name, enc.profile]
        except EncParameterNotFound, e:
            print "*** Required parameters missing for system: %s\n" % e
            print "*** Raw ENC:"
            print enc.raw
            print "-----------------------------------------------------------"
            continue

        print "Creating new system %s...\n" % enc.system_name

        system = CobblerSystem(options.config_file)

        # Dynamically get a list of all setters from the system
        # object.
        attributes = [k[4:] for k in dir(system) if k[0:4] == "set_"]
 
        for attribute in attributes:
            try:
                # Pass the value of the ENC attribute to the cobbler
                # system's set_"attribute" method
                encAttr = getattr(enc, attribute)
                if type(encAttr) is dict:
                    getattr(system, "set_" + attribute)(**encAttr)
                    encAttr = json.dumps(encAttr, indent=4)
                else:
                    getattr(system, "set_" + attribute)(encAttr)
                print "Setting %s:\n%s\n" % (attribute, encAttr)
            except EncParameterNotFound:
                continue  # no biggie, not a required param

        system.save()
        print "System saved!"
        print "-----------------------------------------------------------"

    if config.cobbler_sync:
        """
        Sync cobbler
        """
        print "Syncing cobbler..."
        system.sync()
        print "Done."
        print "-----------------------------------------------------------"
