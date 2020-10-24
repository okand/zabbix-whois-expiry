#!/usr/bin/env python3

# read domains from a json array
# and feed them into zabbix

import sys
import os
import json
from pyzabbix import ZabbixMetric, ZabbixSender

wwwhost = sys.argv[1]
zabbix_host = '\"' + sys.argv[2] + '\"'
asdf = ''
idx = 0
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path+'/whois/'+wwwhost+'.json', 'r') as read_file:
  domains = json.load(read_file)

for idx, thing in enumerate(domains['domains']):
  if idx == 0:
    asdf += '{"{#WHOISDOMAIN}":"'+thing+'"}'
  else:
    asdf += ',{"{#WHOISDOMAIN}":"'+thing+'"}'

done = '{"data":['+asdf+']}'


packet = ZabbixMetric(zabbix_host, 'domain.expiry.item', done),
result = ZabbixSender(use_config=True).send(packet)

## some tests
#print(done)
#print(packet)
#print(result)

## another test
#f = open('/tmp/zabbix-whois.txt', 'w')
#f.write(done)
#f.close()
