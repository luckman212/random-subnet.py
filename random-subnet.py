#!/usr/bin/env python3

import ipaddress
import struct
import random
import sys

def ip_range(addr_spec):
    ip = ipaddress.ip_network(addr_spec)
    base = struct.unpack('>I', ip.network_address.packed)[0]
    mask = struct.unpack('>I', ip.netmask.packed)[0]
    extent = 0x100000000 - mask
    return range(base, base+extent)

rfc1918 = [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16' ]
try:
    cidr = sys.argv[1]
except:
    cidr = 24

ranges = [ ip_range(random.choice(rfc1918)) ]
weights = [ len(r) for r in ranges ]
rng = random.choices(ranges, weights=weights)[0]
ip_int = random.choice(rng)
ip_addr = ipaddress.ip_address(ip_int)
try:
    subnet = ipaddress.IPv4Network((ip_addr, int(cidr)), strict=False)
except ipaddress.NetmaskValueError:
    print(f'invalid netmask ({cidr})')
    exit(1)
except ValueError:
    print(f'invalid input ({cidr})')
    exit(1)
else:
    print(subnet)
