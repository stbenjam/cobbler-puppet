#!/usr/bin/env python

import sys
import yaml
import subprocess
from custom_exceptions import *
from config import Config
from enc_parser import EncParser
from cobbler_system import CobblerSystem
from optparse import OptionParser, OptionGroup


def run():

    ##########################################################
    #
    # Parse Command Line Options 
    #
    ##########################################################

    usage = "usage: %prog [options]"

    Parser = OptionParser(usage=usage)

    Parser.add_option("-m","--many", dest="do_many", action="store_true", default=False, help="Use node_lister and do multiple machines")
    Parser.add_option("-s","--search", dest="search_string", default="", metavar="STRING", help="Search string to pass to node_lister")
    Parser.add_option("-n","--hostname", dest="hostname",  default="", metavar="STRING", help="Target System Hostname")

    (options, args) = Parser.parse_args()

    # Either "many" or "one"
    if (not options.__dict__["do_many"] and not options.__dict__["hostname"]) or (options.__dict__["do_many"] and options.__dict__["hostname"]):
        Parser.print_help()
        print "\n*** Invalid Options: Either --many or --hostname required (and not both)"
        sys.exit(1)

    config = Config()

    # Assemble the query and the cmd
    if options.__dict__["do_many"]:
        cmd = config.node_lister
        if options.__dict__["search_string"]:
            query = options.search_string
        else:
            query = None
    else:
        cmd = config.external_nodes
        query = options.hostname

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
        print "-------------------------------------------------------------"
        enc = EncParser(system)

        try:
            required_options = [ enc.system_name, enc.profile ]
        except EncParameterNotFound, e:
            print "*** Required parameters missing for system: %s\n" % e
            print "*** Raw ENC:"
            print enc.raw
            print "-------------------------------------------------------------"
            continue

        system = CobblerSystem()

        # This is some tricky shit:  I overrode __setattr__ and __getattr__
        # in EncParser and CobblerSystem. I don't know if I like it.
        # But it's cool.

        attributes = [ "hostname", "profile", "interfaces",
                        "ks_opts", "ks_meta", "netboot" ]

        for attribute in attributes:
            try:
                system.setattr(attribute, enc.getattr(attribute))
            except EncParameterNotFound:
                # no biggie
                pass


        print "-------------------------------------------------------------"

         

