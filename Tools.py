import requests
import hashlib
import socket
import json

config = json.load(open('/home/pi/bitrepublic/Config.json'))
address = config["requests"]["login"]["Address"]
data = {'username': socket.gethostname(),'password': config["requests"]["login"]["password"],'hashed': True}     #!!! b'your money is my privacy'
                                                                                            #    ^ removed
def hashPassword(pwd):
    hash_object = hashlib.sha256(pwd)
    hex_dig = hash_object.hexdigest()
    password = hex_dig
    return password

def login():
    data["password"] = hashPassword(data["password"])
    r = requests.post(address, data=data)
    if r.status_code==200:              #checks if the server respond
        jdata = r.json()
        #print(jdata)
        if jdata["data"]!=False: 
            myAuthToken = (jdata["data"]["authToken"])
            myUserId = (jdata["data"]["userId"])
            
            dataList = {'authToken': myAuthToken, 'userId': myUserId}
            return dataList
    else:
        print(r)