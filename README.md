# Zabbix whois expiry auto-discovery and check

## Requirements

- Python **3**
- `pip3 install py-zabbix python-whois`

## Known issues

`.no` domains are broken since python-whois just returns a bunch of nulls.

## Description

This Zabbix template and associated scripts will automatically create and monitor items and triggers for domain expiry.

It uses trapper items so the scheduling is handled entirely independently from Zabbix Server and can run from anywhere as long as it is able to send values to Zabbix Server.

If `zabbix_sender` works for a host then this script should too. The py-zabbix module uses the configuration file for zabbix_agent to figure out where to send the trapper items to and such. That means the `ServerActive=`-parameter in *zabbix_agentd.conf* is used to figure out where to send the item.

The default is `ServerActive=127.0.0.1` so this should work without any config changes needed if you run it directly on your zabbix server.

`zabbix_sender` manpage: <https://www.zabbix.com/documentation/3.4/manpages/zabbix_sender>

## Installation

Put the scripts on the host you want to perform the whois-checks from. Remember that you need Python 3 and to install the modules mentioned further up the readme.

In the same folder as the scripts, create a folder called `whois` and create a json-file containing the domains you want to check. There's an example included in this repo. Make sure you name the file the same as the hostname in Zabbix because it is used as an argument by the scripts both to pick which json-file to read domains from and which host the data belongs to when sent to the Zabbix server.

Add the Zabbix template to the host and schedule both the discovery and check scripts to run every day or however often you think is approperiate.

Append the name of the system running this script to the end of the command, in the example below the host name is 'SRV - Web'.

Example with cron:

```crontab

20 12 * * * python3 zabbix-whois-discovery.py example.host.name "SRV - Web"
30 12 * * * python3 zabbix-whois-check.py example.host.name "SRV - Web"

```

## Adding domains to existing host

Just add more domains to the approperiate json-files and either run the scripts manually or wait for the cronjob.
