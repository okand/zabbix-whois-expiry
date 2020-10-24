#!/usr/bin/env python3

# checks when a domain is going to expire
# and sends the time to zabbix
# new version that reads from a json file

import sys
import os
import json
import whois
from pyzabbix import ZabbixMetric, ZabbixSender

wwwhost = sys.argv[1]
zabbix_host = sys.argv[2]
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path+'/whois/'+wwwhost+'.json', 'r') as read_file:
  domains = json.load(read_file)

for domain in domains['domains']:
        try:
                w = whois.whois(domain)
                if isinstance(w.expiration_date, list):
                        packet = ZabbixMetric(zabbix_host, 'domain.expiry['+domain+']', w.expiration_date[0].timestamp()),
                else:
                     	if w.expiration_date:
                                packet = ZabbixMetric(zabbix_host, 'domain.expiry['+domain+']', w.expiration_date.timestamp()),
                result = ZabbixSender(use_config=True).send(packet)
        except:
               	print("Error occurred while executing whois() for %s." % domain)

  ## some tests
#print(w)
#print(w.domain_name, w.expiration_date)
#print(packet)
#print(result)
