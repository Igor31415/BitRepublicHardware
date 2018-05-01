import grovepi
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('/home/pi/BitRepublicHardware/eu4you/config.cfg'))
#USReader = ultrasonicSensorReader("USReader", json.loads(self.config.get("sensor", "pins")), self.config.getint("sensor", "dist_limit"), grovepi)
sensor_pins = json.loads(config.get("sensor", "pins"))
dists = []
distSmooth = []
isActive = False
dist_limit = config.getint("sensor", "dist_limit")

"""
Bonjour = grovepi.ultrasonicRead(2)
print(Bonjour)
"""

for i, pin in enumerate(sensor_pins):
	print(pin)
	print(sensor_pins)
	dists[i] = grovepi.ultrasonicRead(pin)
	if dists[i] is not False :
		distSmooth[i] = int(round(dists[i]*0.5 + distSmooth[i]*0.5))
		active |= distSmooth[i] <= dist_limit
	isActive = active
