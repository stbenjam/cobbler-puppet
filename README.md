cobbler-puppet
==============

[![Build Status](https://travis-ci.org/stbenjam/cobbler-puppet.png)](https://travis-ci.org/stbenjam/cobbler-puppet)

! Not ready for use.  Work in progress...

Manage Cobbler Server Entries Based On Output of a
Puppet External Node Classifier.


Configuration
-------------
The configuration file is /etc/cobbler-puppet.conf.

<pre><code>
[cobbler]
use_rhn_auth = false
api_url = http://localhost/cobbler_api
username = cobbler
password = password

[puppet]
node_lister=/path/to/enc
external_nodes=/path/to/enc
</code></pre>
