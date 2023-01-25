import psutil, json
from datetime import datetime, timedelta
from urllib.request import urlopen
import re as r
import socket
import requests

# REFRESH JSON DATA WHEN DAY IS
with open('data.json', 'r') as f:
    data = json.load(f)

now = datetime.now()
now_seconds = datetime.now().replace(second=0,microsecond=0)

last_updated = datetime.strptime(data['last_updated'], "%Y-%m-%d %H:%M:%S")

if last_updated.day != now.day:
    data['usr_first_login'] = str(now_seconds)
    data['last_updated'] = str(now.replace(microsecond=0))

with open('data.json', 'w') as f:
    json.dump(data, f)



#GET DATA FOR USR_FIRST LOGIN, WORKHOURS, CHECKING IF USR_FIRST_LOGIN MORE LATEST THAN NOW = JSON NOT CHANGED
with open('data.json', 'r') as f:
    data = json.load(f)

usr_first_login = data['usr_first_login']
usr_first_login = datetime.strptime(usr_first_login, "%Y-%m-%d %H:%M:%S")

timewatch = now.replace(minute=0, second=0, microsecond=0)

a = usr_first_login
b = timewatch
workHours = b - a
print(workHours)

if usr_first_login.hour > now.hour:
    data['usr_first_login'] = str(now_seconds)
    with open('data.json', 'w') as f:
        json.dump(data, f)
elif usr_first_login.hour < now.hour:
    print ("FIRST LOGIN LEBIH AWAL DARI SAAT INI!")

# GET IP PUBLIC FOR LOCATION
def getIP():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

ipAddr = getIP()

# GET LAST REBOOT TIME
boot_time = psutil.boot_time()
boot_time_datetime = datetime.fromtimestamp(boot_time)
t_boottime = str(boot_time_datetime)

# GET UP TIME 
from datetime import datetime
now = datetime.now()
uptime_since_last_boot = now - datetime.fromtimestamp(boot_time)

##GET IP LOCAL AND HOSTNAME
hostname = socket.gethostname()
ipLocal = socket.gethostbyname(hostname)


# START PROCESS #
# Set the endpoint URL
url = 'http://117.54.110.201:8029/endpoint'

# Assume you have got the token from earlier step
headers = {'Authorization': 'Bearer ' + data['token']}

#load json
with open('data.json', 'r') as f:
    data = json.load(f)

# Set the data for the request body to json
data["hostname"] = hostname
data["ipAddr"] = str(ipAddr)
data["ipAddrLocal"] = ipLocal
data["uptime_since_last_boot"] = str(uptime_since_last_boot)
data["last_boot"] = t_boottime
data["workHours"] = str(workHours)
# data["usr_first_login"] = str(usr_first_login)
data["last_updated"] = str(datetime.now().replace(microsecond=0))

# Write updated data to file
with open('data.json', 'w') as f:
    json.dump(data, f)

with open('data.json', 'r') as f:
    data1 = json.load(f)

# print (data)
# Make the POST request
response = requests.post(url, headers=headers, json=data1)

print(response.json())