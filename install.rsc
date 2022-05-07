# More details at https://github.com/Davie3/mikrotik-cloudflare-iplist
# Script to download the Cloudflare list
/system script add name="d3-cloudflare-download" source={
:log info "Download Cloudflare IP list";
/tool fetch url="https://raw.githubusercontent.com/Davie3/mikrotik-cloudflare-iplist/main/cloudflare-ips-v4.rsc" mode=https dst-path=cloudflare-ips-v4.rsc;
}

# Script to replace the Cloudflare list
/system script add name="d3-cloudflare-replace" source {
:log info "Remove current Cloudflare IPs";
/ip firewall address-list remove [find where list="cloudflare-ips"];
:log info "Import newest Cloudflare IPs";
/import file-name=cloudflare-ips-v4.rsc;
}

# Initialize the scheduler with the scripts
/system scheduler
add interval=1d name="d3-cf-dl" start-date=Jan/01/2000 start-time=00:05:00 on-event=d3-cloudflare-download
add interval=1d name="d3-cf-rp" start-date=Jan/01/2000 start-time=00:10:00 on-event=d3-cloudflare-replace