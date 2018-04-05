import json
import sys
sys.path.append('/home/pi/bitrepublic/printer')
import Print

config = json.load(open('/home/pi/bitrepublic/Config.json'))
behaviour = config["behaviour"]

if behaviour=="printer":
    Print.run()