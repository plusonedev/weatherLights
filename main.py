from rgbcolor import RGBColor
from location import Location


auburn = Location(48611)

print("Current:", auburn.currentTime)
print("SunRise:", auburn.sunRise)
print("MidDay:", auburn.midDay)
print("SunSet:", auburn.sunSet)
print("EndDay:", auburn.endDay)

auburnColor = RGBColor(auburn)

ledColor = auburnColor.color()

print(ledColor)
