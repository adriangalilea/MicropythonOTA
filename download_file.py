# download and read version of a given file

import network
import secrets
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.ssid, secrets.password)

import urequests
import ujson
import uio
import os
import urequests
import time
import binascii
import uzlib

username = "adriangalilea"
repository = "MicropythonOTA"
filepath = "main.py"

def filepath_version(filepath):
    if filepath in os.listdir():
        print(f'found {filepath}')
        # Open the file
        with open(filepath, 'r') as f:
            # Read the contents of the file
            contents = f.read()

            # Parse the contents to extract the value of the VERSION variable
            new_version = None
            for line in contents.split('\n'):
                if line.startswith('VERSION'):
                    new_version = line.split('=')[1].strip()
                    break
        return float(new_version.replace('"', ''))
    else:
        print(f'ERROR: not found {filepath}')
        return 0.0

version = filepath_version(filepath)
print(f"current version: {version}")

def update_file():
    global version
    # downloads file and updates if newer
    # to-do check if file is newer without downloading
    headers={'User-Agent': username}

    url = f"https://api.github.com/repos/{username}/{repository}/contents/{filepath}"
    response = urequests.get(url, headers=headers)
    download_url = ujson.loads(response.content.decode())["download_url"]
    response = urequests.get(download_url)
    with open("new_" + filepath, "wb") as f:
        f.write(response.content)

    new_version = filepath_version("new_" + filepath)
    if new_version > version:
        version = new_version
        print(f"updating file to version: {new_version}")
        try:
            os.remove(filepath)
        except OSError:
            pass
        os.rename("new_" + filepath, filepath)
    else:
        print(f"already up to date: {new_version}")
        os.remove("new_" + filepath)

import gc
print(f'Free memory: {gc.mem_free()} bytes')

while True:
    update_file()
    # Load the contents of the file into a string
    with open(filepath, 'r') as f:
        file_contents = f.read()

    # Execute the contents of the file using a custom namespace
    namespace = {}
    exec(file_contents, namespace)

    # Access a variable defined in the file from the calling namespace
    print(namespace['foo'])
    print(f'Free memory: {gc.mem_free()} bytes')
    print()