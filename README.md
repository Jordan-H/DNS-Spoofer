<h1>DNS Spoofing Script</h1>

A DNS Spoofing python script to be executed with [PyPy](https://pypy.org/) (for faster run time) and [NetfilterQueue](https://pypi.org/project/NetfilterQueue/) 
to guarantee against any race between DNS server and attacking machine.

This implementation is a proof of concept displaying DNS spoofing as well as ARP poisoning demonstrating a Man-in-the-middle attack. 
This script utilizes NetfilterQueue to stop packets when they reach the attacking machine and filter them for a DNS name that 
we are looking for before deciding whether or not to send a spoofed response. This decreases performance significantly but is a workaround 
to guarantee that our spoofed DNS response will reach the victim machine before the DNS server will send a legitimate response as we will not 
allow specific DNS request to reach the router with our filter.

<h2>Installation</h2>

This script is intended for Linux machines with netfilter already installed and configured. 

Due to the complex setup of PyPy and NetfilterQueue, a setup script is supplied and is invoked as:

`./setup.sh` 

The setup files are downloaded in the ~/Documents directory before being installed and configured

***Note*** - if you want to run PyPy directly from command line, it should be alias'd first as follows:

`alias pypy="~/Documents/pypy-6.0.0-linux_x86_64-portable/bin/pypy"`

IP forwarding must also be enabled as follows:

`echo 1 > /proc/sys/net/ipv4/ip_forward`

The script can finally be executed as:

`pypy dns_spoof.py -v <victim IP> -r <router IP> -d <domain target> -t <spoofing IP>`

The <victim IP> is the IP address of the machine we are trying to attack with our DNS spoofing. The
<router IP> is the IP address of the router that both machines are connected to. The <domain target> is
the domain that we will try to match for when we look at outbound DNS requests from the victim
machine. The <spoofing IP> is the IP address of a website that we will serve the victim once we find a
match with the <domain target>.
