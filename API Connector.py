import requests
import psutil
import datetime
# from urllib.request import urlopen
import re as r
import socket
import os
import json
import tkinter as tk

now = datetime.datetime.now().replace(minute=0,second=0,microsecond=0)

# Set the endpoint URL
url = 'http://127.0.0.1:5000/login'

data_form = {}

def on_submit():
    email = email_entry.get()
    password = password_entry.get()
    token = token_entry.get()
    # data_form.append({"user_id": email, "password": password, "token": token})
    data_dump = {"user_id": email, "password": password, "token": token}
    # username = os.getlogin()
    # # file_path = os.path.join("C:", "Users", username, "Documents", "data", "data.json")
    # file_path = 'data.json'
    # os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open('data.json', 'w') as json_file:
        json.dump(data_dump, json_file)
    root.destroy()

from tkinter import *
root = tk.Tk()

root.geometry("290x150")
root.title("API Connector")

label = tk.Label(root, text="API Connector - Perdana Consulting")
label.grid(row=1, column=1 )

email_label = tk.Label(root, text="Email:")
email_label.grid(row=2, column=0, )

email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=3, column=0)

password_entry = tk.Entry(root)
password_entry.grid(row=3, column=1)

token_label = tk.Label(root, text="Token:")
token_label.grid(row=4, column=0)

token_entry = tk.Entry(root)
token_entry.grid(row=4, column=1)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=5, column=0, columnspan=4)
root.mainloop()

file_path = 'data.json'


# Read existing data from file
try:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
except:
    data = []

# Set the data for the request body
new_data = {'hostname': '', 'ipAddr': '', 'ipAddrLocal': '', 'uptime_since_last_boot': '', 'last_boot': '', 'workHours': '', 'usr_first_login': str(now), 'last_updated': str(now)}
data.update(new_data)

# Write updated data to file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file)

with open(file_path, "r") as infile:
    data = json.load(infile)

value = data['token']
print (value)
# Assume you have got the token from earlier step
headers = {'Authorization': 'Bearer ' + value}

# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Do something with the response
rServer = response.json()
print(rServer['message'])