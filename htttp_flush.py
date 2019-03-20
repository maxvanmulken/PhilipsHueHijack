import requests
import json
import time

ip = "http://192.168.178.178/api/"

username = ""
step = 0

while True:
    new_user = requests.post(ip, data="{\"devicetype\": \"openhabHueBinding#openhab\"}")
    response = json.loads(new_user.content)[0]
    step += 1

    if 'success' in response:
        username = response['success']['username']
        print("Made a connection, after " + str(step) + " packages send.                          ")
        break
    else:
        print("Link button has not been pressed, " + str(step) + " packages send.", end="\r")

    time.sleep(1)

print("The username is: " + username)
