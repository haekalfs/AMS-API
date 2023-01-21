import psutil, json
from datetime import datetime, timedelta
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

ipAddr = '117.54.110.201'

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
url = 'http://192.168.1.34:8000/endpoint'

# Assume you have got the token from earlier step
headers = {'Authorization': 'Bearer ' + data['token']}

#load json
with open('data.json', 'r') as f:
    data = json.load(f)

# Set the data for the request body to json
data["hostname"] = hostname
data["ipAddr"] = ipAddr
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













# now = datetime.now()
# start_time = datetime.now()


# now = now.replace(minute=0, second=0, microsecond=0)
# # define the start and end time of the 8-hour period
# start_time = datetime.strptime('08:00:00', '%H:%M:%S').time()
# end_time = datetime.strptime('17:00:00', '%H:%M:%S').time()




# # workHours = 0
# # check if the current time is within the 8-hour period
# if now.time() >= start_time:
#     uptime_since_last_boot = now - datetime.fromtimestamp(psutil.boot_time())
#     wo = now - eight_oclock
#     print(usr_first_login)
#     # workHours = now.time() - datetime.fromtimestamp(start_time)
#     # print(workHours)
# elif now.time() <= start_time:
#     print('test')
#     # wo = now - start_time
#     # print(wo)
# else:
#     print('test')

# # from datetime import datetime

# # create a datetime object with the input date and time
# date_time_str = "2023-01-13 01:55:15.922458"
# date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")

# # replace the time with 8:00:00
# eight_oclock = date_time_obj.replace(hour=8, minute=0, second=0)
# print(eight_oclock)



# totalworkHours = str(workHours)

# print(totalworkHours)

# # GET LAST REBOOT TIME
# boot_time = psutil.boot_time()
# boot_time_datetime = datetime.fromtimestamp(boot_time)
# print(boot_time_datetime)