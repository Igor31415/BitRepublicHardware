import requests                                             #Allow to send requests to the server (.get/.post/...)
import json                                                 #Allow to open and process json files

config = None                                               #As the setup() need to be executed from the Main script, variables are set as enpty global so that the setup() can fill it
address = None

def setup() :
    global address
    global config
    config = json.load(open('/home/pi/bitrepublic/Config.json'))
    address = config["requests"]["genBitSoil"]["Address"]
    
def run(headers) :
    r = requests.post(address, headers=headers)                          #send the post request.
    if r.status_code == 200:
        jdata = r.json()
        print(jdata)
    else:
        print(r)