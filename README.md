cobbler-puppet
==============

Manage Cobbler Server Entries Based On Output of a
Puppet External Node Classifier.


Configuration
-------------

The configuration file is /etc/puppet/cobbler.conf

[cobbler]
use_rhn_auth = false
api_url = http://localhost/cobbler_api
username = cobbler
password = password

[puppet]
node_lister=/bin/cat
external_nodes=/bin/cat


