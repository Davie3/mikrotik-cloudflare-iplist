# Mikrotik Cloudflare IP Address List

Generate Mikrotik Address Lists for Cloudflare's IP ranges.

Once created, these address lists can be used to filter Web traffic on your Mikrotik Router to only come from Cloudflare's proxied IPs. Available lists for IPv4 and IPv6 Addresses.

Cloudflare does not change these IPs often, but GitHub Actions will run at 8am UTC (12am PT) and 8pm UTC (12pm PT) to generate the lists: `cloudflare-ips-v4.rsc` and `cloudflare-ips-v6.rsc`.

**Always use caution and backup your Mikrotik configurations!**

![2022-05-06 19_51_07 - WinBox (64bit) v7 2 3 on hEX (mmips)](https://user-images.githubusercontent.com/536044/167235264-3022272e-99b5-48ce-85a6-54178d75afe9.png)

![2022-05-06 19_49_40- WinBox (64bit) v7 2 3 on hEX (mmips)](https://user-images.githubusercontent.com/536044/167235272-295a3516-aa08-4cd3-8294-40a4a8c2bd3f.png)

## Usage

### Simpliest Way

- Download **install.rsc** and/or **install-v6.rsc** and upload them to your Mikrotik Router
- Run `/import file-name=install.rsc` and/or `/import file-name=install-v6.rsc` from the Mikrotik terminal
- `d3-cloudflare-download` and `d3-cloudflare-replace` will now be added to your Scripts
- `d3-cf-dl` and `d3-cf-rp` will be added to the Scheduler
- By default, the download script will run everyday at 00:05:00 and the replace script at 00:10:00. Adjust the frequency and time as needed

### Manual Way

Adjust for `cloudflare-ips-v4.rsc` and/or `cloudflare-ips-v6.rsc` depending on what you need, manually create both scripts, and add the schedule.

- Manually create the download script
`:log info "Download Cloudflare IP list";
/tool fetch url="https://raw.githubusercontent.com/Davie3/mikrotik-cloudflare-iplist/main/cloudflare-ips-v4.rsc" mode=https dst-path=cloudflare-ips-v4.rsc;`
- Manually create the replace script
`:log info "Remove current Cloudflare IPs";
/ip firewall address-list remove [find where list="cloudflare-ips"];
:log info "Import newest Cloudflare IPs";
/import file-name=cloudflare-ips-v4.rsc;`
- Schedule a job for both scripts making sure the download script runs a few minutes before the replace script
