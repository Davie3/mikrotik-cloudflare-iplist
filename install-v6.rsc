# Script to download the Cloudflare list
/system script add name="d3-cloudflare-download-v6" source={
:log info "Download Cloudflare IP list (v6)";
/tool fetch url="https://raw.githubusercontent.com/Davie3/mikrotik-cloudflare-iplist/main/cloudflare-ips-v6.rsc" mode=https dst-path=cloudflare-ips-v6.rsc;
}

# Script to replace the Cloudflare list
/system script add name="d3-cloudflare-replace-v6" source {
:log info "Remove current Cloudflare IPs (v6)";
/ip firewall address-list remove [find where list="cloudflare-ips-v6"];
:log info "Import newest Cloudflare IPs (v6)";
/import file-name=cloudflare-ips-v6.rsc;
}

# Initialize the scheduler with the scripts
/system scheduler
add interval=1d name="d3-cf-dl-v6" start-date=Jan/01/2000 start-time=00:05:00 on-event=d3-cloudflare-download-v6
add interval=1d name="de-cf-rp-v6" start-date=Jan/01/2000 start-time=00:10:00 on-event=d3-cloudflare-replace-v6