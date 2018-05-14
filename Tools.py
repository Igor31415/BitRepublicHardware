import requests                                                 #Allow to send requests to the server (.get/.post/...)
import hashlib                                                  #Allow to hash the password via sha256 method
import socket                                                   #Allow the script to get the hostname of the pi
import json                                                     #Allow to open and process json files

address = None                                                  #As the setup() need to be executed from the Main script, variables are set as enpty global so that the setup() can fill it
data = None
config = None

def setup ():
    global address                                              #Signals that we are trying to access the global variable address and not a local one only in the setup()
    global data
    global config
    config = json.load(open('/home/pi/bitrepublic/Config.json'))#Open the Config.json file to check the behaviour hte rapsberry should have
    address = config["requests"]["login"]["Address"]
    data = {'username': socket.gethostname(),'password': config["requests"]["login"]["password"],'hashed': True}    #'hashed': True informs the server that the password is crypted in sha256
    print(data)
    data["password"] = hashPassword(data["password"])                                                               #Calls hashPassword() and update the password in the data object

def hashPassword(pwd):                                          #There is where the witcraft happens, the math i meant
    hash_object = hashlib.sha256(pwd)                           #Here babies are set on fire to please the mad god
    hex_dig = hash_object.hexdigest()                           #The script lights dark candles
    password = hex_dig                                          #And then set the pentacle on fire
    return password                                             #Finally we get the desired outcome, the function return the hashed password

def login():
    global address
    global data
    r = requests.post(address, data=data)                       #Post request sent to the server
    if  r.status_code == 200:                                   #Checks if the server respond (success of the request)
        jdata = r.json()                                        #Stock the data from the request in jdata
        if jdata["data"]!=False:                                #Ckecking if jdata is false. The request can succeed but the response may not be the authData
            myAuthToken = (jdata["data"]["authToken"])
            myUserId = (jdata["data"]["userId"])
            dataList = {'authToken': myAuthToken, 'userId': myUserId}   #Creating an object to return the userId and the authToken
            return dataList
        
        else:
            print("jdata: false")
            return False
            
    else:
        print("Login failed, status code: " + str(r.status_code))
        return False