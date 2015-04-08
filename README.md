weatherLights
=============
WeatherLights is a collection of python3 classes that are used to assign colors to the time of day in ten minute increments.  This was written for RGB LED lights I installed as cabinet lights.  The day is broken into quadrants which are midnight to sunRise, sunRise to midDay, midDay to sunSet, sunSet to midnight.  the first quadrant fades from Blue to Red, 2nd is Red to Yellow, 3rd is Yellow to Red, and finaly Red back to Blue.

The setup is completely modular.  A location object is instantiated using the zip code of the desired location. The location object has five property methods, currentTime(), sunRise(), sunSet(), midDay(), and endDay().  The location object is passed to the RGBColor class.

The RGBColor object's color method outputs an RGB color code.

Although weather is not currently integrated, the plan is to develop behavior that flash the lights red and white during severe weather and white and blue during different types of precipitation.

## APIs
Three seperate APIs are utilized to determine the current color output.  The Google geocoding API is used to convert the zip code into longitude and latitude coordinates.  The Google Time Zone API is used to determine the UTC offset along with the current daylight savings time offset.  An API supplied by EarthTools.org is fed the longitude, latitude, current day, month, and DLS offset to calculate the sunRise and sunSet.  In a future update Weather Underground's develop API will be used to get current weather based on zip code as well.

## Config
Config.ini has two values that must be set.  [APIKEYS][weatherUnderground] stores your Weather Underground api key and [APIKEYS][google] stores your Google Developer API access key.

## Dependencies
weatherlights.py:
urllib.request: http://docs.python-requests.org/en/latest/

rgbcolor.py:
colour: http://pypi.python.org/pypi/colour


## Use
    from rgbcolor import RGBColor
    from location import Location
    from weather import Weather
    
    bevHills = Location(90210)
    
    # location properties available
    bevHills.currentTime
    bevHills.sunRise
    bevHills.midDay
    bevHills.sunSet
    bevHills.endDay
    
    bevHillsColor = RGBColor(bevHills)
    
    if Weather(bevHills.zipCode).severe:
        # output severe weather colors
        print([255,0,0])

    else:
        # output time based color
    	bevHillsColor.color() #[255, 104, 0]

