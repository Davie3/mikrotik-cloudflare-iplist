from datetime import datetime, UTC
import requests

cloudflareIpURLv4 = "https://www.cloudflare.com/ips-v4"
cloudflareIpURLv6 = "https://www.cloudflare.com/ips-v6"
today = datetime.now(UTC).strftime("%c") + " UTC"


def generate_rsc(url, outputFile):
    file_data = requests.get(url).content

    writer = open(outputFile, "w")
    writer.write("# Generated on " + today)

    if "v6" in url.lower():
        writer.write("\n/ipv6 firewall address-list")
    else:
        writer.write("\n/ip firewall address-list")

    for line in file_data.splitlines():
        ip = str(line.decode("utf-8"))
        print("Adding IP: " + ip)
        if "v6" in url.lower():
            writer.write("\nadd list=cloudflare-ips-v6 address=" + ip)
        else:
            writer.write("\nadd list=cloudflare-ips address=" + ip)

    writer.close()


def main():
    print(today)
    generate_rsc(cloudflareIpURLv4, "cloudflare-ips-v4.rsc")
    generate_rsc(cloudflareIpURLv6, "cloudflare-ips-v6.rsc")


if __name__ == "__main__":
    main()
