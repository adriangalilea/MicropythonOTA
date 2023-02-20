VERSION = "1.01"

# we download and read version of filepath
# we need to execute the new file and delete the old

import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(secrets.ssid, secrets.password)

import urequests
import ujson
import os
import urequests
import time
import binascii

username = "adriangalilea"
repository = "MicropythonOTA"
filepath = "main.py"

headers={'User-Agent': 'adriangalilea'}

url = f"https://api.github.com/repos/{username}/{repository}/contents/{filepath}"
response = urequests.get(url, headers=headers)
download_url = ujson.loads(response.content.decode())["download_url"]
response = urequests.get(download_url)
with open("myfile.py", "wb") as f:
    f.write(response.content)

# Open the file
with open('myfile.py', 'r') as f:
    # Read the contents of the file
    contents = f.read()

    # Parse the contents to extract the value of the VERSION variable
    version = None
    for line in contents.split('\n'):
        if line.startswith('VERSION'):
            version = line.split('=')[1].strip()
            break

    # Print the value of the VERSION variable
    print(f'The version is: {version}')

# if latest_version > float(VERSION):
#     pass
    