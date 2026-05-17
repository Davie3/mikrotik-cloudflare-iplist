from datetime import datetime, UTC
import ipaddress
import sys

import requests

CLOUDFLARE_IP_URL_V4 = "https://www.cloudflare.com/ips-v4"
CLOUDFLARE_IP_URL_V6 = "https://www.cloudflare.com/ips-v6"
REQUEST_TIMEOUT = 30
MIN_ENTRIES_V4 = 5
MIN_ENTRIES_V6 = 3

today = datetime.now(UTC).strftime("%c") + " UTC"


def fetch_and_validate(url, family):
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    networks = []
    for raw_line in response.text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        network = ipaddress.ip_network(line, strict=False)
        if not isinstance(network, family):
            raise ValueError(
                f"Wrong address family from {url}: got {network!r}, expected {family.__name__}"
            )
        networks.append(network)
    return networks


def write_rsc(networks, output_file, list_name, header):
    lines = [f"# Generated on {today}", header]
    lines.extend(f"add list={list_name} address={n}" for n in networks)
    with open(output_file, "w") as writer:
        writer.write("\n".join(lines))


def generate_rsc(url, output_file):
    is_v6 = "v6" in url.lower()
    family = ipaddress.IPv6Network if is_v6 else ipaddress.IPv4Network
    list_name = "cloudflare-ips-v6" if is_v6 else "cloudflare-ips"
    header = "/ipv6 firewall address-list" if is_v6 else "/ip firewall address-list"
    min_entries = MIN_ENTRIES_V6 if is_v6 else MIN_ENTRIES_V4

    networks = fetch_and_validate(url, family)
    if len(networks) < min_entries:
        raise ValueError(
            f"Refusing to write {output_file}: got {len(networks)} entries, "
            f"minimum is {min_entries} (suspicious upstream response)"
        )

    for n in networks:
        print(f"Adding IP: {n}")

    write_rsc(networks, output_file, list_name, header)


def main():
    print(today)
    generate_rsc(CLOUDFLARE_IP_URL_V4, "cloudflare-ips-v4.rsc")
    generate_rsc(CLOUDFLARE_IP_URL_V6, "cloudflare-ips-v6.rsc")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(1)
