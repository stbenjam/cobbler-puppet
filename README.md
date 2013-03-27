cobbler-puppet
==============

A demo of travis CI

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
[root@luna ~]# cobbler system report --name www1
Name                           : www1
TFTP Boot Files                : {}
Comment                        : 
Enable gPXE?                   : 0
Fetchable Files                : {}
Gateway                        : 192.168.1.1
Hostname                       : www1.example.com
Image                          : 
IPv6 Autoconfiguration         : False
IPv6 Default Device            : 
Kernel Options                 : {'quiet': '~', 'acpi': False}
Kernel Options (Post Install)  : {}
Kickstart                      : <<inherit>>
Kickstart Metadata             : {'potato': True}
LDAP Enabled                   : False
LDAP Management Type           : authconfig
Management Classes             : []
Management Parameters          : <<inherit>>
Monit Enabled                  : False
Name Servers                   : ['8.8.8.8', '8.8.4.4']
Name Servers Search Path       : ['example.com']
Netboot Enabled                : True
Owners                         : ['admin']
Power Management Address       : 
Power Management ID            : 
Power Management Password      : 
Power Management Type          : ipmitool
Power Management Username      : 
Profile                        : default
Proxy                          : <<inherit>>
Red Hat Management Key         : <<inherit>>
Red Hat Management Server      : <<inherit>>
Repos Enabled                  : False
Server Override                : <<inherit>>
Status                         : production
Template Files                 : {}
Virt Auto Boot                 : <<inherit>>
Virt CPUs                      : <<inherit>>
Virt Disk Driver Type          : <<inherit>>
Virt File Size(GB)             : <<inherit>>
Virt Path                      : <<inherit>>
Virt RAM (MB)                  : <<inherit>>
Virt Type                      : <<inherit>>
Interface =====                : bond0
Bonding Opts                   : mode=active-backup miimon=100
Bridge Opts                    : 
DHCP Tag                       : 
DNS Name                       : 
Master Interface               : 
Interface Type                 : bond
IP Address                     : 192.168.1.100
IPv6 Address                   : 
IPv6 Default Gateway           : 
IPv6 MTU                       : 
IPv6 Secondaries               : []
IPv6 Static Routes             : []
MAC Address                    : 
Management Interface           : False
MTU                            : 
Subnet Mask                    : 255.255.255.0
Static                         : True
Static Routes                  : []
Virt Bridge                    : 
Interface =====                : eth1
Bonding Opts                   : 
Bridge Opts                    : 
DHCP Tag                       : 
DNS Name                       : 
Master Interface               : bond0
Interface Type                 : bond_slave
IP Address                     : 
IPv6 Address                   : 
IPv6 Default Gateway           : 
IPv6 MTU                       : 
IPv6 Secondaries               : []
IPv6 Static Routes             : []
MAC Address                    : DE:AD:DE:AD:BE:EF
Management Interface           : False
MTU                            : 
Subnet Mask                    : 
Static                         : False
Static Routes                  : []
Virt Bridge                    : 
Interface =====                : eth0
Bonding Opts                   : 
Bridge Opts                    : 
DHCP Tag                       : 
DNS Name                       : 
Master Interface               : bond0
Interface Type                 : bond_slave
IP Address                     : 
IPv6 Address                   : 
IPv6 Default Gateway           : 
IPv6 MTU                       : 
IPv6 Secondaries               : []
IPv6 Static Routes             : []
MAC Address                    : DE:AD:DE:AD:BE:ED
Management Interface           : False
MTU                            : 
Subnet Mask                    : 
Static                         : False
Static Routes                  : []
Virt Bridge                    : 
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

MIT License
===========

Copyright (c) 2013 Stephen Benjamin

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

