cobbler-puppet
==============

Travis CI: [![Build Status](https://travis-ci.org/stbenjam/cobbler-puppet.png)](https://travis-ci.org/stbenjam/cobbler-puppet)

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
  cobbler_system_name: www1
  cobbler_hostname: www1.example.com
  cobbler_profile: default
  cobbler_kernel_opts:
    quiet:
    acpi: off
  cobbler_kernel_opts_post:
    quiet:
    acpi: on
  cobbler_ks_meta:
    potato: true
  cobbler_name_servers: [ "8.8.8.8", "8.8.4.4" ]
  cobbler_name_servers_search: example.com
  cobbler_interfaces:
    eth0:
      bonding: slave
      bonding_master: bond0
      macaddress: DE:AD:DE:AD:BE:ED
    eth1:
      bonding: slave
      bonding_master: bond0
      macaddress: DE:AD:DE:AD:BE:EF
    bond0:
      bonding: master
      bonding_opts: "mode=active-backup miimon=100"
      static: true
      ipaddress: 192.168.1.100
      subnet: 255.255.255.0
      gateway: 192.168.1.1
```

Running cobbler-import-enc:

```
[root@luna ~]# cobbler-import-enc -s www1.example.com
-----------------------------------------------------------
Creating new system www1...

Setting hostname:
www1.example.com

Setting interfaces:
{
    "bond0": {
        "subnet": "255.255.255.0", 
        "bonding": "master", 
        "static": true, 
        "bonding_opts": "mode=active-backup miimon=100", 
        "interface": "bond0", 
        "ipaddress": "192.168.1.100", 
        "gateway": "192.168.1.1"
    }, 
    "eth1": {
        "interface": "eth1", 
        "macaddress": "DE:AD:DE:AD:BE:EF", 
        "bonding": "slave", 
        "bonding_master": "bond0"
    }, 
    "eth0": {
        "interface": "eth0", 
        "macaddress": "DE:AD:DE:AD:BE:ED", 
        "bonding": "slave", 
        "bonding_master": "bond0"
    }
}

Setting kernel_opts:
{
    "quiet": null, 
    "acpi": false
}

Setting kernel_opts_post:
{
    "quiet": null, 
    "acpi": true
}

Setting ks_meta:
{
    "potato": true
}

Setting name_servers:
['8.8.8.8', '8.8.4.4']

Setting name_servers_search:
example.com

Setting profile:
default

Setting system_name:
www1

System saved!
-----------------------------------------------------------
Syncing cobbler...
Done.
-----------------------------------------------------------
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

How to Build the RPM
====================

You can use build.sh if you have mock, otherwise:

```
tar -czvf cobler-puppet.tar.gz src/
rpmbuild -ba cobbler-puppet.spec 
```
