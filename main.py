from rgbcolor import RGBColor
from location import Location
from weather import Weather


auburn = Location(81054)

print("Current:", auburn.currentTime)
print("SunRise:", auburn.sunRise)
print("MidDay:", auburn.midDay)
print("SunSet:", auburn.sunSet)
print("EndDay:", auburn.endDay)

auburnColor = RGBColor(auburn)

if Weather(auburn.zipCode).severe:
	print("Severe Output:", [255,0,0])
else:
	ledColor = auburnColor.color()
	print("RGB Output:", ledColor)

