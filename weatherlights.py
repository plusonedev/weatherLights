import urllib.request, json, time, datetime, configparser
from xml.dom.minidom import parseString

# currently 28 API calls are processed every time a color is produced
#
# TODO:
#	Move all API calls into the constructor  and create variables for the other methods to reference the needed values
#	Also create an update() method that can refresh those values if the program is ever expanded and might run for 
#	longer periods of time where delays of greater than 10 minutes could be accumulated

class Location:
	
	def __init__(self, zipCode):
		# import config file
		config = configparser.ConfigParser()
		config.read('config.ini')
		
		# save api keys and zipcode
		self.weatherUndergroundKey = config['APIKEYS']['weatherUnderground']
		self.googleAPIKey = config['APIKEYS']['google']
		self.zipCode = zipCode
		
		#google geoCode API
		# supply the given zip code and the apikey
		geoCodeURL = "https://maps.googleapis.com/maps/api/geocode/json?components=postal_code:{0}&key={1}".format(self.zipCode, self.googleAPIKey)
		
		# save the returned latitude and longitude of the given zip code
		geoResponse = urllib.request.urlopen(geoCodeURL)
		geoResponse = geoResponse.read().decode('utf-8')
		geoResponse = json.loads(geoResponse)
		self.latitude = geoResponse['results'][0]['geometry']['location']['lat']
		self.longitude = geoResponse['results'][0]['geometry']['location']['lng']
		
		self.time = time.time()
		
		#google TimeZone API
		# request returns the raw UTC offset along with the dst (day light savings) offset
		tzGoogleURL = "https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&sensor=false&key={3}".format(self.latitude, self.longitude, self.time, self.googleAPIKey)
		
		tzResponse = urllib.request.urlopen(tzGoogleURL)
		tzResponse = tzResponse.read().decode('utf-8')
		tzResponse = json.loads(tzResponse)
		
		self.rawOffset = int(tzResponse['rawOffset'])
		self.dstOffset = int(tzResponse['dstOffset'])
		
		
		day = self.currentTime.strftime('%d')
		month = self.currentTime.strftime('%m')
		year = self.currentTime.strftime('%Y')
		
		# Google returns the dst offset in seconds
		# convert to hours
		offset = int(self.dstOffset / 3600)
		
		geoRequestURL = 'http://www.earthtools.org/sun/{0}/{1}/{2}/{3}/99/{4}'.format(self.latitude, self.longitude, day, month, offset)
		
		# make api call
		response = urllib.request.urlopen(geoRequestURL)
		page = response.read().decode('utf-8')
		geoDom = parseString(page)
		
		# parse out the day, month, and sunrise values
		day = geoDom.getElementsByTagName('day')[0].toxml()
		day = day.replace('<day>','').replace('</day>','')
		
		month = geoDom.getElementsByTagName('month')[0].toxml()
		month = month.replace('<month>','').replace('</month>','')
		
		sunrise = geoDom.getElementsByTagName('sunrise')[0].toxml()
		sunrise = sunrise.replace('<sunrise>','').replace('</sunrise>','')
		
		sunRiseDT = datetime.datetime(int(year), int(month), int(day))
		sunRiseTM = datetime.time(int(sunrise[0:2]), int(sunrise[3:5]), int(sunrise[6:]))
		self.sunrise = sunRiseDT.combine(sunRiseDT, sunRiseTM)
		
		sunset = geoDom.getElementsByTagName('sunset')[0].toxml()
		sunset = sunset.replace('<sunset>','').replace('</sunset>','')
		
		sunSetDT = datetime.datetime(int(year), int(month), int(day))
		sunSetTM = datetime.time(int(sunset[0:2]), int(sunset[3:5]), int(sunset[6:]))
		self.sunset = sunSetDT.combine(sunSetDT, sunSetTM)
		
	@property
	def currentTime(self):
		
		# to get current local time of the given zip code
		# add the rawOffset and the dstOffset to the UTC time stamp
		ts = self.time + self.rawOffset + self.dstOffset
		currentTime = datetime.datetime.utcfromtimestamp(ts)
		
		return(currentTime)
		
	@property
	def sunRise(self):
		
		return self.sunrise

	@property
	def sunSet(self):
		
		return self.sunset
		
	@property
	def midDay(self):
		dayDelta = self.sunSet - self.sunRise
		midDay = dayDelta / 2
		midDay = self.sunRise + midDay
		
		return midDay
	
	@property
	def endDay(self):
		endDay = datetime.time.max
		endDay = self.sunSet.combine(self.sunSet, endDay)
		
		return endDay
		
		#endDay is needed to calculate the quadrantDelta
#		self.endDay = datetime.time.max
#		self.endDay = self.sunSet.combine(self.sunSet, self.endDay)


#	@property
#	def weather(self):
		#update Weather information		
		#send GET request to weatherUnderground API
#		weatherRequestURL = "http://api.wunderground.com/api/{0}/conditions/q/{1}.json".format(self.apiKey, self.zipCode)
		
#		response = urllib.request.urlopen(weatherRequestURL)
#		page = response.read().decode('utf-8')
#		self.currentWeather = json.loads(page)
#		self.latitude = self.currentWeather['current_observation']['display_location']['latitude']
#		self.longitude = self.currentWeather['current_observation']['display_location']['longitude']
		
#		return 
