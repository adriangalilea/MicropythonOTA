VERSION = "0.99"

import network
import secrets
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.ssid, secrets.password)

import urequests
import ujson
import os
import urequests
import time
import binascii
import uzlib
import os
import io

def extract_zip(zip_file_path, extract_dir):
    # Open the zip file and read the contents
    with open(zip_file_path, 'rb') as f:
        compressed_data = f.read()
    
    # Create a new io.BytesIO object to wrap the compressed data
    compressed_file = io.BytesIO(compressed_data)

    # Create a new uzlib.DecompIO object to decompress the data
    decompressed_data = uzlib.DecompIO(compressed_file)

    # Create the extract directory if it doesn't already exist
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    # Iterate through the contents of the zip file and extract each file
    while True:
        # Read the next file header from the decompressed data
        header = decompressed_data.read(30)
        if len(header) < 30:
            # End of file
            break

        # Parse the header fields
        name_length, _, file_size = uzlib._parse_dos_time(header[6:]), header[26:28], header[28:30]

        # Extract the filename and file data
        name = decompressed_data.read(name_length).decode('utf-8')
        data = decompressed_data.read(file_size)

        # Write the file data to disk
        with open(os.path.join(extract_dir, name), 'wb') as f:
            f.write(data)


import urequests
import ujson

username = "adriangalilea"
repository = "MicropythonOTA"

headers={'User-Agent': 'adriangalilea'}

response = urequests.get(f"https://api.github.com/repos/{username}/{repository}/releases/latest", headers=headers)
version_response = ujson.loads(response.content.decode())["tag_name"]
latest_version = float(version_response[1:])

import os
import urequests
import time

if latest_version > float(VERSION):
    response = urequests.get(f"https://github.com/{username}/{repository}/archive/{latest_version}.zip")
    with open("update.zip", "wb") as update_file:
        update_file.write(response.content)
    print("yes")
    time.sleep(1)
    extract_zip("update.zip")
    os.remove("update.zip")
    os.rename("main/main.py", "main.py")
else:
    print("already up to date")