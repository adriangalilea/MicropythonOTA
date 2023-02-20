VERSION = "1.0"

import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = ""
password = ""
wlan.connect(ssid, password)

import urequests

username = "adriangalilea"
repository = "MicropythonOTA"

response = urequests.get(f"https://api.github.com/repos/{username}/{repository}/releases/latest").json()

print(response)
latest_version = response.json()["tag_name"]

print(latest_version)

import os
import urequests

if latest_version > VERSION:
    response = urequests.get(f"https://github.com/{username}/{repository}/archive/{latest_version}.zip")
    with open("update.zip", "wb") as update_file:
        update_file.write(response.content)
    os.rename("main.py", "main.bak")
    os.mkdir("main")
    os.system("unzip update.zip -d main")
    os.remove("update.zip")
    os.rename("main/main.py", "main.py")