# Step by step instructions
Let's assume the following things:
- You do this directly on your Zabbix server
- You are running Ubuntu 20.04 LTS
- The domains you want to monitor are __example.com__, __example.org__, and __example.net__
- The host inside of Zabbix that you want the items and triggers to be displayed under is called __server1.example.com__

Preparation:
- Install whois by typing `sudo apt install whois`. Then type `whois example.com` to check if it even is possible to automate this for the domain you want, as we concluded could be a problem in issue number #4 
- Install pip by typing `sudo apt install python3-pip`
- Install the dependencies this script has by then typing `sudo pip install py-zabbix python-whois`

Instructions:
- Import the file _zabbix-whois-template.xml_ in the Zabbix GUI and then add the template on the __server1.example.com__ host
- Put the two .py-files from this repository anywhere on your server you want. For this example, let's just use your own users home directory _~/zabbix-whois-expiry/_
- Make the .py-files executable with `chmod +x zabbix-whois-discovery.py` and `chmod +x zabbix-whois-check.py`
- Create the folder _~/zabbix-whois-expiry/whois_ and inside that folder create a file called _server1.example.com.json_
- Put the following inside of that .json-file:
```
{
  "domains": [
    "example.com",
    "example.org",
    "example.net"
  ]
}
```

Testing:
- You can now test all of this manually by first typing `./zabbix-whois-discovery.py server1.example.com` to do the discovery, this will create the items and triggers in zabbix.
- Then type `./zabbix-whois-check.py server1.example.com` to actually run the whois check and add data to the zabbix items.

Scheduling:
- Assuming the above tests worked we will now use cron to schedule your server to automatically check the domains once each day.
- Type `crontab -e` to edit your users cron-file (this is often online just called your users crontab instead).
- Insert the following at the bottom of the editor that will appear in your terminal:
```
20 12 * * * $HOME/zabbix-whois-expiry/zabbix-whois-discovery.py server1.example.com
30 12 * * * $HOME/zabbix-whois-expiry/zabbix-whois-check.py server1.example.com
```
- This means that 20 minutes past 12 on every day the file _~/zabbix-whois-expiry/zabbix-whois-discovery.py_ with the argument _server1.example.com_ will automatically run.
- Then at 30 minutes past 12 on every day the file _~/zabbix-whois-expiry/zabbix-whois-check.py_ with the argument _server1.example.com_ will automatically run.
- (Look up "crontab syntax" on a search engine if you're curious what the three asterisk symbols mean)

If you want to do this again for other hosts in zabbix just create new appropriately named .json-files and lines in your crontab and wait. If you no longer want to monitor a domain just remove it from the .json-file and wait, it will disappear automatically after a day or two. "Discovered" items in zabbix have an expiry time on them so this is why we run the discovery every day to remind zabbix of them as long as the domains exist in the .json-files.
