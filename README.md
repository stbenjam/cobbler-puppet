cobbler-puppet
==============

! Still a work in progress...not ready

[![Build Status](https://travis-ci.org/stbenjam/cobbler-puppet.png)](https://travis-ci.org/stbenjam/cobbler-puppet)

Manage Cobbler Server Entries Based On Output of a Puppet External Node Classifier.

How It Works
============

Cobbler-Puppet calls your [External Node Classifier](http://docs.puppetlabs.com/guides/external_nodes.html) and looks for information about the server so that it can add the system profile to cobbler for provisioning.  An example of the default values expected are show in the paramters section.

If you want to change the "schema" of the expected ENC output, you can modify the methods in enc\_parser.py to pull the requisite data from wherever in your YAML.  For example, you might want to pull the network configuration from a 'network' class's parameters.

```yaml
---
classes:
  foo:
  bar:
  baz:
parameters:
  cobbler\_system\_name: www1
  cobbler\_hostname: www1.example.com 
  cobbler\_profile: fedora18-vm-default
  cobbler\_kernel\_opts:
    quiet:
    ascpi: off
  cobbler\_ks\_meta:
    potato: true
  cobbler\_interfaces: 
    eth0:
      bonding: slave
      bonding\_master: bond0
      macaddress: DE:AD:DE:AD:BE:ED
    eth1:
      bonding: slave
      bonding\_master: bond0
      macaddress: DE:AD:DE:AD:BE:EF
    bond0:
      bonding: master
      bonding\_opts: "mode=active-backup miimon=100"
      static: true
      ipaddress: 192.168.1.100
      subnet: 255.255.255.0
      gateway: 192.168.1.1
```

Configuration
=============

The configuration file is /etc/cobbler-puppet.conf.

Cobbler Configuration
---------------------

<pre><code>
[cobbler]
api\_url = http://localhost/cobbler\_api
use\_rhn\_auth = false
use\_shared\_secret = true
username = cobbler
password = password
</pre></code>

There are multiple ways to authenticate to cobbler.  

  * If you're using an RHN Satellite or Spacewalk, you can use the RHN's taskomatic user to authenticate.
  * If you're running this from the cobbler server, you can access the shared secret stored on the system
  * You can provide normal cobbler API credentials


Puppet Configuration
-------------------- 

<pre><code>
[puppet]
node\_lister=/bin/cat
external\_nodes=/bin/cat
</pre></code>

Cobbler-Puppet takes the normal ENC script you might use with your puppet infrastructure already.  It gets passed one argument, the name of a hostname, and must return one YAML document.

node\_lister is an additional script you may optionally provide that can return many yaml documents.  You can optionally specify an argument to this script, like a search string.  
