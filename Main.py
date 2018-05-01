import json                                                     #Allow to open and process json files
import sys                                                      #Allow the access of files on different directories
sys.path.append('/home/pi/bitrepublic/printer')
sys.path.append('/home/pi/bitrepublic/moveDetector')
sys.path.append('/home/pi/bitrepublic/speaker')
sys.path.append('/home/pi/bitrepublic/fanDriver')
sys.path.append('/home/pi/bitrepublic/displayer')
sys.path.append('/home/pi/bitrepublic/eu4you/scripts')
import Print                                                    #Allow executing fonctions from the Print script
import Tools                                                    #Allow executing fonctions from the Tools script
#import MoveDetector                                             #Allow executing fonctions from the MoveDetector script
import time                                                     #Allow using the Time.sleep() fonctions
from eu4youTest import EuForYou
from Print import Printer
from Speak import Speaker
from FanDrive import FanDriver
from Display import Displayer

config = json.load(open('/home/pi/bitrepublic/Config.json'))    #open the Config.json file to check the behaviour hte rapsberry should have
behaviour = config["behaviour"]
sleepTime = config["mainSleepTime"]
x=1                                                             #Variable used to print the number of while loops during standby from authentification

authData = False                                                #Setting the variable authData as false
Tools.setup()

while authData == False:                                        #If authData is false the script keep on trying to login on to the server
    authData = Tools.login()                                    #Filling authData with the return of the login fonction (returns false if login unsuccessful)
    time.sleep(sleepTime)                                       #Each login try, the pi must sleep before trying again not to DDOS the server

headers = {"X-Auth-Token": authData["authToken"] , "X-User-Id": authData["userId"]}     #As the script must request the server, the token&Id are needed as headers to be sent to the server
#print(str(authData))                                            #If authData!=False it contains the authToken and the userId needed to login

if behaviour=="printer":                                        #Execute the printer behaviour if the config specifies the pi is supposed to be a printer
    thread_Print = Printer(headers)
    thread_Print.start()
    
if behaviour=="speakerPrinter":
    thread_Print = Printer(headers)
    thread_Speak = Speaker(headers)
    thread_Print.start()
    thread_Speak.start()

if behaviour=="fanPrinter":
    thread_Print = Printer(headers)
    thread_Fan = FanDriver(headers)
    thread_Print.start()
    thread_Fan.start() 

if behaviour=="displayer":
    thread_Display = Displayer(headers)
    thread_Display.start()

if behaviour=="moveDetector":                                    #Execute the moveDetector behaviour if the config specifies the pi is supposed to be a moveDetector
    #MoveDetector.setup()
    #MoveDetector.run(headers)
    eu4youClass = EuForYou()
    eu4youClass.run(headers)
