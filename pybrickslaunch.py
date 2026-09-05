HUB_NAME = "Geva_Blitzy_JR"

import os
import subprocess

target = os.getenv("TARGET")
command = f"pybricksdev run ble --name {HUB_NAME} {target}"

try:
    subprocess.run(command, shell=True, check=True)
except subprocess.CalledProcessError:
    print("Error uploading code to hub")
    print(
        "Make sure to:\n- set HUB_NAME\n- turn the hub on\n- turn on bluetooth on your laptop"
    )
