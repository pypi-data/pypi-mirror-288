#!/usr/bin/env python3

import argparse
import ipaddress
import json

def reverse_pointer_v6(a):
    # a has to be an IPv*Interface

    out = {}

    out["reverse_pointer"] = ".".join(a.ip.packed.hex()[::-1]) + ".ip6.arpa"

    zone_prefixlen_nibbles = a.network.prefixlen // 4

    out["reverse_pointer_zone"] = ".".join(a.ip.packed.hex()[:zone_prefixlen_nibbles][::-1]) + ".ip6.arpa"

    out["reverse_pointer_host"] = ".".join(a.ip.packed.hex()[zone_prefixlen_nibbles:][::-1])

    return out

def reverse_pointer_v4(a):
    # a has to be an IPv*Interface

    out = {}

    ip_octets = list(map(str, a.ip.packed))

    out["reverse_pointer"] = ".".join(ip_octets[::-1]) + ".in-addr.arpa"

    zone_prefixlen_octets = a.network.prefixlen // 8

    out["reverse_pointer_zone"] = ".".join(ip_octets[:zone_prefixlen_octets][::-1]) + ".in-addr.arpa"

    out["reverse_pointer_host"] = ".".join(ip_octets[zone_prefixlen_octets:][::-1])

    if a.network.prefixlen > 24:
        net_octets = list(map(str, a.network.network_address.packed))

        # These are 5 octets
        ip_octets_rfc2317 = net_octets[:3] + [ net_octets[3] + "/" + str(a.network.prefixlen) ] + ip_octets[3:4]

        out["reverse_pointer_rfc2317"] = ".".join(ip_octets_rfc2317[::-1]) + ".in-addr.arpa"

        out["reverse_pointer_zone_rfc2317"] = ".".join(ip_octets_rfc2317[:3][::-1]) + ".in-addr.arpa"

        out["reverse_pointer_host_rfc2317"] = ip_octets_rfc2317[4]

    return out

def reverse_pointer(ipinterface):

    a = ipaddress.ip_interface(ipinterface)

    data = {
        "ip_version": a.version,
        "ip_interface": str(a),
        "ip_address": str(a.ip),
        "network": str(a.network),
        "prefixlen": a.network.prefixlen,
    }

    match a.version:
        case 6:
            data.update(reverse_pointer_v6(a))
        case 4:
            data.update(reverse_pointer_v4(a))
        case _:
            raise Exception(f"Unsupported IP Version {a.version}")

    return data

def main():
    parser = argparse.ArgumentParser(
        prog='ptrcalc',
    )

    parser.add_argument("ipaddress", help="IPv6 or IPv4 Address to get reverse zone for. Accepts prefixlen in CIDR notation to specify zone \"depth\".")
    parser.add_argument("--json", dest="format_json", action='store_true', help="display in json format")

    args = parser.parse_args()

    data = reverse_pointer(args.ipaddress)

    if args.format_json:
        print(json.dumps(data))
        exit()

    print(f"IP Address: {data['ip_interface']}")
    print(f"    Reverse pointer:  {data['reverse_pointer']}")
    print(f"    Zone:             {data['reverse_pointer_zone']}")
    print(f"    Host:             {data['reverse_pointer_host']}")

    if data["ip_version"] == 4 and data["prefixlen"] > 24:
        print("")
        print("RFC2317:")
        print(f"    Reverse pointer:  {data['reverse_pointer_rfc2317']}")
        print(f"    Zone:             {data['reverse_pointer_zone_rfc2317']}")
        print(f"    Host:             {data['reverse_pointer_host_rfc2317']}")

if __name__ == "__main__":
    main()
