import urllib.request, json, time, datetime, configparser
from xml.dom.minidom import parseString


class Weather:
	
	def __init__(self, zipCode):
		# import config file
		config = configparser.ConfigParser()
		config.read('config.ini')
		
		# save api keys and zipcode
		apiKey = config['APIKEYS']['weatherUnderground']
		
		weatherRequestURL = "http://api.wunderground.com/api/{0}/alerts/q/{1}.json".format(apiKey, zipCode)
		
		response = urllib.request.urlopen(weatherRequestURL)
		page = response.read().decode('utf-8')
		
		self.currentWeather = json.loads(page)
		#self.latitude = self.currentWeather['current_observation']['display_location']['latitude']
		#self.longitude = self.currentWeather['current_observation']['display_location']['longitude']
		
		
		
	@property
	def severe(self):
		return len(self.currentWeather['alerts'])


